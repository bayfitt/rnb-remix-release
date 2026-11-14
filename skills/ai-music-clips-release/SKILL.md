---
name: ai-music-clips-release
description: Make hook-first AI music shorts from a song reference, edit licensed motion clips, and release with captions through YouTube CLIs. Use for short music or promotional clip videos and their release workflow.
---

# AI music clips release

Create the requested song first, then the clip edit. Follow the user's creative choices, output count, release authorization, private channel settings, and standing sharing preferences. Do not repeat routine authorization questions already answered in the session.

1. Identify and save the reference's title, artists, URL and audio. Read relevant previous-release comments. Write the requested replacement lyrics, with the main outcome/hook at the start. Use reference-based remix controls when available; preserve the requested melody, key, instruments and voice character as closely as the provider supports. Do not promise an exact reproduction or invent a numeric variance control. Use the requested economical model, submit once, save the task ID before polling, and reconcile an uncertain submission before spending again.
2. Save the finished audio, lyrics, prompt, provider timing data and costs. Remove an unwanted instrumental intro when a hook-first short is requested. Keep the generated master and the edited delivery audio. Preserve pitch and tempo unless the user asks for changes. Choose the short's duration from the actual sung content; do not cut required lyrics to force a duration the user did not specify.
3. Build a 9:16 motion-clip edit, with a new shot every three seconds unless overridden. Use new characters when requested. Pexels and Pixabay provide free video APIs that require API keys; their media use stock-content licenses, not open-source software licenses. Wikimedia Commons has freely licensed media with per-file conditions. Mixkit offers both commercial-use Free and personal-use-only Restricted video downloads: check the individual asset before using it. Respect access limits; do not bypass blocks. Save each selected clip's source URL, exact license, license-page evidence and checksum. Keep raw third-party clips out of the public workflow repository. Avoid implying a stock performer's endorsement or actual financial circumstances.
4. Create readable timed English lyrics from validated provider word/line timestamps. Shift every cue by any intro trim and check exact text, order, non-overlap and audio bounds. Burn the lyrics into the edit and retain editable SRT/VTT. Credit the reference song explicitly in the YouTube title and thumbnail. Put a legible remix/source label within the central image area as well, so an automatically cropped thumbnail retains it. Verify the audio/video decode, dimensions, duration, shot boundaries and representative captioned frames.
5. Prefer CLI operations for routine releases. Use Yutu for the canonical upload path, captions, thumbnail and comments; use `youtube-cli-app` for retention, watch-time/traffic analytics and channel profiles. Do not submit the same video through both tools. Both need a Google Desktop OAuth client and a one-time Google consent flow. Share one client/profile with `scripts/youtube_tools.py`, keep credentials and tokens outside the repository, and verify the returned channel ID against private settings before changing a channel. Enable YouTube Data API v3 and YouTube Analytics API v2 in the credential's Google Cloud project.
6. Upload initially private, record the returned video ID immediately, and resume that ID after interruptions. Set Music, English, accurate made-for-kids and synthetic-media disclosures. Disable optional audio leveling/stabilization when preserving the rendered master. Upload the existing timed SRT as a standard English caption track with `--isDraft=false --isAutoSynced=false`; verify `status=serving` and `isDraft=false`. Set and verify the thumbnail, then change visibility to public and read back privacy, channel, metadata and caption state. Report only checks the API actually exposes; do not claim a Studio-only copyright check was performed. If an API restriction prevents a requested setting, report it rather than silently claiming completion.
7. Read available comments on the new release and record the check time and actionable feedback, or that none are available. Reading does not authorize replies or moderation. Pull requested analytics through `youtube-cli-app`; fresh videos can have no analytics data yet. Do not schedule ongoing monitoring unless asked.
8. After the whole batch and its caption tracks are published, automatically send one consolidated link message to the user's standing authorized destination, verify the recipient and send result, and save a receipt to prevent duplicate messages. Include the workflow URL when requested. After successful workflow/tooling changes, validate and update the authorized GitHub workflow repository. Keep account identifiers, private messaging configuration, credentials and song assets out of that public update.

## CLI examples

The optional helper delegates to the upstream CLIs and converts the already-authorized profile token for Yutu; it does not request a second consent grant. `PROFILE` is a local channel profile.

```sh
youtube-tools --profile PROFILE status
youtube-tools --profile PROFILE connect --client /private/path/client_secret.json
youtube-tools --profile PROFILE yutu channel list --for mine --output json
youtube-tools --profile PROFILE yutu video insert --file video.mp4 --title 'Song | Reference Remix' --categoryId 10 --privacy private --language en --containsSyntheticMedia --forKids=false --autoLevels=false --stabilize=false --yes --output json
youtube-tools --profile PROFILE yutu caption insert --videoId VIDEO_ID --file captions.en.srt --language en --name 'English lyrics' --isDraft=false --isAutoSynced=false --yes --output json
youtube-tools --profile PROFILE yutu caption list --videoId VIDEO_ID --output json
youtube-tools --profile PROFILE cli video-update --video-id VIDEO_ID --privacy public --json
youtube-tools --profile PROFILE yutu commentThread list --videoId VIDEO_ID --maxResults 100 --output json
youtube-tools --profile PROFILE cli analytics --days 28 --json
youtube-tools --profile PROFILE cli analytics --days 28 --dimensions insightTrafficSourceType --sort=-views --json
```

Use the installed versions' help before adapting these commands. Read-only checks and retries of queries are safe; uploads and message sends need stored duplicate guards.
