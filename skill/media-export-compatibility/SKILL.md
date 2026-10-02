---
name: media-export-compatibility
description: "Diagnose a rejected media export, convert authorized local media to a documented target specification, and deliver the usable file with evidence that its content and timing survived."
---

# Make a rejected media file usable

Use this when a video or audio file will not import, upload or play in the intended tool and the user wants a compatible export. Deliver an actual converted file, any required caption sidecars, and a short before/after record. A renamed extension or a successful encoder exit is not sufficient.

This workflow handles container and stream compatibility. Authoring transcripts, correcting caption wording and establishing speech synchronization are separate tasks. Preserve existing captions here and report unsupported features rather than silently rewriting them.

The [worked example](example.md) follows a clearly fictional target contract and includes a labeled original synthetic source, an actual MP4 and an extracted SRT. No real service was contacted. Use it to understand the decisions, not as a preset for every uploader.

## Establish the mismatch

Get the exact source version, target tool and import/upload path, reported error, and useful constraints. “It wants an MP4” does not settle which codecs, dimensions or audio layout it accepts. Inspect the actual file before attributing the rejection to its extension.

Find the target's current official import/export documentation for that product and workflow. Record the URL, access date, relevant requirement and ambiguity. Distinguish a hard acceptance limit from a recommendation. If the user supplies a contract, preserve it and identify its source. Do not invent a provider requirement from a general compatibility recipe. While constraints remain unknown, inspect the source and propose a candidate export with those unknowns visible.

Relevant constraints can include container, video/audio codecs, profile/level, pixel format/bit depth, dimensions, frame rate, interlacing, duration, file size, channel layout, sample rate and subtitle support. Add color/HDR/alpha or stream-count requirements when they matter to this source. Avoid filling a matrix with irrelevant fields merely to complete it.

Separate preparation from submission. A local conversion does not authorize sending private media to an online converter, cloud transcription service, support portal or target account. Use authorized local files and installed tools. If later upload is requested, confirm that the destination, exact file/version and data to be transmitted fall within the user's authorization. Do not use an unrelated personal clip as a test upload.

## Inspect all the content, not just the default track

Create a new output directory. Preserve the original bytes and record the source filename, size and a checksum before transformation. Review helper code for downloads, installation, overwrites, source deletion and network outputs before running it. Check the installed tools and available encoders/filters; do not assume another machine has the same build.

For an installed FFmpeg toolchain, start with:

```sh
ffmpeg -version
ffprobe -version
ffprobe -v error -show_format -show_streams -show_chapters -of json "source-file"
```

Keep the machine-readable probe with the result. FFprobe can expose container, stream and chapter information in JSON; missing fields are unknown, not zero or proof of absence. See the [official ffprobe options](https://ffmpeg.org/ffprobe.html#Main-options).

Inspect the features that could be lost or misinterpreted:

- Container versus each codec; stream index, language, title and disposition; alternate audio, subtitle, attachment, data and cover-art streams
- Stored width/height, sample and display aspect ratio, rotation/display-matrix side data, pixel format, color/HDR metadata, and field order
- Stream start times, duration evidence, frame rate and time base; use frame/packet inspection if the fields conflict, VFR matters, or the source has gaps
- Audio sample rate, channel count and named layout; a two-channel count alone does not establish which channel is which
- Caption type and role: selectable text, image subtitles, embedded captions or already burned into the picture; fonts/styling and forced/default flags when relevant

Compare actual playback orientation with stored geometry when inspection is available. A shallow probe can miss in-band captions, changing geometry or later corruption; inspect decoded frames/packets when those features or failure symptoms matter. Record the evidence reviewed. A thumbnail, metadata read or amplitude plot does not establish that the whole clip is intact, intelligible or synchronized.

Write a stream disposition list before conversion. Every original stream and meaningful feature should have a destination: copied, transcoded, retained as a sidecar/original, or deliberately excluded with the user's accepted reason. If preserving an unsupported feature is unresolved, say the candidate is incomplete. Keeping the source available does not make an unexplained missing track acceptable in the deliverable.

## Choose the least destructive sufficient change

Use the constraints and source inspection to choose a change; do not default to re-encoding everything.

| Finding | Useful decision |
|---|---|
| Container alone is incompatible, and every required stream is supported by the target container | Remux the selected streams and verify the result; preserve codec data when possible |
| One codec is unsupported | Transcode that stream; copy other streams if their target support and timing permit |
| Required 4:2:0 output cannot encode an odd-sized frame | Prefer an explicitly accepted small pad or a fitted rescale; never silently crop an edge |
| Display rotation conflicts with target behavior | Choose either supported metadata or physical orientation; establish expected displayed geometry before encoding |
| Audio layout exceeds the target | Preserve channels when supported; otherwise obtain the intended channel selection/downmix and check actual channel content |
| Embedded captions are unsupported | Deliver a supported sidecar if allowed; preserve its text/timing and explain that the video alone will not display it |
| Size exceeds a hard limit | Budget and encode to the limit, then measure actual bytes; discuss quality/resolution tradeoffs if the first sufficient candidate is too large |

Streamcopy avoids decode/re-encode, but cannot apply frame filters and is constrained by the output container. FFmpeg's explicit `-map` selections control which streams go into each output. See [streamcopy](https://ffmpeg.org/ffmpeg.html#Streamcopy) and [stream selection](https://ffmpeg.org/ffmpeg.html#Stream-selection). Choose actual inspected indices; an example's `0:v:0` and `0:a:0` are not a rule for a multitrack recording.

Resolve content-changing decisions specifically:

- **Picture:** Record padding dimensions, position and color, or the agreed scale. Preserve the complete visible source rectangle unless cropping is requested. Treat pixel-format conversion, HDR-to-SDR tone mapping and alpha removal as transformations with visible consequences. A generic `yuv420p` export is not an HDR/alpha preservation recipe.
- **Orientation:** FFmpeg autorotation is normally enabled for transcoding. Account for that before adding a transpose filter; otherwise a second rotation can undo the fix. Inspect the resulting pixels and residual rotation metadata. See [video options](https://ffmpeg.org/ffmpeg.html#Video-Options). A square-pixel setting alone cannot repair a non-square-pixel source without the corresponding geometry decision.
- **Time:** Preserve the requested full clip and relative A/V/subtitle alignment. Do not add `-shortest`, `-t`, `-ss`, a new frame rate or speed filters as housekeeping. In particular, a shorter audio track must not silently cut off later video or captions. If a new constant frame rate is required, disclose duplicated/dropped frames and verify the resulting timeline.
- **Sound:** Distinguish resampling, channel remapping and mixing. Do not discard one stereo channel or invent a universal downmix. Preserve descriptions, alternate languages and isolated microphone tracks according to the agreed disposition. Avoid claims about loudness, hearing safety, intelligibility or perceptual quality from metadata alone.
- **Captions:** Keep text captions selectable when the target supports that delivery. Image subtitles cannot be made into faithful text merely by changing their extension; styled formats may lose layout in SRT. Burning captions into pixels changes the image and removes selectability. Request that choice when it is not already authorized. Preserve the original and surface unresolved styling, position or timing losses.

Document the chosen command and its effects. Run with non-overwrite behavior into the new directory. Keep the source available until the user can use the result. If a candidate fails, retain the useful error, change the implicated setting and use a fresh candidate filename; do not accumulate arbitrary alternate exports.

## Reconcile the result against both source and contract

Probe the new file, then decode the full selected media streams and inspect the output. For example, after confirming there is one intended video/audio pair:

```sh
ffprobe -v error -show_format -show_streams -show_chapters -of json "compatible.mp4"
ffmpeg -v error -xerror -i "compatible.mp4" -map 0:v:0 -map 0:a:0 -f null -
```

Adapt the mappings for the actual file; the null output does not test subtitles or a target uploader. Check the caption delivery separately.

Use evidence appropriate to each claim:

1. **Conformance:** Check actual container, stream counts, codec details, pixel format, size, geometry, audio fields and every documented target requirement. Inspect initialization/index placement if the contract requires it. A `+faststart` command is intent; the example also inspects its MP4 box order. The [MP4 muxer documentation](https://ffmpeg.org/ffmpeg-formats.html#mov_002c-mp4_002c-ismv) describes that option.
2. **Picture and time:** Reconcile duration, start offsets, frame/packet timing when needed, and intended orientation. Inspect beginning, ending and relevant interior frames, plus transformed borders, captions and fine text. If the source is VFR, compare actual timestamps rather than treating an average as its complete cadence. Explain small container time-base or codec-padding differences instead of forcing identical decimal values.
3. **Sound content:** Confirm the expected content on each retained channel, near the beginning/end and at transitions. Listen where the available capability permits. For a known synthetic fixture, decoded signal evidence can test channel identity and sequence; it does not constitute a listening test of speech or music. Presence, nonzero duration and a moving waveform alone do not prove content survived.
4. **Captions and other content:** Compare all cues' text, order and intervals to the source track. Check sidecar association and actual display in the intended player when available. Reconcile languages, forced/default behavior, attachments and chapters with the planned dispositions. Never count an extracted sidecar as embedded captions in the MP4.
5. **Preservation and delivery:** Recheck the original checksum. Verify that output files are nonempty and openable and that the handoff names the exact final candidate. Record unreviewed intervals, unsupported features and subjective checks not performed.

A source that cannot decode fully may need recovery rather than ordinary export. Preserve the failure interval and original, and avoid calling a partial result the complete clip. Stop once one candidate meets the requested contract and content checks, or the next required check needs unavailable access or a content decision.

## Hand off a usable file

Lead with the actual output and any companion files needed for use. Include a compact record of:

- Source identity/checksum, target requirement source/date and exact output paths or links
- Why the source did not meet the stated contract, separating measured mismatches from unresolved requirements or user-reported errors
- Changed geometry, encoding, audio, timing, metadata and track dispositions; any accepted quality or feature loss
- Before/after measurements and the checks actually performed, with tool versions
- Local conformance, local playback review and target-service acceptance as separate statuses

If the target was not tried, say “Matches the documented local requirements; target import/upload is untested.” If an authorized target attempt succeeds, record the actual tool/version or destination, selected file and observed success; an HTTP response or completed upload may still precede a processing failure. Do not claim the target accepted a file solely because FFmpeg decoded it.

## Reproduce the worked example

Read [example.md](example.md) for the fictional request, transformation and concrete evidence, and [verification.md](verification.md) for source/tool claims and limits. The [helper](reproduce_example.py) generates only its own synthetic media, writes to a new directory and uses the already-installed FFmpeg/ffprobe. It is not a general-purpose converter or an uploader.

```sh
python3 reproduce_example.py --out /tmp/media-compatibility-example-new
```

The output directory must not exist. Supply `--font /path/to/an/existing/font.ttf` when the documented default font is absent. No dependency installation or service access is part of this example.
