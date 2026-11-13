# R&B Remix Release

A reusable Codex skill for making an R&B reinterpretation from a song reference, preparing fictional-artist artwork and videos, publishing requested versions, reviewing comments, and sharing completed releases. It preserves the requested creative direction, follows standing authorization without repeated routine permission questions, and checks provider limits and release details.

This repository contains instructions for an agent, not a music-generation model or any songs. Music, image, video, and publishing tools depend on what is available in the user's environment. Optional audio-to-MIDI services send audio to a third party and may impose non-commercial terms.

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
