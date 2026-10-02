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

Unrun: playback, acoustic review, synchronization, rendering in a media player, upload/import into a hosting platform, sound-event coverage, complete accessibility review and release approval. C03 remains an unresolved transcription alternative even when every mechanical check passes.
