from __future__ import annotations

import argparse

VALID_STAGES = [
    "fetch",
    "ingest",
    "extract",
    "cluster",
    "investigate",
    "knowledge",
    "brief",
    "weekly",
    "monthly",
    "deliver",
    "site",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="news-intel")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run the full Personal Tech Radar pipeline")
    run.add_argument("--date", required=True)
    run.add_argument("--skip-delivery", action="store_true")

    stage = sub.add_parser("stage", help="Run one pipeline stage")
    stage.add_argument("stage_name", choices=VALID_STAGES)
    stage.add_argument("--date", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
