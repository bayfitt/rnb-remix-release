# R&B Remix Release

A reusable Codex skill for making an R&B reinterpretation from a song reference, preparing optional fictional-artist artwork and videos, and publishing or sharing requested versions. It preserves the requested creative direction and checks permissions, provider limits, and release details.

This repository contains instructions for an agent, not a music-generation model or any songs. Music, image, video, and publishing tools depend on what is available in the user's environment. Optional audio-to-MIDI services send audio to a third party and may impose non-commercial terms.

## Install

Ask Codex to install the skill from `bayfitt/rnb-remix-release`, using the path `skills/rnb-remix-release`. Alternatively, clone the repository and copy that folder into `~/.codex/skills/` if a skill with the same name is not already installed.

Restart or reload Codex if needed, then ask:

> Use $rnb-remix-release to make an R&B remix of my reference song.

Provide the reference, the desired tempo and sound, and the intended lyrics or theme. Give the agent explicit instructions if you want it to publish the result or send links to anyone.
