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
- The first live attempt stopped before Post because a TikTok onboarding overlay blocked the existing description field. It never reached the new label step.
- On November 13, 2026 (America/New_York), a subsequent live test uploaded an existing five-minute **mureka-9.5** video through the rebuilt `tiktok_uploader.cli.main` entrypoint with `--visibility only_you --ai-generated`. The original AI-label helper and Post function ran unchanged. The CLI reported success; the saved private post displayed **Creator labeled as AI-generated**. Its full description was verified in Studio, and playback was verified at 1920×1080 with a 302.573-second duration. This was a private tooling test and required no new music generation.

The live test used a local controller to save receipts and verify the account, caption, privacy and AI switch before Post. It dismissed the unrelated first-use Studio tour with its native **Got it** button before continuing. The existing uploader entered the long description through its normal typing path, which was slow. This test establishes a successful CLI upload with the native label; it does not establish unattended handling of every first-use notice.

The two other requested releases were published through an existing Chrome session controlled by the browser-harness CLI. Both native AI switches were verified before Post, both published videos show **Creator labeled as AI-generated**, and both became public after platform review. Those fallback releases did not invoke the rebuilt uploader's `--ai-generated` option; the separate private test above provides the live CLI verification. See the [cross-post verification notes](social-crosspost.md).

The installed runtime also retains separate local fixes that suppress upstream cookie debug output and normalize Netscape session-cookie expiry. Those fixes are not included in this AI-label feature commit; rebuilding from this branch alone does not include them. Keep authentication files outside repositories and retain these fixes when replacing the installed runtime.

[Upstream PR #243](https://github.com/wkaisertexas/tiktok-uploader/pull/243) was opened after the successful private test. The upstream CI job did not start: GitHub's check annotation states that the account is locked due to a billing issue. No CI test steps ran. Local checks and the live verification above passed; the pull request remains open for upstream review.

Keep the intended account, enabled native switch immediately before Post, resulting post URL and saved label evidence in private receipts. Check existing receipts before retrying an upload with an uncertain outcome.
