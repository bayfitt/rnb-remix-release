# TikTok CLI native AI label

The [feature branch](https://github.com/bayfitt/tiktok-uploader/tree/feat/ai-generated-label) forks MIT-licensed [tiktok-uploader](https://github.com/wkaisertexas/tiktok-uploader). The implementation is pinned at [9412d8e](https://github.com/bayfitt/tiktok-uploader/commit/9412d8e9bb85c92120efb6efaee00cfb28ff09e0).

## Usage

```sh
tiktok-uploader -v video.mp4 -d "AI-generated music" -c /private/path/cookies.txt --ai-generated
```

The Python class and convenience `upload_video(...)` function accept `ai_generated=True`. For batch uploads, set `"ai_generated": true` on each video dictionary that needs the label.

The uploader expands **Show more** when necessary, enables the native **AI-generated content** control, and handles the **Labeling AI-generated content → Turn on** confirmation. An already-enabled switch stays on. Without the flag, the uploader leaves the setting unchanged. If the requested switch cannot be verified as enabled, the upload fails before clicking Post. The observed controls use TikTok's English interface.

## Build and verification

The 1.2.0 wheel was rebuilt with `uv build --wheel` and installed using `uv tool install --force --reinstall dist/tiktok_uploader-1.2.0-py3-none-any.whl`. Installed CLI help exposes `--ai-generated`.

- All 26 tests passed, including nine new cases for flag propagation, switch state, confirmation handling, and stopping before Post on failure.
- Ruff lint, formatting checks, and mypy passed.
- Four isolated Playwright browser checks passed against a local HTML fixture: collapsed settings with first-use confirmation, direct toggle, already-enabled label, and unchanged default. These checks made no platform requests and published nothing.
- The live attempt stopped before Post because a TikTok onboarding overlay blocked the existing description field. It never reached the new label step. Live publication with the flag remains unverified.

The installed runtime also retains separate local fixes that suppress upstream cookie debug output and normalize Netscape session-cookie expiry. Those fixes are not included in this AI-label feature commit; rebuilding from this branch alone does not include them. Keep authentication files outside repositories and retain these fixes when replacing the installed runtime.

An upstream pull request is deferred until the native label is confirmed during a real upload. Before marking that check complete, record the intended account, enabled native switch immediately before Post, resulting post URL, and the published label when the platform exposes it. Check existing receipts before retrying an upload with an uncertain outcome.
