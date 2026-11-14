# Unofficial Instagram CLI

The local `instagram-tools` command wraps [instagrapi](https://github.com/subzeroid/instagrapi), an MIT-licensed Python SDK. It uses the account owner's protected Instagram session, without a Meta developer app or a Postiz connection. This is a separate publishing route from Postiz.

Instagrapi 3.2.12 was installed and authenticated with the intended brand account on November 13, 2026 (America/New_York). The installed CLI successfully verified its own account and listed its posts. It subsequently published the two requested full-length Reels: owner and exact captions were read back, and both remote videos retained audio and their complete duration. Seven offline tests cover wrong-account rejection, uncertain upload outcomes, duplicate prevention, caption verification, dry runs and withholding raw error text. Comments and insights lookup remain untested. See the [release verification notes](social-crosspost.md).

## Install

Use Python 3.11 or newer, `uv`, and executable `ffmpeg`/`ffprobe`:

```sh
uv venv ~/.local/share/rnb-social/instagrapi/venv
uv pip install --python ~/.local/share/rnb-social/instagrapi/venv/bin/python 'instagrapi[video]==3.2.12'
```

Run [the helper](../scripts/instagram_tools.py) with that environment's Python. The configured installation has a `~/.local/bin/instagram-tools` launcher, which invokes a copy of the helper with the isolated environment. Video uploads require an explicit JPG thumbnail. Instagrapi reads ordinary MP4 metadata directly; that path with a supplied thumbnail avoids its optional MoviePy dependency and MoviePy's conflicting Pillow requirement.

## Connect once

Export only the intended account's cookies from an already authorized browser session to a private JSON file. The file must contain `sessionid`; additional cookie keys are ignored by the helper. Keep the containing directory at mode 0700 and the file at mode 0600. Never pass a session token as a command-line argument, print it, or commit it.

```sh
instagram-tools connect --cookies-file /private/path/cookies.json --username YOUR_BRAND
instagram-tools whoami
```

`connect` verifies the account before saving the SDK session. Its default private configuration directory is `~/.config/rnb-social/instagram/`; it records the expected username and stable account ID. Later commands reload the saved device/session state and verify both account identifiers. Use `--config /private/path/cli.json` before the subcommand to select a different configuration. Reconnecting an existing configuration must still match its stored account ID.

## Routine commands

```sh
instagram-tools status
instagram-tools whoami
instagram-tools posts --limit 5
instagram-tools comments --media https://www.instagram.com/reel/SHORTCODE/ --limit 20
instagram-tools insights
instagram-tools insights --media https://www.instagram.com/reel/SHORTCODE/
instagram-tools upload reel --file video.mp4 --thumbnail cover.jpg --caption-file caption.txt --receipt upload-receipt.json --dry-run
instagram-tools upload reel --file video.mp4 --thumbnail cover.jpg --caption-file caption.txt --receipt upload-receipt.json
```

Commands return JSON and exit nonzero on failure. `status` only inspects the local installation. `--dry-run` checks local paths, caption length and hashes; it makes no API calls and does not validate the video's encoding or Instagram eligibility. `upload photo` accepts JPG; `upload reel` and `upload video` accept MP4 and require `--thumbnail cover.jpg`. Insights require an eligible account/media and may fail independently of authentication. Comments are read-only; this helper has no reply, like, follow or messaging commands.

Uploads require a receipt path. The helper claims it before sending bytes, retains the resulting media ID and checks the published owner and exact caption. Reusing a verified receipt returns its recorded result without uploading again. An interrupted, uncertain or unverified attempt must be reconciled against the account's post history and receipt; do not delete the marker and blindly retry. Keep receipts in the private song project, outside the public workflow repository. Use a unique receipt for each requested publication, and reuse it for all attempts to reconcile that publication.

For music releases, preserve the timed burned lyrics in the vertical edit and include the source attribution, AI disclosure and versioned complete remix recipe in the Instagram caption. The helper accepts up to 2,200 caption characters; link the full recipe when the complete prompts and lyrics do not fit. It verifies the caption verbatim after upload. The helper does not currently set a per-post AI-content label; check the available platform disclosure controls for the first requested release rather than assuming that a caption or the profile's AI label sets that flag.

The upstream private API can change and can require login verification. The helper does not bypass account challenges, automatically retry restricted requests or authenticate through a third-party paid API. Refresh the protected session when Instagram actually requires it.
