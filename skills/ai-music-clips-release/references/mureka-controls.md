# Mureka API controls

Checked against the official documentation and its published OpenAPI schema on 2026-11-14. A documented feature is not a verified audio result. Retain the original reference, editable project and every charged task ID. Ask the user for song settings and wait before uploading/submitting a new music job.

## Model and endpoint choice

| Goal | Endpoint/control | Practical limits |
| --- | --- | --- |
| Higher-quality full remix | `POST /v1/song/remix`, explicit `model: mureka-9.5` | Reference audio 10–480 seconds; mixed, vocal-only, accompaniment-only and instrumental input supported. Custom lyrics and style prompt; no numeric similarity/variance or seed field. |
| Rewrite selected lyrics | `POST /v1/song/region-edit` | Replacement lyrics plus `edit_start`/`edit_end` in milliseconds; minimum 3-second edit region. Check the actual output before claiming unchanged surrounding audio. |
| Generate using a reusable voice | `POST /v1/song/generate`, `vocal_id` | Create the vocal ID with `/v1/song/vocal-clone` from a 15–30-second sample. It can be combined with `reference_id` or a prompt. Do not promise an exact voice clone. |
| Condition on a MIDI melody | Upload with `purpose: melody`, then `melody_id` on `/v1/song/generate` | MIDI is recommended; 5–60-second melody input. **The melody control cannot be combined with other generation control options**, including the reusable voice/reference controls. |
| Create an individual part | `POST /v1/track/generate` | Choose `generate_type`: Vocals, Instrumental, Drums, Bass, Guitar, Keyboard, Percussion, Strings, Synth, FX, Brass or Woodwinds. Segment boundaries, prompt, lyrics for vocals and vocal gender are available. The current request does not expose a model/seed field. |
| Export audio and editable MIDI parts | `POST /v1/song/stem`, `model: audio-separation-2` | Up to 12 WAV stems and a MIDI ZIP. Model 3 provides vocals/accompaniment WAV and MIDI; model 1 has up to 5 audio stems and **no MIDI**. Transcribed notes need review. |
| Export sheet music | `POST /v1/song/transcribe` | Returns a ZIP with MusicXML, PDF and timed lyric JSON, rather than MIDI. Best suited to clear solo vocals and steady timing. |

V9.5 remix became generally available on 2026-11-12 at **$0.50 per song**. Set `n` explicitly: the API otherwise defaults to two, with a maximum of three, and charges per output. Other operations are separately billed; check their current price before submitting.

For lyrics-to-song generation, V9.5 also accepts a target `duration` of **120–300 seconds**. That parameter is not available on the remix endpoint, and must not be presented as a native 30/60-second remix control. Short deliveries can be edited from the resulting audio while preserving the sung content.

A quality preference does not authorize spending on unrequested variants. Proposed low-variance settings must map to real API fields; prompt requests for similarity are not numeric locks. A stem/MIDI export plus local arrangement editing provides direct note and instrument control, while Mureka handles the requested vocal/song edits.

## Official sources

- [Changelog and V9.5 remix price](https://platform.mureka.ai/docs/en/changelog.html)
- [Remix](https://platform.mureka.ai/docs/api/operations/post-v1-song-remix.html)
- [Lyrics to song](https://platform.mureka.ai/docs/api/operations/post-v1-song-generate.html)
- [Upload purposes and supported lengths](https://platform.mureka.ai/docs/api/operations/post-v1-files-upload.html)
- [Region editing](https://platform.mureka.ai/docs/api/operations/post-v1-song-region-edit.html)
- [Vocal cloning](https://platform.mureka.ai/docs/api/operations/post-v1-song-vocal-clone.html)
- [Track generation](https://platform.mureka.ai/docs/api/operations/post-v1-track-generate.html)
- [Stem and MIDI export](https://platform.mureka.ai/docs/api/operations/post-v1-song-stem.html)
- [Sheet-music transcription](https://platform.mureka.ai/docs/api/operations/post-v1-song-transcribe.html)
