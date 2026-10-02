# Sources, execution and delivery limits

## Provenance

The example source was generated locally for this skill from FFmpeg's synthetic `testsrc` and `aevalsrc` filters, four deliberately colored corner markers, two fixture labels, and the original [source-captions.srt](source-captions.srt). No downloaded clip, real person, voice, music, account, credential or user recording was used. The fictional [target contract](target-contract.json) is an input invented for this example; it is not attributed to a real service.

All delivered binaries are below 2 MiB individually. The source, converted MP4 and contact sheet are original synthetic example artifacts; no font binary is included. The SRT is UTF-8 text, not burned into the video.

## Primary references checked 2026-10-02 UTC

| Primary source | Limited claims used here |
|---|---|
| [FFmpeg command documentation](https://ffmpeg.org/ffmpeg.html) | Explicit mapping; streamcopy versus transcode; autorotation; timestamp/frame-rate options; `-shortest` semantics |
| [FFprobe documentation](https://ffmpeg.org/ffprobe.html) | JSON output and container, stream, chapter and frame inspection |
| [FFmpeg filter documentation](https://ffmpeg.org/ffmpeg-filters.html) | Padding, synthetic sources, text labels and contact-sheet filters |
| [FFmpeg format documentation](https://ffmpeg.org/ffmpeg-formats.html) | MP4 faststart and fragmentation behavior |

These online pages describe the current development documentation and are not a frozen manual for the installed release. The relevant installed `pad` filter and MP4 muxer help were also inspected. The recorded command equivalents in [evidence.json](example-output/evidence.json) correspond to executions against the installed versions below. No real uploader's acceptance limits are claimed.

## Observed execution

Execution date: 2026-10-02 UTC. Environment: Linux x86-64; installed `/usr/bin/ffmpeg` and `/usr/bin/ffprobe`, both `7.1.5-0+deb13u1`, built with GCC 14 (Debian 14.2.0-19). No installation occurred. The invoked encoders included FFV1, libx264, AAC and PCM; the installed default font was `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`.

The source and conversion were executed locally. The final contact sheet renders the existing source and converted media with separate source/output and timestamp gutters. A full helper reproduction in another new directory passed all checks and produced the same converted MP4, SRT and preview hashes. The delivered files are:

| Delivered file | Bytes | SHA-256 |
|---|---:|---|
| [source.mkv](example-output/source.mkv) | 713562 | `85f527821aae6d657b822f2df4be245996115d456317eb8b79f96f88ba35abf0` |
| [compatible.mp4](example-output/compatible.mp4) | 66164 | `fe32fb2c81024b01c84cdb94563f4e352131c76c0deaa21930a3b27a867366e2` |
| [compatible.en.srt](example-output/compatible.en.srt) | 159 | `6a4eae4fec7807a663db4ab5b4b561860b50a8859000e89914f657832553c85c` |
| [preview.png](example-output/preview.png) | 85101 | `124062533a58e94465bf40b9c9639ae8a53205b83dc46c60042296e6023c7d25` |

The main observations and their meaning are in the [worked example](example.md). Supporting checks performed:

- Python syntax parsing, frontmatter and local-file link checks passed
- An attempted rerun into the existing output directory failed at directory creation. All existing output file hashes remained unchanged
- A private negative control swapped the source's left/right audio channels. The tone-content check rejected it at 0.4 seconds: approximately 880.10 Hz in the left channel where 440 Hz was expected. That control is not included as a deliverable
- The source checksum was unchanged after conversion, extraction, probing and decoding
- The final contact sheet was opened and visually reviewed: the two synthetic labels, full-frame extent and expected corner identities are visible in corresponding source/output frames. Separate gutters identify each row, frame and timestamp without covering image content. This preview-only revision left both media-file hashes unchanged
- The full selected output audio/video decoded with `-xerror`; stream constraints, frame count and PTS comparison, tone sequence, sidecar payload, output size and MP4 box order passed the recorded checks

The no-overwrite check establishes the helper's output-directory behavior. The swapped-channel control establishes that its content check can reject a relevant loss that stream metadata alone would miss. Neither is a general codec or media-quality certification.

## Portable evidence paths

The saved probe reports localize only `format.filename` to the delivered filename. Command records use portable output-relative paths and a temporary font-copy name; the separate final-preview destination is localized to `preview.png`. They are reproducible command equivalents, not verbatim logs of private working directories. Stream measurements, timing observations and delivered artifact hashes are unchanged. The helper applies the same localization to new reports and records the font filename and digest without its absolute path.

## Boundaries

The helper is a small, fixed-fixture reproduction, not a general conversion library. It does not handle arbitrary uploads, URLs, custom codecs or every subtitle representation. Its assertions deliberately target known properties of this example. Use ordinary Python execution; `-O` is rejected because it would disable assertions. If any step fails, the new output directory remains for inspection, and a later attempt needs another new directory.

The demonstration exercises odd dimensions, a shorter audio track, changed audio sampling/encoding, a subtitle sidecar and container time-base differences. It does not exercise nonzero rotation metadata, multichannel downmixing, HDR, alpha, interlacing, variable-frame-rate source material, image subtitles, styled subtitles, multiple languages or corrupt source recovery. The main instructions identify the decisions needed for such inputs, but this run supplies no empirical coverage for them.

Corner checks and selected frames do not compare every original pixel. The known-tone checks do not prove the subjective quality of speech or music and are not a listening test. The source and output contain 2.6 seconds of intended audio followed by roughly 0.4 seconds of video only; the tiny raw AAC decoded tail difference is reported rather than hidden. The automated helper extracts and compares captions. The separate [local editor check](native-editor-check.md) also imported and rendered them, and recorded changed saved boundaries. Continuous-playback quality and A/V synchronization were not subjectively reviewed.

No accounts, remote services, online converters or uploaders were used. The separate editor check used only the delivered synthetic files locally. The MP4 passes the local fictional contract. Actual target-service acceptance remains untested, and no publication or user-media transmission is implied.

## Independent conversion review

An independent inspected reproduction retained the exact delivered MP4, SRT and preview bytes. Additional decoded-content comparisons checked frame order, the audio beginning, tone transition and ending, plus the encoder priming and small decoded tail. Swapped channels were rejected. Muting only the first 0.3 seconds escaped the helper’s three sampled tone windows, which demonstrates their coverage limit; the actual delivered prefix passed the independent check. The relative-font case now records the correct filename and digest, and portable reports retain the measured values without private execution paths.

A separate guide-only multitrack remux case planned to retain both supported language streams and a supplied 0.4-second offset. It was a plan-only check, not another encoded artifact or service test.
