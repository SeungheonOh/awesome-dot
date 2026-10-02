"""Read the installed package's format data and print one label."""

import argparse
import json
import sys
from importlib.resources import files

from . import __version__


def main():
    parser = argparse.ArgumentParser(prog="packet-stamp")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--style", choices=("standard", "priority"), default="standard")
    parser.add_argument("name")
    args = parser.parse_args()
    try:
        formats = json.loads(files("packet_stamp").joinpath("formats.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("packet-stamp: required bundled data formats.json is missing", file=sys.stderr)
        return 2
    print(formats[args.style].format(name=args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
