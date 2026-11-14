# R&B Remix Release

A reusable Codex skill for making an R&B reinterpretation from a song reference, preparing fictional-artist artwork and videos, publishing requested versions, reviewing comments, and sharing completed releases. It preserves the requested creative direction, follows standing authorization without repeated routine permission questions, and checks provider limits and release details.

This repository contains agent instructions and a small CLI integration helper, not a music-generation model or any songs. Music, image, video, and publishing tools depend on what is available in the user's environment. Optional audio-to-MIDI services send audio to a third party and may impose non-commercial terms.

## Workflows

- [R&B remix release](skills/rnb-remix-release/SKILL.md): song references, fictional artist artwork, captioned releases and sharing.
- [AI music clips release](skills/ai-music-clips-release/SKILL.md): hook-first vertical songs, licensed motion clips with three-second cuts, and CLI publishing/analytics.

## Release workflow

- Review the song reference, creative instructions, and relevant comments on previous releases.
- Check the chosen service's actual models, prices, reference controls, and requested output count before spending credits. Do not invent unsupported variance controls.
- Generate the requested versions once and keep their audio, lyrics, prompts, and provider records together.
- Make requested artwork with consistent character references, then verify the finished videos.
- Add timed English lyric captions, keep editable SRT/VTT files, and verify that YouTube publishes the caption tracks.
- Publish to the configured channel with accurate attribution and AI disclosure.
- Automatically share all release links with the user's previously authorized destination in one consolidated message, then verify the send result.
- Read available comments on the new videos and save actionable feedback for the next remix.

Keep personal channel settings, sharing destinations, chat identifiers, local messaging-store paths, and credentials in private project instructions or local configuration. This public skill follows those preferences without publishing them. Reading comments does not authorize posting replies or moderation.

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
