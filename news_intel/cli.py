from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from news_intel.config import load_sources
from news_intel.clustering import cluster_candidates
from news_intel.extraction import extract_candidate
from news_intel.ingest import parse_raw_article, should_drop_article
from news_intel.knowledge import update_claims, update_entities
from news_intel.llm import OpenAICompatibleClient
from news_intel.models import Article, Candidate, Claim, Entity, Event
from news_intel.storage import append_jsonl, read_jsonl, write_jsonl

ROOT = Path(__file__).resolve().parents[1]
CST = timezone(timedelta(hours=8))

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


def stage_extract(date: str) -> int:
    input_path = ROOT / "data" / "articles" / f"{date}.jsonl"
    output_path = ROOT / "data" / "candidates" / f"{date}.jsonl"
    llm = OpenAICompatibleClient()
    candidates = []
    failed = []
    for row in read_jsonl(input_path):
        article = Article.model_validate(row)
        try:
            candidate = extract_candidate(article, llm=llm)
            candidates.append(candidate.model_dump(mode="json"))
        except Exception as exc:
            failed.append(f"{article.id}: {exc}")
    write_jsonl(output_path, candidates)
    print(f"[EXTRACT] wrote {len(candidates)} candidates to {output_path}", file=sys.stderr)
    for failure in failed:
        print(f"[WARN] extract failed: {failure}", file=sys.stderr)
    return 0


def stage_cluster(date: str) -> int:
    input_path = ROOT / "data" / "candidates" / f"{date}.jsonl"
    events_path = ROOT / "data" / "events" / f"{date}.jsonl"
    evidence_path = ROOT / "data" / "evidence.jsonl"
    candidates = [Candidate.model_validate(row) for row in read_jsonl(input_path)]
    events, evidence = cluster_candidates(candidates)
    write_jsonl(events_path, [event.model_dump(mode="json") for event in events])
    append_jsonl(evidence_path, [row.model_dump(mode="json") for row in evidence])
    print(f"[CLUSTER] wrote {len(events)} events to {events_path}", file=sys.stderr)
    print(f"[CLUSTER] appended {len(evidence)} evidence rows to {evidence_path}", file=sys.stderr)
    return 0


def stage_knowledge(date: str) -> int:
    events_path = ROOT / "data" / "events" / f"{date}.jsonl"
    entities_path = ROOT / "data" / "entities.jsonl"
    claims_path = ROOT / "data" / "claims.jsonl"
    events = [Event.model_validate(row) for row in read_jsonl(events_path)]
    entities = [Entity.model_validate(row) for row in read_jsonl(entities_path)]
    claims = [Claim.model_validate(row) for row in read_jsonl(claims_path)]
    now = datetime.now(CST).isoformat()
    updated_entities = update_entities(entities, events, now=now)
    updated_claims = update_claims(claims, events, now=now)
    write_jsonl(entities_path, [entity.model_dump(mode="json") for entity in updated_entities])
    write_jsonl(claims_path, [claim.model_dump(mode="json") for claim in updated_claims])
    print(f"[KNOWLEDGE] wrote {len(updated_entities)} entities to {entities_path}", file=sys.stderr)
    print(f"[KNOWLEDGE] wrote {len(updated_claims)} claims to {claims_path}", file=sys.stderr)
    return 0


def run_stage(stage_name: str, date: str) -> int:
    if stage_name == "ingest":
        return stage_ingest(date)
    if stage_name == "extract":
        return stage_extract(date)
    if stage_name == "cluster":
        return stage_cluster(date)
    if stage_name == "knowledge":
        return stage_knowledge(date)
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
