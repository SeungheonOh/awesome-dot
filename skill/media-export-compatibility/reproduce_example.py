#!/usr/bin/env python3
"""Reproduce only the original synthetic example; not a general media converter.

Uses Python standard library and already-installed ffmpeg/ffprobe. Creates one new
directory, writes only there, invokes no shell, and does not accept source URLs or
user media. The optional font is read only. Read example.md before executing.
"""
import argparse
import array
import hashlib
import json
import math
import pathlib
import shutil
import struct
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
COMMANDS = []


def run(args):
    COMMANDS.append([str(arg) for arg in args])
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def ff(*args):
    return run(["ffmpeg", "-hide_banner", "-v", "error", "-nostdin", "-n", *args])


def probe(path, *args):
    return json.loads(run(["ffprobe", "-v", "error", "-of", "json", *args, path]))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def portable_probe(info):
    """Preserve measured fields; localize only the known input file locator."""
    result = dict(info)
    result["format"] = dict(info["format"])
    result["format"]["filename"] = pathlib.Path(info["format"]["filename"]).name
    result["path_note"] = "format.filename is relative to this report's directory"
    return result


def portable_commands(commands, output):
    prefix = str(output) + "/"
    return [[arg[len(prefix):] if arg.startswith(prefix) else arg for arg in command]
            for command in commands]


def stream(info, kind):
    return next(s for s in info["streams"] if s["codec_type"] == kind)


def rotations(s):
    return [float(d["rotation"]) for d in s.get("side_data_list", []) if "rotation" in d]


def rate(value):
    numerator, denominator = value.split("/")
    return float(numerator) / float(denominator)


def contract_failures(path, info, contract):
    """Inspect actual properties against this example's supplied constraints."""
    failures = []
    v, a = stream(info, "video"), stream(info, "audio")
    vc, ac = contract["video"], contract["audio"]
    conditions = {
        "MP4 container": "mp4" in info["format"]["format_name"].split(","),
        "file size": path.stat().st_size <= contract["max_bytes"],
        "one video": sum(s["codec_type"] == "video" for s in info["streams"]) == vc["count"],
        "one audio": sum(s["codec_type"] == "audio" for s in info["streams"]) == ac["count"],
        "video codec": v["codec_name"] == vc["codec"],
        "pixel format": v["pix_fmt"] == vc["pixel_format"],
        "even dimensions": v["width"] % 2 == v["height"] % 2 == 0,
        "dimension bounds": v["width"] <= vc["max_width"] and v["height"] <= vc["max_height"],
        "square pixels": v["sample_aspect_ratio"] == vc["sample_aspect_ratio"],
        "frame rate": rate(v["avg_frame_rate"]) <= vc["max_frame_rate"],
        "rotation": all(r == vc["rotation_degrees"] for r in rotations(v)) and
                    float(v.get("tags", {}).get("rotate", 0)) == vc["rotation_degrees"],
        "audio codec": a["codec_name"] == ac["codec"],
        "sample rate": int(a["sample_rate"]) == ac["sample_rate"],
        "channel count": a["channels"] == ac["channels"],
        "channel layout" if a.get("channel_layout") else "channel layout unreported":
            a.get("channel_layout") == ac["channel_layout"],
        "no embedded subtitle": sum(s["codec_type"] == "subtitle" for s in info["streams"]) == 0,
    }
    for label, passed in conditions.items():
        if not passed:
            failures.append(label)
    return failures


def frame_times(path):
    frames = probe(path, "-select_streams", "v:0", "-show_frames",
                   "-show_entries", "frame=best_effort_timestamp_time")["frames"]
    return [float(f["best_effort_timestamp_time"]) for f in frames]


def inspect_markers(path, width, height):
    # Full decode; inspect known spatial landmarks in every decoded frame.
    rgb = ff("-i", path, "-map", "0:v:0", "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1")
    stride = width * height * 3
    assert len(rgb) % stride == 0, "Incomplete decoded video frame"
    points = [(6, 6), (312, 6), (6, 172), (312, 172)]
    checks = [lambda r, g, b: r > 180 and b > 180 and g < 65,
              lambda r, g, b: g > 85 and r < 65 and b < 65,
              lambda r, g, b: b > 180 and r < 65 and g < 65,
              lambda r, g, b: min(r, g, b) > 185]
    for frame_offset in range(0, len(rgb), stride):
        for (x, y), check in zip(points, checks):
            p = frame_offset + (y * width + x) * 3
            assert check(*rgb[p:p+3]), "A corner marker moved or lost its color identity"
    return {"decoded_frames": len(rgb) // stride, "corner_markers_checked_per_frame": 4,
            "result": "magenta / green / blue / white remain in their original corners"}


def inspect_audio(path, sample_rate):
    pcm = ff("-i", path, "-map", "0:a:0", "-c:a", "pcm_s16le", "-f", "s16le", "pipe:1")
    samples = array.array("h", pcm)
    if sys.byteorder != "little":
        samples.byteswap()
    assert len(samples) % 2 == 0, "Incomplete stereo sample"
    observations = []
    # Frequency estimates establish sequence and left/right identity in this
    # known pure-tone fixture. They are not a quality or listening score.
    for start, expected in [(0.4, (440, 880)), (1.7, (660, 990)), (2.3, (660, 990))]:
        end = start + 0.2
        values = []
        for channel, frequency in enumerate(expected):
            window = samples[round(start * sample_rate) * 2 + channel:round(end * sample_rate) * 2:2]
            upward = sum(a <= 0 < b for a, b in zip(window, window[1:]))
            measured = upward / ((len(window) - 1) / sample_rate)
            rms = math.sqrt(sum(x*x for x in window) / len(window))
            assert abs(measured - frequency) < 6, (start, channel, measured, frequency)
            assert rms > 500, "Tone window is unexpectedly silent"
            values.append(round(measured, 2))
        observations.append({"window_seconds": [start, end], "expected_hz_L_R": expected,
                             "estimated_hz_L_R": values})
    return {"decoded_samples_per_channel": len(samples) // 2,
            "decoded_duration_seconds": len(samples) / 2 / sample_rate,
            "tone_windows": observations, "listening_test": "not performed"}


def mp4_boxes(path):
    data = path.read_bytes()
    boxes, offset = [], 0
    while offset < len(data):
        length, kind = struct.unpack_from(">I4s", data, offset)
        if length == 1:
            length = struct.unpack_from(">Q", data, offset + 8)[0]
        if length == 0:
            length = len(data) - offset
        assert length >= 8 and offset + length <= len(data), "Invalid top-level MP4 box"
        boxes.append(kind.decode("ascii"))
        offset += length
    return boxes


def make_preview(source, converted, destination, font, source_times, output_times):
    # Put each label in a separate 28-pixel gutter; never cover the picture.
    def labels(name, times, decimals):
        result = ""
        for column, frame in enumerate((0, 18, 35)):
            label = f"{name} | frame {frame} | {times[frame]:.{decimals}f} s"
            result += (f",drawtext=fontfile='{font}':text='{label}':"
                       f"fontsize=13:fontcolor=white:x={column * 320 + 8}:y=7")
        return result
    selected = "select='eq(n,0)+eq(n,18)+eq(n,35)'"
    graph = (f"[0:v]{selected},pad=320:180:0:0:black,tile=3x1,"
             "pad=iw:ih+28:0:28:color=0x202020" + labels("Source", source_times, 3) + "[top];"
             f"[1:v]{selected},tile=3x1,pad=iw:ih+28:0:28:color=0x202020" +
             labels("Converted", output_times, 6) + "[bottom];[top][bottom]vstack[preview]")
    ff("-i", source, "-i", converted, "-filter_complex", graph,
       "-map", "[preview]", "-frames:v", "1", destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=pathlib.Path, required=True, help="New directory; must not exist")
    parser.add_argument("--font", type=pathlib.Path,
                        default=pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    args = parser.parse_args()
    if not __debug__:
        parser.error("Run without Python -O; this example uses assertions for verification")
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            parser.error(f"{tool} is not installed; this helper never installs software")
    if not args.font.is_file():
        parser.error("Supply --font pointing to an existing local TrueType/OpenType font")
    # Restrict font path grammar because the filename is embedded in a filter.
    if any(c in str(args.font.resolve()) for c in ":'\\,[];"):
        parser.error("Use a font path without FFmpeg filter delimiter characters")
    font_source = args.font.resolve()
    font_record = {"filename": font_source.name, "sha256": digest(font_source)}
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(font_source, output / "label-font.ttf")
    # Font is a temporary local helper input, removed at successful completion;
    # it is never included in the delivered artifacts.
    contract = json.loads((HERE / "target-contract.json").read_text(encoding="utf-8"))
    shutil.copyfile(HERE / "source-captions.srt", output / "source-captions.srt")
    source, converted = output / "source.mkv", output / "compatible.mp4"
    versions = {t: run([t, "-version"]).decode().splitlines()[0] for t in ("ffmpeg", "ffprobe")}
    # Relative font reference avoids platform filter escaping. All generated
    # paths remain absolute; only this process's working directory changes.
    import os
    os.chdir(output)
    video = ("testsrc=size=319x179:rate=12:duration=3,format=yuv444p,"
             "drawbox=x=0:y=0:w=14:h=14:color=magenta:t=fill,"
             "drawbox=x=305:y=0:w=14:h=14:color=green:t=fill,"
             "drawbox=x=0:y=165:w=14:h=14:color=blue:t=fill,"
             "drawbox=x=305:y=165:w=14:h=14:color=white:t=fill,"
             "drawtext=fontfile=label-font.ttf:text='SYNTHETIC TEST PATTERN':"
             "fontsize=17:fontcolor=white:box=1:boxcolor=black:x=22:y=70,"
             "drawtext=fontfile=label-font.ttf:text='No source recording':"
             "fontsize=14:fontcolor=white:box=1:boxcolor=black:x=80:y=95")
    audio = ("aevalsrc='0.1*sin(2*PI*if(lt(t,1.3),440,660)*t)|"
             "0.1*sin(2*PI*if(lt(t,1.3),880,990)*t)':s=44100:d=2.6:c=stereo")
    ff("-f", "lavfi", "-i", video, "-f", "lavfi", "-i", audio,
       "-i", output / "source-captions.srt", "-map", "0:v:0", "-map", "1:a:0", "-map", "2:s:0",
       "-c:v", "ffv1", "-c:a", "pcm_s16le", "-c:s", "srt",
       "-metadata", "title=Original synthetic compatibility fixture",
       "-metadata:s:s:0", "language=eng", source)
    source_hash = digest(source)
    source_probe = probe(source, "-show_format", "-show_streams", "-show_chapters")
    save(output / "source-probe.json", portable_probe(source_probe))
    ff("-i", source, "-map", "0:v:0", "-map", "0:a:0",
       "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:black,format=yuv420p",
       "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-fps_mode:v", "passthrough",
       "-c:a", "aac", "-ar", "48000", "-b:a", "128k", "-movflags", "+faststart", converted)
    sidecar = output / "compatible.en.srt"
    ff("-i", source, "-map", "0:s:0", "-c:s", "srt", sidecar)
    output_probe = probe(converted, "-show_format", "-show_streams", "-show_chapters")
    save(output / "output-probe.json", portable_probe(output_probe))
    assert digest(source) == source_hash, "Source changed"
    # SRT extraction may change container representation; this plain fixture's
    # UTF-8 cue payload and times are preserved byte-for-byte after CRLF handling.
    assert sidecar.read_text(encoding="utf-8") == (HERE / "source-captions.srt").read_text(encoding="utf-8")
    failures_before = contract_failures(source, source_probe, contract)
    failures_after = contract_failures(converted, output_probe, contract)
    assert failures_before, "Fixture must demonstrate an actual local contract mismatch"
    assert not failures_after, failures_after
    before_times, after_times = frame_times(source), frame_times(converted)
    assert len(before_times) == len(after_times) == contract["preservation"]["video_frame_count"]
    delta = max(abs(a-b) for a, b in zip(before_times, after_times))
    assert delta <= contract["preservation"]["video_timestamp_tolerance_seconds"]
    assert abs(float(stream(output_probe, "video")["duration"]) - 3) <= 0.001
    boxes = mp4_boxes(converted)
    assert boxes.index("moov") < boxes.index("mdat") and "moof" not in boxes
    visual = {"source": inspect_markers(source, 319, 179),
              "output": inspect_markers(converted, 320, 180)}
    sound = {"source": inspect_audio(source, 44100), "output": inspect_audio(converted, 48000)}
    audio_delta = sound["output"]["decoded_duration_seconds"] - sound["source"]["decoded_duration_seconds"]
    assert abs(audio_delta) <= contract["preservation"]["decoded_audio_duration_tolerance_seconds"]
    assert len(output_probe["streams"]) == 2 and not output_probe["chapters"]
    ff("-xerror", "-i", converted, "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-")
    # Three actual decoded source frames above their corresponding output frames.
    make_preview(source, converted, output / "preview.png", "label-font.ttf", before_times, after_times)
    (output / "label-font.ttf").unlink()
    artifacts = {p.name: {"bytes": p.stat().st_size, "sha256": digest(p)}
                 for p in (source, converted, sidecar, output / "preview.png")}
    assert all(a["bytes"] < 2 * 1024 * 1024 for a in artifacts.values())
    evidence = {"target": contract["identity"], "versions": versions,
                "font_input": font_record, "source_unchanged": True,
                "source_local_contract_failures": failures_before,
                "output_local_contract_failures": failures_after,
                "source_frame_pts_seconds": before_times, "output_frame_pts_seconds": after_times,
                "max_frame_pts_difference_seconds": delta,
                "visual_landmarks": visual, "audio_content": sound,
                "audio_decoded_duration_difference_seconds": audio_delta,
                "subtitle_result": "Two cues; times and text match the supplied SRT exactly",
                "mp4_top_level_boxes": boxes, "full_av_decode": "passed with -xerror",
                "target_service_acceptance": "not tested; target contract is fictional",
                "artifacts": artifacts, "commands": portable_commands(COMMANDS, output),
                "path_note": "Commands use this report's directory as the media working directory; "
                             "output paths are relative. Tool-version lookups are independent of cwd. "
                             "label-font.ttf is a temporary copy of the recorded font, removed after rendering."}
    save(output / "evidence.json", evidence)
    print(json.dumps({"output_directory": str(output), "artifacts": artifacts,
                      "source_local_contract_failures": failures_before,
                      "output_local_contract_failures": failures_after}, indent=2))


if __name__ == "__main__":
    main()
