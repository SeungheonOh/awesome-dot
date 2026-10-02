#!/usr/bin/env python3
"""Render this fictional caption pair on a labeled synthetic background.

Requires an existing FFmpeg with drawtext, subtitles/libass and libx264 support,
plus a DejaVu Sans font file. No download, network request or audio capture.
"""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent


def run(args, cwd):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=90)
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:])
    return result.stdout


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, required=True,
                        help="Existing DejaVuSans.ttf used for the example labels")
    parser.add_argument("--output", type=Path, required=True,
                        help="New output directory; existing directories are refused")
    args = parser.parse_args()
    font = args.font.resolve()
    output = args.output.resolve()
    if not font.is_file() or shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise ValueError("An existing font, ffmpeg and ffprobe are required")
    run([sys.executable, str(ROOT / "check_example.py")], ROOT)
    input_hashes = {name: sha256(ROOT / name) for name in ("captions.srt", "captions.vtt")}
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="caption-render-", dir=output) as temporary:
        work = Path(temporary)
        shutil.copyfile(font, work / "label-font.ttf")
        for name in input_hashes:
            shutil.copyfile(ROOT / name, work / name)
        (work / "header.txt").write_text("CAPTION RENDER CHECK", encoding="utf-8")
        (work / "scope.txt").write_text(
            "Synthetic background only. No source audio or video.", encoding="utf-8")
        label_filters = (
            "drawtext=fontfile=label-font.ttf:textfile=header.txt:fontsize=28:"
            "fontcolor=0xE7EEF2:x=(w-tw)/2:y=70,"
            "drawtext=fontfile=label-font.ttf:textfile=scope.txt:fontsize=19:"
            "fontcolor=0xA8BAC7:x=(w-tw)/2:y=116,"
        )
        frame_records = {}
        for extension in ("srt", "vtt"):
            filters = label_filters + (
                f"subtitles=captions.{extension}:fontsdir=.:"
                "force_style='FontName=DejaVu Sans,FontSize=22,MarginV=35'"
            )
            run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                 "color=c=0x101820:s=960x540:r=10:d=36", "-vf", filters,
                 "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22",
                 "-map_metadata", "-1", f"render-{extension}.mp4"], work)
            frame_text = run(["ffmpeg", "-v", "error", "-i", f"render-{extension}.mp4",
                              "-f", "framemd5", "-"], work)
            frame_records[extension] = [line for line in frame_text.splitlines()
                                        if line and not line.startswith("#")]
        if len(frame_records["srt"]) != 360 or frame_records["srt"] != frame_records["vtt"]:
            raise ValueError("The two formats did not render the same 360 decoded frames")
        points = [0, 30, 70, 120, 160, 210, 260, 310]
        selection = "+".join(f"eq(n\\,{number})" for number in points)
        run(["ffmpeg", "-v", "error", "-i", "render-srt.mp4", "-vf",
             f"select={selection},scale=720:405,tile=2x4", "-frames:v", "1",
             "-map_metadata", "-1", "render-preview.png"], work)
        streams = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                                  "stream=codec_type,width,height,nb_frames:format=duration",
                                  "-of", "json", "render-srt.mp4"], work))
        if len(streams["streams"]) != 1 or streams["streams"][0]["codec_type"] != "video":
            raise ValueError("Expected one video stream and no audio")
        shutil.copyfile(work / "render-srt.mp4", output / "caption-render.mp4")
        shutil.copyfile(work / "render-preview.png", output / "render-preview.png")
    if input_hashes != {name: sha256(ROOT / name) for name in input_hashes}:
        raise ValueError("Caption inputs changed during rendering")
    report = {
        "ffmpeg_version": run(["ffmpeg", "-version"], ROOT).splitlines()[0],
        "input_sha256": input_hashes,
        "output_sha256": {name: sha256(output / name) for name in
                          ("caption-render.mp4", "render-preview.png")},
        "decoded_frames_each": 360,
        "all_decoded_frames_equal": True,
        "contact_sheet_seconds": [number / 10 for number in points],
        "stream_inspection": streams,
        "source_media_alignment_checked": False,
        "audio_present": False,
    }
    (output / "render-check.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: both formats rendered 360 identical decoded frames; no audio stream")
    print("Inspect the actual preview for wrapping, accents and clipping before delivery.")


if __name__ == "__main__":
    main()
