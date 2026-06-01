from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from news_intel.config import load_sources
from news_intel.briefing import render_daily_brief, render_monthly_review, render_weekly_review
from news_intel.clustering import cluster_candidates
from news_intel.extraction import extract_candidate
from news_intel.ingest import parse_raw_article, should_drop_article
from news_intel.investigation import INVESTIGATION_PROMPT, select_events_for_investigation
from news_intel.knowledge import update_claims, update_entities
from news_intel.llm import OpenAICompatibleClient
from news_intel.models import Article, Candidate, Claim, Entity, Event, Evidence, SourceHealth
from news_intel.storage import append_jsonl, read_jsonl, write_json, write_jsonl

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


def stage_investigate(date: str) -> int:
    events_path = ROOT / "data" / "events" / f"{date}.jsonl"
    events = [Event.model_validate(row) for row in read_jsonl(events_path)]
    selected = select_events_for_investigation(events)
    strong_model = os.environ.get("STRONG_LLM_MODEL", "")
    if not strong_model:
        skipped_path = ROOT / "state" / "investigation" / f"{date}-skipped.json"
        write_json(skipped_path, {
            "date": date,
            "reason": "STRONG_LLM_MODEL not configured",
            "selected_event_ids": [event.id for event in selected],
        })
        print(f"[INVESTIGATE] skipped {len(selected)} events; wrote {skipped_path}", file=sys.stderr)
        return 0

    client = OpenAICompatibleClient(model=strong_model)
    updated_by_id = {event.id: event for event in events}
    for event in selected:
        prompt = f"{INVESTIGATION_PROMPT}\n\nEVENT JSON:\n{event.model_dump_json()}"
        result = client.complete_json(prompt)
        current = updated_by_id[event.id]
        if result.get("confidence") in {"low", "medium", "high"}:
            current.confidence = result["confidence"]
        claim_links = result.get("claim_links", {})
        for claim_id, relation in claim_links.items():
            if relation in {"supports", "weakens", "contradicts", "neutral"}:
                current.claim_links[claim_id] = relation
        updated_by_id[event.id] = current
    write_jsonl(events_path, [event.model_dump(mode="json") for event in updated_by_id.values()])
    print(f"[INVESTIGATE] updated {len(selected)} events in {events_path}", file=sys.stderr)
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


def stage_brief(date: str) -> int:
    events_path = ROOT / "data" / "events" / f"{date}.jsonl"
    evidence_path = ROOT / "data" / "evidence.jsonl"
    health_path = ROOT / "state" / "source_health.json"
    daily_path = ROOT / "brief" / "daily" / f"{date}.md"
    report_path = ROOT / "report" / f"{date}.md"

    events = [Event.model_validate(row) for row in read_jsonl(events_path)]
    evidence_rows = [Evidence.model_validate(row) for row in read_jsonl(evidence_path)]
    evidence_by_id = {row.id: row for row in evidence_rows}
    health_data = json.loads(health_path.read_text(encoding="utf-8")) if health_path.exists() else {}
    source_health = [SourceHealth.model_validate(row) for row in health_data.values()]
    markdown = render_daily_brief(date, events, evidence_by_id, source_health)
    daily_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    daily_path.write_text(markdown, encoding="utf-8")
    report_path.write_text(markdown, encoding="utf-8")
    print(f"[BRIEF] wrote {daily_path}", file=sys.stderr)
    print(f"[BRIEF] mirrored {report_path}", file=sys.stderr)
    return 0


def events_for_period(*, week_id: str | None = None, month_id: str | None = None) -> list[Event]:
    events_dir = ROOT / "data" / "events"
    events = []
    for path in sorted(events_dir.glob("*.jsonl")):
        day = path.stem
        if week_id:
            if datetime.fromisoformat(day).date().isocalendar()[:2] != (
                int(week_id[:4]),
                int(week_id[-2:]),
            ):
                continue
        if month_id and not day.startswith(month_id):
            continue
        events.extend(Event.model_validate(row) for row in read_jsonl(path))
    return events


def stage_weekly(date: str) -> int:
    iso = datetime.fromisoformat(date).date().isocalendar()
    week_id = f"{iso.year}-W{iso.week:02d}"
    claims = [Claim.model_validate(row) for row in read_jsonl(ROOT / "data" / "claims.jsonl")]
    events = events_for_period(week_id=week_id)
    markdown = render_weekly_review(week_id, claims, events)
    path = ROOT / "brief" / "weekly" / f"{week_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")
    print(f"[WEEKLY] wrote {path}", file=sys.stderr)
    return 0


def stage_monthly(date: str) -> int:
    month_id = date[:7]
    claims = [Claim.model_validate(row) for row in read_jsonl(ROOT / "data" / "claims.jsonl")]
    events = events_for_period(month_id=month_id)
    markdown = render_monthly_review(month_id, claims, events)
    path = ROOT / "brief" / "monthly" / f"{month_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")
    print(f"[MONTHLY] wrote {path}", file=sys.stderr)
    return 0


def run_stage(stage_name: str, date: str) -> int:
    if stage_name == "ingest":
        return stage_ingest(date)
    if stage_name == "extract":
        return stage_extract(date)
    if stage_name == "cluster":
        return stage_cluster(date)
    if stage_name == "investigate":
        return stage_investigate(date)
    if stage_name == "knowledge":
        return stage_knowledge(date)
    if stage_name == "brief":
        return stage_brief(date)
    if stage_name == "weekly":
        return stage_weekly(date)
    if stage_name == "monthly":
        return stage_monthly(date)
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
