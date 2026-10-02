# Local editor import and saved-caption readback

On October 2, 2026, the delivered MP4 and SRT were opened in a new local Kdenlive 24.12.3 project using MLT 7.30.0. These were the original synthetic files linked by this skill. No account, recording input or uploader was involved.

The editor recognized a three-second, 320×180, 12 fps clip. The empty project was matched to that profile. The SRT import used UTF-8 with both the timeline-cursor offset and frame-rate transformation options off. Its preview showed the two supplied texts and source intervals.

The MP4 was placed on empty video/audio tracks at the timeline start. Paused project-monitor observations at `00:00:00:06` (0.5 s) and `00:00:02:00` (2 s) showed the first and second captions respectively over the synthetic picture, with no observed text clipping. A play command advanced the playhead to the final frame. This establishes the exercised UI behavior, not smooth real-time playback, subjective A/V synchronization or a listening result.

## What saving changed

The saved project retained its 320×180, 12 fps profile and two subtitle texts. Its [ASS sidecar](example-output/kdenlive-cues.ass) recorded these intervals:

| Cue | Delivered SRT | Saved editor ASS | Text |
|---|---|---|---|
| 1 | 0.200–1.100 s | 0.17–1.08 s | Synthetic test pattern. No source recording. |
| 2 | 1.400–2.800 s | 1.42–2.83 s | Tone pair changes; video continues after audio. |

The observed boundary differences reach 0.03 seconds. The project uses a frame-based timeline and the ASS file represents times to centiseconds; this readback is evidence of the saved values, not a universal rounding rule for other projects or versions. The original delivered MP4 and SRT remained byte-identical. The ASS is a readback artifact, not a replacement for that exact SRT delivery.

[The machine-readable record](example-output/native-editor-readback.json) contains only relevant profile, input-hash, option and cue observations. The native project is omitted because a machine-local project is unnecessary to use the delivered media. No export of a new video, project restart, cross-platform check, target uploader acceptance or color-fidelity assessment is claimed.

Kdenlive's [current subtitle manual](https://docs.kdenlive.org/en/effects_and_filters/subtitles.html) documents subtitle import/export and ASS storage. That rolling manual describes a newer version than the observed 24.12.3 build; the result above comes from the actual local run.
