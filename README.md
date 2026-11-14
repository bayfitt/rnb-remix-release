# RNB Remix AI Workflows

A reusable Codex skill for making an R&B reinterpretation from a song reference, preparing fictional-artist artwork and videos, publishing requested versions, reviewing comments, and sharing completed releases. It preserves the requested creative direction, follows standing authorization without repeated routine permission questions, and checks provider limits and release details.

This repository contains agent instructions, CLI integration helpers and public remix recipes, rather than a music-generation model or audio recordings. Music, image, video, and publishing tools depend on what is available in the user's environment. Optional audio-to-MIDI services send audio to a third party and may impose non-commercial terms.

## Workflows

- [R&B remix release](skills/rnb-remix-release/SKILL.md): song references, fictional artist artwork, captioned releases and sharing.
- [AI music clips release](skills/ai-music-clips-release/SKILL.md): hook-first vertical songs, licensed motion clips with three-second cuts, and CLI publishing/analytics.

## Release workflow

- Review the song reference, creative instructions, and relevant comments on previous releases.
- Ask for the song settings and wait for answers before each new music API job: lyrics, what to preserve/change, voice/effects, tempo/key, length and candidate count. Explain the model, supported controls and estimated cost. This does not repeat previously settled reference/release permission questions.
- Check the chosen service's actual models, prices, reference controls, and requested output count before spending credits. Do not invent unsupported variance controls.
- Generate the requested versions once and keep their audio, lyrics, prompts, and provider records together.
- Make requested artwork with consistent character references, then verify the finished videos.
- Add timed English lyric captions, keep editable SRT/VTT files, and verify that YouTube publishes the caption tracks.
- Publish to the configured channel with accurate attribution and AI disclosure.
- Publish the exact generation prompt, lyrics, model, supported settings, reference excerpt and any visual prompts with every new post. Link a complete versioned remix recipe, include the prompt text directly when space permits, and verify the published description.
- Automatically share all release links with the user's previously authorized destination in one consolidated message, then verify the send result.
- Read available comments on the new videos and save actionable feedback for the next remix.

Keep personal channel settings, sharing destinations, chat identifiers, local messaging-store paths, and credentials in private project instructions or local configuration. This public skill follows those preferences without publishing them. Reading comments does not authorize posting replies or moderation.

## Public remix recipes

Every new release includes its exact music prompt, lyrics, provider/model, supported settings, reference excerpt, and visual/edit details in a linked public recipe. See [release recipes](releases/README.md). Credentials and private provider IDs are excluded.

## Install

Ask Codex to install the skill from `bayfitt/rnb-remix-release`, using the path `skills/rnb-remix-release`. Alternatively, clone the repository and copy that folder into `~/.codex/skills/` if a skill with the same name is not already installed.

Restart or reload Codex if needed, then ask:

> Use $rnb-remix-release to make an R&B remix of my reference song.

Provide the reference, desired tempo and sound, intended lyrics or theme, and requested version count. Set the publishing channel and standing sharing preferences once in private project instructions. After that, completed releases are shared automatically with the authorized destination unless you opt out or override it for a particular task.

## YouTube CLI tools

[Yutu](https://github.com/eat-pray-ai/yutu) supplies the upload, caption, thumbnail and comment commands. [youtube-cli-app](https://github.com/faborsky/youtube-cli-app) adds YouTube Analytics reports and named channel profiles. Their upload/metadata/playlist functions overlap; use one upload path per video. The clips workflow uses Yutu for uploading and the Python app for analytics.

Both tools require a Google Cloud Desktop OAuth client. Enable YouTube Data API v3 and YouTube Analytics API v2, then authorize the channel once. The optional [youtube-tools helper](skills/ai-music-clips-release/scripts/youtube_tools.py) shares that client and authorized profile between the tools; account credentials stay in the private user configuration directory. Set `YOUTUBE_CLI_APP` if the Python application is installed somewhere other than `~/.local/share/youtube-cli-app`.

```sh
python3 skills/ai-music-clips-release/scripts/youtube_tools.py --profile CHANNEL status
python3 skills/ai-music-clips-release/scripts/youtube_tools.py --profile CHANNEL connect --client /private/path/client_secret.json
python3 skills/ai-music-clips-release/scripts/youtube_tools.py --profile CHANNEL yutu channel list --for mine --output json
python3 skills/ai-music-clips-release/scripts/youtube_tools.py --profile CHANNEL cli analytics --days 28 --json
```

Routine releases use CLI calls after initial OAuth setup. Verification still matters: a successful upload is not a verified public release, and a caption insert is not yet a serving caption track. API-visible checks do not expose every YouTube Studio copyright feature.

The shared OAuth helper uses an available loopback callback port, so a local service already listening on port 8080 does not block sign-in.

The helper keeps the credential files outside the project and translates media paths to Yutu’s configured file root. It also returns a failing exit status when the installed Yutu version prints an error but exits with status zero. See the [personal CLI privacy notice](PRIVACY.md) for the Google authorization data flow.

Tested with Yutu v0.11.0 and youtube-cli-app v2.1.0: private video upload, public release, timed English caption insert and serving-state checks, comments, channel analytics, and traffic-source reports. The helper removes read-only caption defaults rejected by YouTube. Supply the AI disclosure explicitly when updating video visibility; a missing disclosure field in an API read is not proof that the setting is off. Some channel settings and independent disclosure checks still require Studio. If custom thumbnails are restricted, review the actual generated thumbnail before release.

## Optional social channels

[The unofficial Instagram CLI](skills/ai-music-clips-release/references/instagram-cli.md) wraps MIT-licensed [instagrapi](https://github.com/subzeroid/instagrapi). Version 3.2.12 is installed in an isolated environment; the `instagram-tools` launcher returns JSON. Two full-length Reels were published and verified on November 13, 2026 (America/New_York), including owner, exact captions, recipe links, remote audio and complete duration. It provides Reel/photo/video upload commands, read-only comments and eligible-account insights, with an account guard and upload receipts. Comments and insights remain untested. The helper does not set a native per-post AI label; the release captions explicitly disclose AI generation, and the account has an AI-generated profile label. This session-based route does not require a Meta developer app or connect Postiz. Keep its saved session and account configuration private.

See the [verified Instagram and TikTok release notes](skills/ai-music-clips-release/references/social-crosspost.md) for the actual publishing paths, disclosure checks and duplicate-prevention procedure.

[Postiz CLI](https://github.com/gitroomhq/postiz-agent) supplies one JSON-oriented interface for Instagram, TikTok and Facebook publishing and analytics. Its CLI is AGPL-3.0; installing it does not connect or create platform accounts. Version 2.0.27's help, version and unauthenticated status commands were checked. Keep Yutu as the YouTube upload path to avoid duplicate submissions.

```sh
npm install -g postiz@2.0.27
postiz --help
postiz auth:status
postiz integrations:list
```

The [self-hosted Postiz app](https://github.com/gitroomhq/postiz-app) and CLI are open source. Prefer a local backend when requested; keep database secrets and API keys outside the project. A healthy local installation is separate from verified platform connections. Connecting requires a configured Postiz backend and the platform account authorizations. [Postiz Cloud has no free plan](https://docs.postiz.com/cloud/overview); self-hosting requires your own provider applications. Do not start a paid plan or recurring trial without authorization. A fresh TikTok developer app also needs a [Direct Post audit for public API posts](https://developers.tiktok.com/doc/content-posting-api-get-started). Account creation, initial consent and platform reviews remain separate from routine CLI publishing. Verify each actual account connection before describing a platform as ready.

The optional unofficial [tiktok-uploader](https://github.com/wkaisertexas/tiktok-uploader) CLI uses a protected browser session instead of a developer posting grant. Version 1.2.0 installs `tiktok-uploader` and `tiktok-auth`; installation alone does not authenticate an account or verify publishing. Before using that version, remove its `authenticate_agent` debug print of full cookie dictionaries and normalize Netscape session-cookie expiry to Playwright’s `-1`; the installed copy used here has those fixes. Keep cookies private, verify the intended brand account, and stop for actual login challenges.

The [AI-label fork](https://github.com/bayfitt/tiktok-uploader/tree/feat/ai-generated-label) adds `--ai-generated` and `ai_generated=True`. It enables TikTok's native AI-generated content switch, handles its first-use confirmation, and refuses to click Post if the label cannot be verified. The wheel was rebuilt and installed; 26 tests, lint, formatting, types, and four isolated browser checks passed. Live publication with this flag is still unverified: the attempted upload stopped at an unrelated TikTok onboarding overlay before reaching the label step. No upstream pull request has been opened; that waits for confirmed live behavior. See [usage and verification](skills/ai-music-clips-release/references/tiktok-ai-label.md).

For a self-hosted backend, the CLI’s `POSTIZ_API_URL` is the backend prefix ending in `/api` (for example, `http://127.0.0.1:4007/api`), because the client appends `/public/v1/...`. Supply its protected owner API key through `POSTIZ_API_KEY`; do not use the hosted OAuth flow for this configuration. Keep the Compose project name consistent when recreating services, so the app and database remain on the same network. A local owner account, API-key authentication and an empty integration-list CLI read were verified. The unofficial TikTok CLI also reached its own authenticated Edit profile view; no TikTok upload was performed in that setup check.

For initial Instagram setup, use the owner’s real birthdate and the current verification email for the intended account. An existing instruction to check that mailbox authorizes retrieving and submitting the code; keep codes and credentials out of chat, logs and this repository. For the fictional AI artist, enable the AI-generated profile label and select a Creator account with the Musician/band category. Verify the saved name, portrait, bio, label and category after a fresh page load. This setup was completed on November 13, 2026 (America/New_York); it does not connect Postiz. Instagram desktop disabled website-link editing during that check, so the YouTube handle was included in the bio.
