from __future__ import annotations

import argparse
import sys
from pathlib import Path

from news_intel.config import load_sources
from news_intel.ingest import parse_raw_article, should_drop_article
from news_intel.storage import write_jsonl

ROOT = Path(__file__).resolve().parents[1]

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


def stage_ingest(date: str) -> int:
    yyyy, mm, dd = date.split("-")
    raw_dir = ROOT / "raw" / yyyy / mm / dd
    output_path = ROOT / "data" / "articles" / f"{date}.jsonl"
    if not raw_dir.exists():
        print(f"[WARN] raw directory does not exist: {raw_dir}", file=sys.stderr)
        write_jsonl(output_path, [])
        return 0

    sources = load_sources(ROOT / "sources" / "feeds.yaml")
    source_tiers = {source["name"]: source["tier"] for source in sources}
    articles = []
    dropped = 0
    for path in sorted(raw_dir.glob("*.md")):
        article = parse_raw_article(path, date=date, source_tiers=source_tiers)
        if should_drop_article(article):
            dropped += 1
            continue
        articles.append(article.model_dump(mode="json"))
    write_jsonl(output_path, articles)
    print(f"[INGEST] wrote {len(articles)} articles to {output_path} ({dropped} dropped)", file=sys.stderr)
    return 0


def run_stage(stage_name: str, date: str) -> int:
    if stage_name == "ingest":
        return stage_ingest(date)
    print(f"[WARN] stage not implemented yet: {stage_name}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "stage":
        return run_stage(args.stage_name, args.date)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
