#!/usr/bin/env python3
"""Check the bundled plain-text fixture; no media or external dependencies."""

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def millis(value, separator):
    pattern = rf"(\d{{2}}):([0-5]\d):([0-5]\d){re.escape(separator)}(\d{{3}})"
    match = re.fullmatch(pattern, value)
    require(match is not None, f"Invalid timestamp: {value!r}")
    hours, minutes, seconds, fraction = map(int, match.groups())
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + fraction


def stamp(value):
    seconds, fraction = divmod(value, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{fraction:03}"


def read_cues(filename, vtt=False):
    text = (ROOT / filename).read_text(encoding="utf-8")
    require(text.endswith("\n"), f"Missing final newline: {filename}")
    blocks = text.strip().split("\n\n")
    if vtt:
        require(blocks.pop(0) == "WEBVTT", "Missing WebVTT header")
    cues = []
    for block in blocks:
        lines = block.splitlines()
        require(len(lines) >= 3, f"Incomplete cue: {block!r}")
        require(lines[1].count(" --> ") == 1, "Invalid timing line")
        start, end = lines[1].split(" --> ")
        cues.append((lines[0], millis(start, "." if vtt else ","),
                     millis(end, "." if vtt else ","), lines[2:]))
    return cues


def verify(cues, source, vtt=False):
    segments = source["segments"]
    limits = source["constraints"]
    require(len(cues) == len(segments), "Missing or extra cue")
    previous_end = 0
    readings = []
    for ordinal, (cue, segment) in enumerate(zip(cues, segments), 1):
        identity, start, end, lines = cue
        expected_id = segment["cue_id"] if vtt else str(ordinal)
        require(identity == expected_id, f"Cue identifier/order mismatch: {identity}")
        require((start, end) == (segment["start_ms"], segment["end_ms"]),
                f"Supplied timing changed: {identity}")
        require(0 <= start < end <= source["clip_duration_ms"],
                f"Invalid interval: {identity}")
        require(start >= previous_end, f"Unexpected fixture overlap: {identity}")
        previous_end = end
        expected_text = f'{segment["speaker"]}: {segment["text"]}'
        require(" ".join(lines) == expected_text, f"Source wording changed: {identity}")
        require(len(lines) <= limits["max_lines"], f"Too many lines: {identity}")
        require(all(len(line) <= limits["max_line_codepoints"] for line in lines),
                f"Line too long: {identity}")
        cps = sum(map(len, lines)) / ((end - start) / 1000)
        require(cps <= limits["target_cps"], f"Reading-speed flag: {identity}")
        readings.append(cps)
    return readings


def main():
    source = json.loads((ROOT / "source-transcript.json").read_text(encoding="utf-8"))
    srt, vtt = read_cues("captions.srt"), read_cues("captions.vtt", vtt=True)
    readings = verify(srt, source)
    verify(vtt, source, vtt=True)
    require([cue[1:] for cue in srt] == [cue[1:] for cue in vtt], "Formats differ")
    review = (ROOT / "example.md").read_text(encoding="utf-8")
    for segment in source["segments"]:
        offset = source["original_offset_ms"]
        expected_row = (f'| {segment["cue_id"]} | {segment["id"]} | '
                        f'{stamp(segment["start_ms"])}–{stamp(segment["end_ms"])} | '
                        f'{stamp(segment["start_ms"] + offset)}–'
                        f'{stamp(segment["end_ms"] + offset)} |')
        require(expected_row in review, f'Missing/incorrect time map: {segment["cue_id"]}')
    require("00:02:17.250–00:02:53.250" in review, "Missing excerpt boundary map")
    require(source["original_offset_ms"] + source["clip_duration_ms"] == 173250,
            "Incorrect excerpt end")

    # Exercise the realistic dropped-negation failure without modifying a file.
    faulty = [(identity, start, end, [line.replace("Do not crop", "Do crop") for line in lines])
              for identity, start, end, lines in srt]
    try:
        verify(faulty, source)
    except ValueError as error:
        require(str(error) == "Source wording changed: 2", "Unexpected rejection")
    else:
        raise ValueError("Dropped negation was not rejected")
    print("PASS: caption syntax subset, source text/order, format parity and source map")
    print(f"PASS: supplied layout limits; highest reading speed {max(readings):.2f} code points/s")
    print("PASS: deliberately dropped negation rejected; C03 uncertainty remains intact")
    print("NOT CHECKED: media alignment, audio accuracy, player rendering or accessibility")


if __name__ == "__main__":
    main()
