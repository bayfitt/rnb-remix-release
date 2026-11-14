"""Offline checks for upload duplication, account guards, and secret-safe output."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "skills/ai-music-clips-release/scripts/instagram_tools.py"
spec = importlib.util.spec_from_file_location("instagram_tools", SOURCE)
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class FakeInstagram:
    def __init__(self, account, caption, failure=None, returned_caption=None):
        self.account = account
        self.caption = caption
        self.failure = failure
        self.returned_caption = returned_caption
        self.upload_calls = 0

    def clip_upload(self, **kwargs):
        self.upload_calls += 1
        if self.failure:
            raise self.failure
        return self.media(self.caption)

    photo_upload = clip_upload
    video_upload = clip_upload

    def media(self, caption):
        return SimpleNamespace(pk=123, code="example", product_type="clips",
                               user=self.account, caption_text=caption)

    def media_info(self, media_id):
        return self.media(self.caption if self.returned_caption is None else self.returned_caption)


class InstagramCLITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.account = SimpleNamespace(pk=10, username="example_artist", full_name="Example Artist")
        self.args = SimpleNamespace(receipt=self.root / "receipt.json")
        self.plan = {"kind": "reel", "file": "/unused/offline.mp4", "file_sha256": "a" * 64,
                     "caption": "Exact lyrics and recipe link", "thumbnail": None, "thumbnail_sha256": None}

    def assert_cli_error(self, code, fn):
        with self.assertRaises(cli.CLIError) as caught:
            fn()
        self.assertEqual(caught.exception.code, code)

    def test_username_alone_does_not_override_account_id_guard(self):
        self.assert_cli_error("wrong_account", lambda: cli.guard_account(
            self.account, {"expected_username": "example_artist", "expected_user_id": "99"}))

    def test_confirmed_upload_reused_without_second_upload(self):
        client = FakeInstagram(self.account, self.plan["caption"])
        first = cli.upload(client, self.account, self.args, self.plan)
        second = cli.upload(client, self.account, self.args, self.plan)
        self.assertEqual(client.upload_calls, 1)
        self.assertTrue(second["already_published"])
        self.assertEqual(first["url"], second["url"])
        self.assertEqual(json.loads(self.args.receipt.read_text())["status"], "published_and_verified")

    def test_timeout_after_sending_is_not_automatically_retried(self):
        client = FakeInstagram(self.account, self.plan["caption"], failure=TimeoutError())
        with self.assertRaises(TimeoutError):
            cli.upload(client, self.account, self.args, self.plan)
        self.assertEqual(json.loads(self.args.receipt.read_text())["status"], "outcome_unknown")
        self.assert_cli_error("upload_needs_reconciliation", lambda: cli.upload(client, self.account, self.args, self.plan))
        self.assertEqual(client.upload_calls, 1)

    def test_caption_mismatch_keeps_existing_publication_for_reconciliation(self):
        client = FakeInstagram(self.account, self.plan["caption"], returned_caption="Caption was lost")
        self.assert_cli_error("published_content_mismatch", lambda: cli.upload(client, self.account, self.args, self.plan))
        self.assertEqual(json.loads(self.args.receipt.read_text())["status"], "uploaded_verification_pending")
        self.assert_cli_error("upload_needs_reconciliation", lambda: cli.upload(client, self.account, self.args, self.plan))
        self.assertEqual(client.upload_calls, 1)

    def test_receipt_cannot_be_reused_for_changed_content(self):
        client = FakeInstagram(self.account, self.plan["caption"])
        cli.upload(client, self.account, self.args, self.plan)
        changed = {**self.plan, "caption": "Different caption"}
        self.assert_cli_error("receipt_conflict", lambda: cli.upload(client, self.account, self.args, changed))
        self.assertEqual(client.upload_calls, 1)

    def test_dry_run_does_not_connect_or_create_an_upload_receipt(self):
        media = self.root / "example.mp4"
        media.write_bytes(b"offline fixture; only local path/hash validation")
        caption = self.root / "caption.txt"
        caption.write_text("Example lyrics and a complete recipe link")
        thumbnail = self.root / "cover.jpg"
        thumbnail.write_bytes(b"offline fixture; only local path/hash validation")
        output = io.StringIO()
        with patch.object(cli, "client_for", side_effect=AssertionError("Must not connect")) as connect:
            with contextlib.redirect_stdout(output):
                rc = cli.main(["upload", "reel", "--file", str(media), "--thumbnail", str(thumbnail), "--caption-file", str(caption),
                               "--receipt", str(self.args.receipt), "--dry-run"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(output.getvalue())["data"]["network_calls"], 0)
        connect.assert_not_called()
        self.assertFalse(self.args.receipt.exists())

    def test_provider_error_text_is_not_echoed(self):
        secret = "sessionid=DO-NOT-PRINT-THIS"
        output = io.StringIO()
        with patch.object(cli, "run", side_effect=RuntimeError(secret)):
            with contextlib.redirect_stdout(output):
                rc = cli.main(["whoami"])
        self.assertEqual(rc, 1)
        self.assertNotIn(secret, output.getvalue())
        self.assertEqual(json.loads(output.getvalue())["error"]["code"], "RuntimeError")


if __name__ == "__main__":
    unittest.main()
