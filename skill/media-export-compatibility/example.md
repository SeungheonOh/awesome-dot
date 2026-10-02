# A rejected export with odd dimensions and embedded captions

## Fictional request and contract

This is an original synthetic example, not a customer's recording or a real service test. Its moving test pattern is labeled “SYNTHETIC TEST PATTERN / No source recording.” The audio consists only of generated sine tones. Its two original captions describe the fixture, not speech.

The fictional request is: “ClipDrop Desk rejects this file under the supplied import contract. Make one compatible export and keep the whole picture, all video, both audio channels and the caption wording/times. Padding the right and bottom is fine. Put the captions in an SRT sidecar. Do everything locally.” ClipDrop Desk and its rejection are invented. The local mismatches below were measured from the generated file.

The [supplied contract](target-contract.json) asks for MP4 with one H.264 `yuv420p` video, even dimensions at most 640×360, square pixels, at most 30 fps, no rotation, one stereo AAC track at 48 kHz, no embedded subtitle stream, an SRT sidecar, initialization metadata before media, and at most 524,288 bytes. VFR is allowed. It also specifies preservation tolerances for this fixture. These are example inputs, not industry rules or a claim about a real uploader.

## What the source actually contains

The [source](example-output/source.mkv) is a 713,562-byte Matroska file:

| Content | Observed source | Chosen destination |
|---|---|---|
| Video stream 0 | FFV1, `yuv444p`, 319×179, square pixels, progressive, 12 fps, 36 frames, 3.000 s | H.264 `yuv420p`, 320×180; add one black column/right and one row/bottom |
| Audio stream 1 | PCM signed 16-bit, 44,100 Hz, 2 channels, 2.600 s decoded | AAC at 48,000 Hz; preserve channel identity and sequence |
| Subtitle stream 2 | English SubRip, two supplied cues ending at 2.800 s | [compatible.en.srt](example-output/compatible.en.srt), same text/times |
| Rotation | No rotation tag or display matrix reported; corner landmarks establish orientation | Preserve orientation; no rotation filter applied |
| Chapters/attachments/data | None reported | Nothing to move or exclude |
| Metadata | Synthetic source title; encoder-generated tags | Title retained; output encoder/handler/disposition metadata changes recorded by probe |

The source's two-channel PCM stream does not report a named channel layout in ffprobe. Its generator explicitly made stereo, and the decoded left/right tone identities are independently checked. For unknown user media, that missing field would require evidence or a decision rather than an automatic “stereo” assumption.

The subtitle stream-level duration is reported as 3.000 seconds while its last actual cue ends at 2.800 seconds. Cue extraction and comparison establish caption coverage; the container-level duration cannot substitute for checking the cues.

The source violates the fictional container, file-size, video-codec, pixel-format, even-dimension, audio-codec, sample-rate and embedded-subtitle requirements. Its named channel-layout requirement is unconfirmed by metadata alone. The problem is not just its `.mkv` suffix; remuxing unchanged streams cannot satisfy this contract.

## The deliberate changes

The completed [compatible.mp4](example-output/compatible.mp4) is 66,164 bytes. The original 319×179 picture remains at `(0,0)` in a 320×180 frame. Padding changes the overall display aspect from 319:179 to 16:9; it does not stretch or cut the content. Conversion to 4:2:0 and H.264 is lossy and can soften colored edges/text. The request accepts that consequence for this test pattern. It does not establish suitability for archival or color-critical work.

Audio is resampled and encoded, without selecting just one channel or mixing the two together. Video is mapped through its final frame. Audio ends earlier by design: adding `-shortest` would risk removing the video tail. No crop, seek, duration limit, new frame-rate request, speed change or silence-padding filter is applied.

The explicit mappings remove subtitles from the MP4 but not from the delivery. All their text/times are in the companion SRT. A player opening only the MP4 will not display them. The standalone SRT cannot carry the Matroska `eng` tag, so the filename and handoff identify English. Burn-in was not performed. A separate [local editor check](native-editor-check.md) imported and rendered this sidecar, with saved timing differences recorded explicitly.

The conversion command is reproduced below for this source only. Run in a new output directory with the source and caption output paths adjusted; the helper logs the portable command equivalents.

```sh
ffmpeg -hide_banner -v error -nostdin -n -i source.mkv \
  -map 0:v:0 -map 0:a:0 \
  -vf 'pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black,format=yuv420p' \
  -c:v libx264 -crf 18 -preset medium -fps_mode:v passthrough \
  -c:a aac -ar 48000 -b:a 128k -movflags +faststart compatible.mp4

ffmpeg -hide_banner -v error -nostdin -n -i source.mkv \
  -map 0:s:0 -c:s srt compatible.en.srt
```

Those encoder settings are one working choice for a tiny test pattern. Neither CRF nor the requested audio bitrate promises a universal size or quality result; the actual finished file is measured.

## What was checked

The [source probe](example-output/source-probe.json), [output probe](example-output/output-probe.json) and [evidence log](example-output/evidence.json) retain the measurements, versions, portable command equivalents and file identities.

| Check | Observed result | What it establishes |
|---|---|---|
| Contract fields | MP4, H.264 High level 1.2, `yuv420p`, 320×180, square pixels, 12 fps; stereo AAC-LC 48 kHz; two streams | This candidate meets the listed local stream/size constraints |
| Entire A/V decode | Completed with `-xerror`; 36 decoded video frames | FFmpeg could decode the full selected media |
| Timeline | 3.000 s video/container; all 36 source/output frame PTS paired, maximum difference 0.000333 s | Full frame count and timing preserved within the supplied 0.001 s tolerance |
| Video time base | Source `1/1000`; output `1/12288` | Different tick units explain why decimal timestamps need not be identical |
| Picture landmarks | Magenta/green/blue/white corner identities remain in the expected corners of every decoded frame | No detected rotation, mirror or loss of those landmarks |
| Audio timeline | 114,660 source samples/channel at 44.1 kHz = 2.600000 s; 124,928 decoded output samples/channel at 48 kHz = 2.602667 s | 2.667 ms decoded tail difference falls within the fixture's 22 ms tolerance |
| Audio container duration | MP4 audio stream reports 2.600000 s | Container duration and raw AAC decoded sample duration differ; neither replaces the other |
| Audio content | Early left/right tones about 440/880 Hz; middle and late tones about 660/990 Hz in source and output | Expected sequence and channel identity survive at the checked windows |
| Captions | Two cues; UTF-8 text and all timestamps match supplied SRT after newline decoding | Sidecar extraction preserved this plain caption payload |
| MP4 layout | Top-level boxes: `ftyp`, `moov`, `free`, `mdat`; no `moof` | This output has initialization metadata before media and is not fragmented |
| Source preservation | Source SHA-256 unchanged across conversion | Original bytes were not modified |

The audio windows are 0.4–0.6, 1.7–1.9 and 2.3–2.5 seconds. A positive zero-crossing count estimates these known pure-tone frequencies to approximately 5 Hz resolution over each 0.2-second window. They are content checks, not perceptual quality scores. The output's early left estimate is 435.05 Hz; this still identifies the intended 440 Hz tone within the six-Hz fixture threshold. RMS is checked only to reject an unexpectedly silent window. No listening test, loudness normalization, intelligibility or hearing-safety assessment occurred.

The [preview](example-output/preview.png) contains actual decoded frames 0, 18 and 35, left to right. The top row is the source (padded for the contact-sheet layout); the bottom row is the converted file. Separate gutters name each row, frame and sample time. The labels and corner landmarks were visually reviewed. The last source frame is at 2.917 s under its millisecond time base; the output is at approximately 2.916667 s. The preview does not show captions because they are intentionally external, and it cannot prove continuous playback or A/V synchronization.

## Reproduce without touching source media

```sh
python3 reproduce_example.py --out /tmp/media-compatibility-example-new
```

Use an output directory that does not exist. The helper needs Python 3 standard library, installed FFmpeg/ffprobe with FFV1, libx264, AAC, SubRip, lavfi, `drawtext`, `pad` and `tile`, plus an existing font. The default font used here is `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`; pass `--font` for another existing TrueType/OpenType font.

The helper generates its own source, converts it, extracts captions, probes and decodes both files, checks known markers/tones, then writes a preview and JSON evidence. It invokes no shell or network service and installs nothing. It temporarily copies the selected font into the new output directory and removes that copy after a successful run; a failed run can leave partial artifacts there. It refuses an existing output directory and passes `-n` to FFmpeg. It does not clean or overwrite previous runs.

Reproduction promises the declared behavior and checks, not identical media bytes. Font rendering, codec builds and container metadata can change hashes. The published hashes identify the particular delivered artifacts. The helper is intentionally limited to this fixture, not a validator for arbitrary media.

## Acceptance status

Local conformance: passed for the supplied fictional contract. Full FFmpeg A/V decode: passed. Representative visual review: performed. A separate local Kdenlive import and paused subtitle-rendering check was performed. Listening, continuous-playback quality and actual target import/upload remain unverified. No target service exists for this example, so actual acceptance cannot be claimed.
