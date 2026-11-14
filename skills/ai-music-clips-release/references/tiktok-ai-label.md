# TikTok CLI native AI label

The current [Studio repair branch](https://github.com/bayfitt/tiktok-uploader/tree/fix/studio-upload-flow) forks MIT-licensed [tiktok-uploader](https://github.com/wkaisertexas/tiktok-uploader). The installed **1.2.0.post1** build is pinned at [f1bb23a](https://github.com/bayfitt/tiktok-uploader/commit/f1bb23af2b51d11bbcece9b170f1aaf1a8c376e6). It includes the original [AI-label feature](https://github.com/bayfitt/tiktok-uploader/commit/9412d8e9bb85c92120efb6efaee00cfb28ff09e0) and the current Studio upload fixes.

## Usage

```sh
tiktok-uploader -v video.mp4 -d "AI-generated music" -c /private/path/cookies.txt --ai-generated
```

For full prompts and lyrics, use a UTF-8 file and verify the intended account:

```sh
tiktok-uploader -v video.mp4 --description-file caption.txt \
  -c /private/path/cookies.txt --expected-username your_handle \
  --cover cover.jpg --ai-generated --visibility only_you \
  --diagnostics-dir /private/path/attempt-diagnostics
```

Use `--visibility everyone` for an authorized public release. Check the saved post after review before announcing public availability. A private tooling test remains private unless separately authorized for release.

The Python class and convenience `upload_video(...)` function accept `ai_generated=True`. For batch uploads, set `"ai_generated": true` on each video dictionary that needs the label.

The uploader expands **Show more** when necessary, enables the native **AI-generated content** control, and handles the **Labeling AI-generated content → Turn on** confirmation. An already-enabled switch stays on. Without the flag, the uploader leaves the setting unchanged. If the requested switch cannot be verified as enabled, the upload fails before clicking Post. The observed controls use TikTok's English interface.

## Build and verification

### Current Studio repair — November 14, 2026

A traced reproduction identified an outdated cover selector leaving the editor open and a controller's contenteditable `fill()` corrupting a multiline caption. Subsequent direct CLI tests exposed a disabled Reuse of content control and a disappearing optional prompt. The repair uses the current Studio URL and cover controls, waits for the native image input, closes and verifies the cover editor, enters literal multiline captions through native keyboard input, and verifies privacy before Post. Interactivity defaults preserve TikTok's settings; explicit unavailable or conflicting requests fail clearly. Only the known optional Got it tour is dismissed automatically outside the existing split-prompt handler.

The CLI now accepts `--description-file`, `--expected-username` and `--diagnostics-dir`, returns a nonzero exit status on failure, reports the failing stage and underlying cause, and prints a matching post URL when available. It sends no second Post click after an uncertain outcome. Visible-page failure screenshots/text are private diagnostics; no cookies, page HTML or storage are captured.

- All 41 tests passed, including nine real-browser fixture checks without TikTok requests. The expanded failure check also verified private screenshot/text artifacts, error details and that Post was not called.
- Ruff lint, formatting, mypy and whitespace checks passed. The lockfile preserves the existing dependency versions.
- The wheel was rebuilt and installed. The actual `tiktok-uploader` executable, without function monkeypatches or a browser-harness fallback, uploaded one existing 253-second vertical video with its custom cover, complete multiline prompt/lyrics, pinned recipe and native AI label.
- A separate fresh authenticated browser verified the saved caption/recipe, the label within that video's card, full 253.12-second 9:16 playback with decoded audio, and Only me visibility after review. The saved cover was visually checked in Studio. Failed earlier attempts stopped before Post; one private test post was retained.
- Cookie-value logging suppression and Netscape session-cookie expiry normalization are included in this source build, so rebuilding retains them.

Keep the private upload receipt and assigned URL. The release controller now invokes this installed CLI directly, keeps an exclusive attempt receipt and log, and refuses an already-published release. Reconcile uncertain outcomes instead of starting another upload.

### Original AI-label feature verification

The 1.2.0 wheel was rebuilt with `uv build --wheel` and installed using `uv tool install --force --reinstall dist/tiktok_uploader-1.2.0-py3-none-any.whl`. Installed CLI help exposes `--ai-generated`.

- All 26 tests passed, including nine new cases for flag propagation, switch state, confirmation handling, and stopping before Post on failure.
- Ruff lint, formatting checks, and mypy passed.
- Four isolated Playwright browser checks passed against a local HTML fixture: collapsed settings with first-use confirmation, direct toggle, already-enabled label, and unchanged default. These checks made no platform requests and published nothing.
- The first live attempt stopped before Post because a TikTok onboarding overlay blocked the existing description field. It never reached the new label step.
- On November 13, 2026 (America/New_York), a subsequent live test uploaded an existing five-minute **mureka-9.5** video through the rebuilt `tiktok_uploader.cli.main` entrypoint with `--visibility only_you --ai-generated`. The original AI-label helper and Post function ran unchanged. The CLI reported success; the saved private post displayed **Creator labeled as AI-generated**. Its full description was verified in Studio, and playback was verified at 1920×1080 with a 302.573-second duration. This was a private tooling test and required no new music generation.

The live test used a local controller to save receipts and verify the account, caption, privacy and AI switch before Post. It dismissed the unrelated first-use Studio tour with its native **Got it** button before continuing. The existing uploader entered the long description through its normal typing path, which was slow. This test establishes a successful CLI upload with the native label; it does not establish unattended handling of every first-use notice.

The two other requested releases were published through an existing Chrome session controlled by the browser-harness CLI. Both native AI switches were verified before Post, both published videos show **Creator labeled as AI-generated**, and both became public after platform review. Those fallback releases did not invoke the rebuilt uploader's `--ai-generated` option; the separate private test above provides the live CLI verification. See the [cross-post verification notes](social-crosspost.md).

The original AI-label commit did not include the separate cookie-logging and session-expiry fixes. They are now included in the current Studio repair branch. Keep authentication files outside repositories.

[Upstream PR #243](https://github.com/wkaisertexas/tiktok-uploader/pull/243) was opened after the original private test and is now **closed**. Its earlier CI job did not start because GitHub reported an upstream billing lock. The Studio repair is published on the fork; no new upstream pull request was opened.

Keep the intended account, enabled native switch immediately before Post, resulting post URL and saved label evidence in private receipts. Check existing receipts before retrying an upload with an uncertain outcome.
