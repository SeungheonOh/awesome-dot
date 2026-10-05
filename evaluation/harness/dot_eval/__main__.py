"""No-install command interface. Run with `python -m dot_eval --help`."""
import argparse
import json
from pathlib import Path
import sys
from .core import IntegrityError, create_json, load_json
from .execution import RuntimeGateError, run_fixture, run_live
from .grading import blind_export, import_grade
from .protocol import freeze, initialize, prepare, schedule, verify
from .reporting import report
from .telemetry import CodexEvents


def main(argv=None):
    parser = argparse.ArgumentParser(description="Controlled skill evaluation scaffold; live dispatch is disabled")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("inspect-config", help="Verify explicit local source assets without freezing or launching")
    p.add_argument("config")
    p = sub.add_parser("freeze", help="Validate and content-freeze an explicit local config")
    p.add_argument("config"); p.add_argument("output")
    p = sub.add_parser("plan", help="Generate and freeze a balanced paired schedule after protocol freeze")
    p.add_argument("protocol"); p.add_argument("output"); p.add_argument("--seed", required=True, type=int)
    p = sub.add_parser("verify"); p.add_argument("protocol")
    p = sub.add_parser("init"); p.add_argument("protocol"); p.add_argument("schedule"); p.add_argument("study")
    p = sub.add_parser("prepare"); p.add_argument("study"); p.add_argument("attempt")
    p = sub.add_parser("fixture-run", help="Execute authored local process test doubles only")
    p.add_argument("study"); p.add_argument("attempt")
    p.add_argument("--mode", default="success", choices=("success", "failed", "timeout", "truncated", "missing_usage", "duplicate_items", "mutate_input"))
    p.add_argument("--timeout", type=float)
    p = sub.add_parser("live-run", help="Always fails closed: model execution is not enabled")
    p = sub.add_parser("parse-events", help="Parse caller-supplied JSONL without retaining raw text/reasoning")
    p.add_argument("path"); p.add_argument("--exit-code", type=int, required=True); p.add_argument("--timeout", action="store_true")
    p = sub.add_parser("blind-export"); p.add_argument("study"); p.add_argument("attempt"); p.add_argument("destination")
    p = sub.add_parser("import-grade"); p.add_argument("study"); p.add_argument("blind_id"); p.add_argument("grade")
    p.add_argument("--rater", required=True); p.add_argument("--kind", choices=("rating", "adjudication"), default="rating")
    p = sub.add_parser("report"); p.add_argument("study"); p.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect-config":
            result = freeze(args.config, None, inspection_only=True)
        elif args.command == "freeze":
            result = freeze(args.config, args.output)
            result = {"protocol_sha256": result["protocol_sha256"], "tasks": len(result["tasks"]), "stage": result["stage"]}
        elif args.command == "plan":
            result = schedule(load_json(args.protocol), args.seed); create_json(args.output, result)
            result = {"schedule_sha256": result["schedule_sha256"], "scheduled": len(result["rows"])}
        elif args.command == "verify":
            result = {"verified": verify(load_json(args.protocol))}
        elif args.command == "init":
            result = {"study": str(initialize(load_json(args.protocol), load_json(args.schedule), args.study))}
        elif args.command == "prepare":
            result = prepare(args.study, args.attempt); result.pop("prompt")
        elif args.command == "fixture-run":
            result = run_fixture(args.study, args.attempt, args.mode, args.timeout)
        elif args.command == "live-run":
            result = run_live()
        elif args.command == "parse-events":
            events = CodexEvents()
            with Path(args.path).open("rb") as stream:
                for line in stream:
                    events.feed(line)
            result = events.finish(args.exit_code, args.timeout)
        elif args.command == "blind-export":
            result = blind_export(args.study, args.attempt, args.destination)
        elif args.command == "import-grade":
            result = import_grade(args.study, args.blind_id, args.grade, args.rater, args.kind)
        elif args.command == "report":
            result = report(args.study)
            if args.output:
                create_json(args.output, result)
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    except (IntegrityError, RuntimeGateError, OSError, KeyError, ValueError) as error:
        print(json.dumps({"error": type(error).__name__, "detail": str(error)}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
