#!/usr/bin/env python3
"""JSON CLI for a protected instagrapi session. No network calls for status/help."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "rnb-social/instagram/cli.json"


class CLIError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def read_private(path):
    path = Path(path).expanduser()
    if path.stat().st_mode & 0o077:
        raise CLIError("private_file_permissions", "Credential/config files must have mode 0600.")
    return json.loads(path.read_text())


def save_json(path, value):
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temp = path.with_name(path.name + ".tmp")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(value, f, indent=2, default=str)
            f.write("\n")
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def challenge_required(*args, **kwargs):
    raise CLIError("account_verification_required", "Complete Instagram verification, then refresh the protected session.")


def connect(args):
    from instagrapi import Client

    cookies = read_private(args.cookies_file)
    config_path = args.config.expanduser().resolve()
    prior = read_private(config_path) if config_path.exists() else None
    session_path = Path(prior["session_file"]).expanduser() if prior else config_path.with_name("instagrapi-session.json")
    if prior and not session_path.is_absolute():
        session_path = config_path.parent / session_path
    settings = read_private(session_path) if session_path.exists() else {}
    settings.update(request_timeout=10, public_request_retries_count=1, session_retry_total=0)
    client = Client(settings=settings)
    client.challenge_code_handler = challenge_required
    client.change_password_handler = challenge_required
    client.login_by_sessionid(cookies["sessionid"])
    account = client.account_info()
    if account.username.casefold() != args.username.casefold():
        raise CLIError("wrong_account", "The supplied session does not belong to the requested username.")
    if prior:
        guard_account(account, prior)
    save_json(session_path, client.get_settings())
    save_json(config_path, {"expected_username": account.username, "expected_user_id": str(account.pk),
                            "session_file": str(session_path)})
    return {"authenticated": True, **account_summary(account)}


def client_for(config_path):
    from instagrapi import Client

    config_path = Path(config_path).expanduser().resolve()
    config = read_private(config_path)
    if not config.get("expected_username") or not config.get("expected_user_id"):
        raise CLIError("account_guard_missing", "Configure the expected username and user ID before using this session.")
    session_path = Path(config["session_file"]).expanduser()
    if not session_path.is_absolute():
        session_path = config_path.parent / session_path
    settings = read_private(session_path)
    settings.update(request_timeout=10, public_request_retries_count=1, session_retry_total=0)
    client = Client(settings=settings)
    client.challenge_code_handler = challenge_required
    client.change_password_handler = challenge_required
    account = client.account_info()
    guard_account(account, config)
    return client, account, session_path


def guard_account(account, config):
    if account.username.casefold() != config["expected_username"].casefold() or str(account.pk) != str(config["expected_user_id"]):
        raise CLIError("wrong_account", "The authenticated Instagram account does not match the configured account.")


def account_summary(account):
    return {"username": account.username, "full_name": account.full_name,
            "url": f"https://www.instagram.com/{account.username}/"}


def media_summary(media):
    kind = "reel" if getattr(media, "product_type", "") == "clips" else "p"
    user = getattr(media, "user", None)
    return {"id": str(media.pk), "code": media.code,
            "url": f"https://www.instagram.com/{kind}/{media.code}/",
            "username": getattr(user, "username", None),
            "caption": getattr(media, "caption_text", ""),
            "taken_at": str(getattr(media, "taken_at", "")),
            "media_type": getattr(media, "media_type", None),
            "product_type": getattr(media, "product_type", None),
            "like_count": getattr(media, "like_count", None),
            "comment_count": getattr(media, "comment_count", None)}


def media_pk(client, value):
    if value.isdecimal():
        return value
    from urllib.parse import urlsplit
    url = urlsplit(value)
    if url.scheme != "https" or url.hostname not in ("instagram.com", "www.instagram.com"):
        raise CLIError("invalid_media", "Supply an Instagram HTTPS post URL or numeric media ID.")
    return str(client.media_pk_from_url(value))


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def upload_plan(args):
    source = args.file.expanduser().resolve(strict=True)
    caption = args.caption_file.expanduser().read_text().strip()
    if not source.is_file() or not caption or len(caption) > 2200:
        raise CLIError("invalid_upload", "Supply a media file and a nonempty caption of at most 2200 characters.")
    thumbnail = args.thumbnail.expanduser().resolve(strict=True) if args.thumbnail else None
    if thumbnail and (not thumbnail.is_file() or thumbnail.suffix.lower() not in (".jpg", ".jpeg")):
        raise CLIError("invalid_thumbnail", "Supply a JPG thumbnail.")
    if args.kind == "photo" and source.suffix.lower() not in (".jpg", ".jpeg"):
        raise CLIError("invalid_photo", "instagrapi photo uploads require a JPG file.")
    if args.kind != "photo" and source.suffix.lower() != ".mp4":
        raise CLIError("invalid_video", "Supply an MP4 video.")
    if args.kind != "photo" and thumbnail is None:
        raise CLIError("thumbnail_required", "Supply --thumbnail cover.jpg for video and Reel uploads.")
    return {"kind": args.kind, "file": str(source), "file_sha256": digest(source),
            "caption": caption, "caption_characters": len(caption),
            "thumbnail": str(thumbnail) if thumbnail else None,
            "thumbnail_sha256": digest(thumbnail) if thumbnail else None}


def upload(client, account, args, plan):
    receipt = args.receipt.expanduser().resolve()
    # The receipt binds content and account. An uncertain attempt is never retried.
    identity = {k: plan[k] for k in ("kind", "file_sha256", "caption", "thumbnail_sha256")}
    identity["account_id"] = str(account.pk)
    fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    if receipt.exists():
        previous = json.loads(receipt.read_text())
        if previous.get("fingerprint") != fingerprint:
            raise CLIError("receipt_conflict", "This receipt belongs to different content or a different account.")
        if previous.get("status") == "published_and_verified":
            return {"already_published": True, **previous["media"]}
        raise CLIError("upload_needs_reconciliation", "An upload attempt already exists. Reconcile its receipt and account history before another upload.")
    receipt.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    record = {"status": "started", "started_at": now(), "fingerprint": fingerprint,
              "username": account.username, "kind": plan["kind"], "file_sha256": plan["file_sha256"]}
    # O_EXCL claims this receipt before sending bytes, including between processes.
    fd = os.open(receipt, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(record, f, indent=2)
        f.write("\n")
    try:
        kwargs = {"path": Path(plan["file"]), "caption": plan["caption"]}
        if plan["kind"] != "photo" and plan["thumbnail"]:
            kwargs["thumbnail"] = Path(plan["thumbnail"])
        method = {"reel": client.clip_upload, "video": client.video_upload, "photo": client.photo_upload}[plan["kind"]]
        media = method(**kwargs)
        record.update(status="uploaded_verification_pending", media=media_summary(media))
        save_json(receipt, record)
        verified = client.media_info(media.pk)
        if str(verified.user.pk) != str(account.pk) or verified.caption_text != plan["caption"]:
            raise CLIError("published_content_mismatch", "The uploaded account or caption did not match. Inspect the saved receipt.")
        record.update(status="published_and_verified", verified_at=now(), media=media_summary(verified))
        save_json(receipt, record)
        return record["media"]
    except BaseException:
        if record["status"] == "started":
            record.update(status="outcome_unknown", stopped_at=now())
            save_json(receipt, record)
        raise


def bounded_limit(value):
    n = int(value)
    if not 1 <= n <= 50:
        raise argparse.ArgumentTypeError("Use a limit from 1 to 50.")
    return n


def run(args):
    version = importlib.metadata.version("instagrapi")
    if args.command == "status":
        return {"instagrapi_version": version, "config_present": args.config.expanduser().is_file(),
                "authentication_checked": False}
    if args.command == "connect":
        return connect(args)
    plan = upload_plan(args) if args.command == "upload" else None
    if args.command == "upload" and args.dry_run:
        return {"dry_run": True, "network_calls": 0, **plan}
    client, account, session_path = client_for(args.config)
    try:
        if args.command == "whoami":
            return {"authenticated": True, "instagrapi_version": version, **account_summary(account)}
        if args.command == "posts":
            posts = client.user_medias_v1(str(account.pk), amount=args.limit)
            return {"username": account.username, "posts": [media_summary(m) for m in posts]}
        if args.command == "comments":
            comments = client.media_comments(media_pk(client, args.media), amount=args.limit)
            return {"comments": [{"id": str(c.pk), "username": c.user.username,
                                  "text": c.text, "created_at": str(c.created_at_utc)} for c in comments]}
        if args.command == "insights":
            return client.insights_media(int(media_pk(client, args.media))) if args.media else client.insights_account()
        if args.command == "upload":
            return upload(client, account, args, plan)
        raise CLIError("unknown_command", "Unknown command.")
    finally:
        save_json(session_path, client.get_settings())


def main(argv=None):
    os.umask(0o077)
    parser = argparse.ArgumentParser(prog="instagram-tools", description=__doc__)
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--json", action="store_true", help="JSON is the default output format.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Inspect local installation without contacting Instagram.")
    auth = sub.add_parser("connect", help="Import a private cookie JSON file from an authorized Instagram session.")
    auth.add_argument("--cookies-file", type=Path, required=True)
    auth.add_argument("--username", required=True)
    sub.add_parser("whoami", help="Verify the protected session and configured account.")
    posts = sub.add_parser("posts", help="List this account's recent posts.")
    posts.add_argument("--limit", type=bounded_limit, default=5)
    comments = sub.add_parser("comments")
    comments.add_argument("--media", required=True)
    comments.add_argument("--limit", type=bounded_limit, default=20)
    insights = sub.add_parser("insights", help="Account or media insights where the account is eligible.")
    insights.add_argument("--media")
    post = sub.add_parser("upload", help="Publish once, retaining a receipt and verifying the caption.")
    post.add_argument("kind", choices=["reel", "photo", "video"])
    post.add_argument("--file", type=Path, required=True)
    post.add_argument("--caption-file", type=Path, required=True)
    post.add_argument("--thumbnail", type=Path)
    post.add_argument("--receipt", type=Path, required=True)
    post.add_argument("--dry-run", action="store_true", help="Validate local inputs only; make no API calls.")
    args = parser.parse_args(argv)
    logging.disable(logging.CRITICAL)
    try:
        # Upstream can print filenames and request diagnostics; stdout stays JSON.
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            result = run(args)
        print(json.dumps({"ok": True, "command": args.command, "data": result}, default=str))
        return 0
    except Exception as exc:
        if isinstance(exc, CLIError):
            code, message = exc.code, exc.message
        else:
            code = type(exc).__name__
            if code in ("ChallengeRequired", "ChallengeRedirection", "ChallengeSelfieCaptcha", "LoginRequired", "TwoFactorRequired"):
                message = "Instagram requires account verification or a renewed session. Complete that step before retrying."
            elif code in ("PleaseWaitFewMinutes", "RateLimitError", "SentryBlock"):
                message = "Instagram restricted this request. Stop automatic retries."
            else:
                message = "Command failed; raw provider responses and credential values are withheld."
        print(json.dumps({"ok": False, "command": args.command, "error": {"code": code, "message": message}}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
