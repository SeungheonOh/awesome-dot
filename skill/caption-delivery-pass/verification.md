# Example verification

This record covers the fictional transcript and delivered caption files only. There is no source media to play or hear.

## Command

From this skill's folder, using Python 3 and its standard library:

```sh
python3 check_example.py
```

Observed on 2026-10-02 with Python 3.12.14; exit status was 0. No dependency installation was needed.

```text
PASS: caption syntax subset, source text/order, format parity and source map
PASS: supplied layout limits; highest reading speed 11.95 code points/s
PASS: deliberately dropped negation rejected; C03 uncertainty remains intact
NOT CHECKED: media alignment, audio accuracy, player rendering or accessibility
```

The source fixture, both native caption files and the review sheet were also read directly. Local Markdown links were checked for existing targets. Syntax references were opened on the same date: the [W3C WebVTT draft](https://www.w3.org/TR/webvtt1/) and the [Library of Congress SRT description](https://www.loc.gov/preservation/digital/formats/fdd/fdd000569.shtml). These references support the format instructions; they do not verify the fictional track's timing.

## Scope

The checker reads both actual UTF-8 caption files, parses the plain-text syntax used in this example and compares them with the unchanged source fixture. It checks supplied intervals, sequence, source text after joining wrapped lines, cross-format equivalence, the source-clock map and the supplied layout limits. It also removes “not” in memory and requires that comparison to reject the altered cue. The fixture files are not changed by that negative check.

This is intentionally a small fixture check. It does not implement all SRT variants or all WebVTT features, validate arbitrary caption tracks, handle styling or certify a delivery platform. Its no-overlap check applies to this nonoverlapping fixture; real overlapping speech requires review rather than automatic rejection or rearrangement.

A separate guide-only fictional rehearsal produced partial SRT and WebVTT for supported segments while preserving withheld text. It kept a paragraph pending when the supplied interval and line limits could not support an invented timed split. That review also prompted an explicit clip-boundary rule: a segment crossing the chosen clip edge cannot be cropped to fit while retaining words whose location is unknown. This was an instruction and output review, not an audio or player test.

## Independent format parser

The installed `ffprobe` 7.1.5 also read each delivered file as a subtitle stream: `subrip` for the SRT file and `webvtt` for the VTT file. Each yielded seven packets. Their parsed start times and durations matched all seven supplied segment intervals using exact decimal-to-millisecond comparisons.

With an existing compatible FFmpeg installation, inspect the same packet fields from this folder:

```sh
ffprobe -v error -show_packets -show_entries packet=pts_time,duration_time -of json captions.srt
ffprobe -v error -show_packets -show_entries packet=pts_time,duration_time -of json captions.vtt
```

The [official ffprobe documentation](https://ffmpeg.org/ffprobe.html) describes these inspection options. This provides an additional format-parser check; it does not check visible wrapping, audio or media synchronization. A browser-rendering attempt did not start successfully, so no browser rendering result is claimed.

## Synthetic render check

FFmpeg 7.1.5 with its libass subtitle filter actually rendered each delivered caption format over an original 960×540 blank background at 10 frames per second. The background is visibly labeled “Synthetic background only. No source audio or video.” Both complete 36-second renders yielded the same 360 decoded frames; in this run their encoded bytes also matched. No audio stream exists. The [MP4](caption-render.mp4) is one of those identical outputs, and the [preview](render-preview.png) contains samples at 0, 3, 7, 12, 16, 21, 26 and 31 seconds.

The preview was inspected for all seven cues, including the negation in C02, unresolved date in C03, Unicode names and French text. No clipping or lost characters was seen at the rendered size. The [machine-readable check](render-check.json) binds the input and output bytes and records the observed stream properties. This is a consumer rendering result, not an audio alignment test or a claim about other players.

To reproduce with an existing compatible FFmpeg build and a locally available DejaVu Sans font, supply the path to its `DejaVuSans.ttf` file and a new output directory:

```sh
python3 render_example.py --font /path/to/DejaVuSans.ttf --output render-check-new
```

The [renderer](render_example.py) first runs the existing source/caption check, makes its own temporary labeled background, renders both files, compares every decoded frame and writes the MP4, preview and report. It refuses an existing output directory and leaves the source files unchanged. No software or font is downloaded. The supplied font draws the background labels and is exposed to libass through the [subtitle filter's font-directory option](https://ffmpeg.org/ffmpeg-filters.html#subtitles). Rendering behavior or bytes may differ with another FFmpeg/libass/font environment, so inspect the new preview rather than treating a matching command as proof.

The portable helper was run into a second fresh directory in the recorded environment and reproduced both committed binary files byte for byte. A subsequent attempt to reuse that directory was rejected, with its existing files unchanged. Metadata inspection found only ordinary container/codec fields, no audio stream and no private source paths or account details.

Unrun: source-media playback, acoustic review, source synchronization, interactive-player or hosting-platform import/rendering, sound-event coverage, complete accessibility review and release approval. C03 remains an unresolved transcription alternative even when every mechanical check passes.
