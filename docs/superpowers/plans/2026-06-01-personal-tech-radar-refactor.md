# Personal Tech Radar Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild News Intel from a daily news digest generator into a full personal technology intelligence radar with tiered source health, structured events/entities/claims, AI-routed investigation, push-first daily briefs, weekly synthesis, and research-oriented site pages.

**Architecture:** Keep the repository's file-based storage model, but replace prompt-led daily report generation with a Python package that writes validated JSONL/JSON/Markdown artifacts. The pipeline becomes `fetch -> ingest -> extract -> cluster -> investigate -> knowledge -> brief -> deliver -> site`, with agents reserved for top events and weekly synthesis rather than whole-feed processing.

**Tech Stack:** Python 3.11, pytest, pydantic, PyYAML, feedparser, urllib/http stdlib, OpenAI-compatible chat completions, Markdown/JSONL artifacts, Next.js 14 static export, Pagefind, GitHub Pages.

---

## File Structure

Create these new runtime directories:

- `state/source_health.json` - latest source health by source name.
- `data/articles/YYYY-MM-DD.jsonl` - normalized fetched articles.
- `data/candidates/YYYY-MM-DD.jsonl` - article-level extracted candidates.
- `data/events/YYYY-MM-DD.jsonl` - deduplicated daily events.
- `data/entities.jsonl` - durable entity records.
- `data/claims.jsonl` - durable claim records.
- `data/evidence.jsonl` - append-only evidence snippets.
- `brief/daily/YYYY-MM-DD.md` - push-first daily brief.
- `brief/weekly/YYYY-WW.md` - weekly synthesis.
- `brief/monthly/YYYY-MM.md` - monthly synthesis.

Keep these existing directories:

- `raw/YYYY/MM/DD/` remains the immutable raw article archive.
- `report/YYYY-MM-DD.md` remains a compatibility mirror for the daily brief until downstream readers migrate.
- `digest/` and `clusters/` remain historical artifacts; the new pipeline does not read them except during migration/backfill.
- `site/` remains the GitHub Pages static site, but it reads new structured artifacts instead of only `report/*.md`.

Create this Python package:

```text
news_intel/
  __init__.py
  cli.py
  config.py
  models.py
  storage.py
  source_health.py
  fetcher.py
  ingest.py
  llm.py
  extraction.py
  clustering.py
  knowledge.py
  investigation.py
  briefing.py
  delivery.py
```

Create these tests:

```text
tests/
  fixtures/
    article_official.md
    article_secondary.md
    article_duplicate.md
    article_pr.md
  test_models.py
  test_storage.py
  test_source_health.py
  test_ingest.py
  test_extraction.py
  test_clustering.py
  test_knowledge.py
  test_briefing.py
  test_delivery.py
  test_cli.py
```

---

## Task 1: Add Package Skeleton, Dependencies, and CLI Entrypoint

**Files:**
- Modify: `requirements.txt`
- Create: `news_intel/__init__.py`
- Create: `news_intel/cli.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write the failing CLI smoke test**

```python
# tests/test_cli.py
from news_intel.cli import build_parser


def test_parser_accepts_pipeline_commands():
    parser = build_parser()
    args = parser.parse_args(["run", "--date", "2026-06-01", "--skip-delivery"])
    assert args.command == "run"
    assert args.date == "2026-06-01"
    assert args.skip_delivery is True


def test_parser_accepts_individual_stage():
    parser = build_parser()
    args = parser.parse_args(["stage", "brief", "--date", "2026-06-01"])
    assert args.command == "stage"
    assert args.stage_name == "brief"
    assert args.date == "2026-06-01"
```

- [ ] **Step 2: Run the test and verify it fails**

Run: `python3.11 -m pytest tests/test_cli.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'news_intel'`.

- [ ] **Step 3: Add dependencies**

Replace `requirements.txt` content with:

```text
feedparser
PyYAML
pydantic>=2,<3
pytest
```

- [ ] **Step 4: Create package files**

```python
# news_intel/__init__.py
__all__ = ["__version__"]

__version__ = "0.1.0"
```

```python
# news_intel/cli.py
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
```

- [ ] **Step 5: Verify the CLI test passes**

Run: `python3.11 -m pytest tests/test_cli.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt news_intel tests/test_cli.py
git commit -m "chore: add personal radar package skeleton"
```

---

## Task 2: Define Validated Data Contracts

**Files:**
- Create: `news_intel/models.py`
- Create: `tests/test_models.py`

- [ ] **Step 1: Write model tests**

```python
# tests/test_models.py
from news_intel.models import Article, Claim, Event, Evidence, SourceHealth, SourceTier


def test_article_normalizes_source_tier():
    article = Article(
        id="2026-06-01-openai-001",
        date="2026-06-01",
        source="OpenAI Blog",
        source_tier=SourceTier.T0_FIRST_HAND,
        title="Introducing a model",
        url="https://openai.com/example",
        published="2026-06-01",
        category="ai_official",
        raw_path="raw/2026/06/01/001-openai.md",
        summary="Official model announcement",
        body="Full body",
    )
    assert article.source_tier == SourceTier.T0_FIRST_HAND
    assert article.is_first_hand is True


def test_source_health_marks_stale_after_failures():
    health = SourceHealth(
        source="Anthropic Blog",
        tier=SourceTier.T0_FIRST_HAND,
        last_attempt_at="2026-06-01T08:30:00+08:00",
        last_success_at="2026-05-29T08:30:00+08:00",
        status="failed",
        consecutive_failures=3,
        fetched_count=0,
        failure_reason="proxy timeout",
        proxy_used="http://127.0.0.1:7890",
    )
    assert health.is_stale is True


def test_event_links_evidence_entities_and_claims():
    evidence = Evidence(
        id="evd-001",
        event_id="evt-001",
        source="OpenAI Blog",
        source_tier=SourceTier.T0_FIRST_HAND,
        url="https://openai.com/example",
        quote="We are introducing...",
    )
    event = Event(
        id="evt-001",
        date="2026-06-01",
        title="OpenAI introduces a model",
        summary="OpenAI introduced a model.",
        importance=4,
        confidence="high",
        source_tiers=[SourceTier.T0_FIRST_HAND],
        article_ids=["art-001"],
        entity_ids=["openai"],
        evidence_ids=[evidence.id],
        claim_links={"claim-agentic-coding": "supports"},
    )
    assert event.claim_links["claim-agentic-coding"] == "supports"
    assert event.confidence == "high"


def test_claim_status_is_conservative():
    claim = Claim(
        id="claim-agentic-coding",
        title="Coding agents are becoming engineering environments",
        status="active",
        confidence="medium",
        summary="Repeated releases indicate a shift from chat to agentic coding environments.",
        supporting_event_ids=["evt-001"],
        weakening_event_ids=[],
        contradicting_event_ids=[],
        updated_at="2026-06-01T09:00:00+08:00",
    )
    assert claim.status == "active"
```

- [ ] **Step 2: Run the tests and verify they fail**

Run: `python3.11 -m pytest tests/test_models.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'news_intel.models'`.

- [ ] **Step 3: Implement data models**

```python
# news_intel/models.py
from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class SourceTier(str, Enum):
    T0_FIRST_HAND = "T0_FIRST_HAND"
    T1_HIGH_QUALITY_SECONDARY = "T1_HIGH_QUALITY_SECONDARY"
    T2_COMMUNITY_DISCOVERY = "T2_COMMUNITY_DISCOVERY"
    T3_CHINESE_SECONDARY = "T3_CHINESE_SECONDARY"


class Article(BaseModel):
    id: str
    date: str
    source: str
    source_tier: SourceTier
    title: str
    url: str
    published: str
    category: str
    raw_path: str
    summary: str = ""
    body: str = ""

    @property
    def is_first_hand(self) -> bool:
        return self.source_tier == SourceTier.T0_FIRST_HAND


class SourceHealth(BaseModel):
    source: str
    tier: SourceTier
    last_attempt_at: str
    last_success_at: str | None = None
    status: Literal["ok", "failed", "empty", "stale"]
    consecutive_failures: int = 0
    fetched_count: int = 0
    failure_reason: str = ""
    proxy_used: str = ""

    @property
    def is_stale(self) -> bool:
        return self.status in {"failed", "stale"} and self.consecutive_failures >= 2


class Candidate(BaseModel):
    id: str
    article_id: str
    date: str
    event_key: str
    title: str
    summary: str
    source: str
    source_tier: SourceTier
    entities: list[str] = Field(default_factory=list)
    category: str
    intent: Literal[
        "official_announcement",
        "reporting",
        "commentary",
        "pr",
        "community_discussion",
        "deal",
        "tutorial",
        "research",
        "regulatory",
    ]
    importance: int = Field(ge=1, le=5)
    confidence: Literal["low", "medium", "high"]
    caveats: list[str] = Field(default_factory=list)
    evidence_quote: str = ""
    url: str


class Evidence(BaseModel):
    id: str
    event_id: str
    source: str
    source_tier: SourceTier
    url: str
    quote: str


class Event(BaseModel):
    id: str
    date: str
    title: str
    summary: str
    importance: int = Field(ge=1, le=5)
    confidence: Literal["low", "medium", "high"]
    source_tiers: list[SourceTier]
    article_ids: list[str]
    entity_ids: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    claim_links: dict[str, Literal["supports", "weakens", "contradicts", "neutral"]] = Field(default_factory=dict)


class Entity(BaseModel):
    id: str
    name: str
    aliases: list[str] = Field(default_factory=list)
    kind: Literal["company", "product", "person", "technology", "regulator", "project", "topic"]
    event_ids: list[str] = Field(default_factory=list)
    updated_at: str


class Claim(BaseModel):
    id: str
    title: str
    status: Literal["active", "watching", "weakened", "contradicted", "retired"]
    confidence: Literal["low", "medium", "high"]
    summary: str
    supporting_event_ids: list[str] = Field(default_factory=list)
    weakening_event_ids: list[str] = Field(default_factory=list)
    contradicting_event_ids: list[str] = Field(default_factory=list)
    updated_at: str
```

- [ ] **Step 4: Verify model tests pass**

Run: `python3.11 -m pytest tests/test_models.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add news_intel/models.py tests/test_models.py
git commit -m "feat: define personal radar data contracts"
```

---

## Task 3: Add File Storage Utilities

**Files:**
- Create: `news_intel/storage.py`
- Create: `tests/test_storage.py`

- [ ] **Step 1: Write storage tests**

```python
# tests/test_storage.py
from pathlib import Path

from news_intel.models import Article, SourceTier
from news_intel.storage import append_jsonl, read_jsonl, write_json


def test_append_and_read_jsonl_round_trip(tmp_path: Path):
    path = tmp_path / "data" / "articles.jsonl"
    article = Article(
        id="art-001",
        date="2026-06-01",
        source="OpenAI Blog",
        source_tier=SourceTier.T0_FIRST_HAND,
        title="Title",
        url="https://openai.com/example",
        published="2026-06-01",
        category="ai_official",
        raw_path="raw/2026/06/01/001.md",
    )

    append_jsonl(path, [article.model_dump(mode="json")])

    rows = list(read_jsonl(path))
    assert rows[0]["id"] == "art-001"
    assert rows[0]["source_tier"] == "T0_FIRST_HAND"


def test_write_json_creates_parent_directory(tmp_path: Path):
    path = tmp_path / "state" / "source_health.json"
    write_json(path, {"OpenAI Blog": {"status": "ok"}})
    assert path.exists()
    assert '"OpenAI Blog"' in path.read_text(encoding="utf-8")
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_storage.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'news_intel.storage'`.

- [ ] **Step 3: Implement storage utilities**

```python
# news_intel/storage.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def append_jsonl(path: Path, rows: Iterable[dict]) -> None:
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    ensure_parent(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(path)


def read_jsonl(path: Path) -> Iterable[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, data: dict | list) -> None:
    ensure_parent(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)
```

- [ ] **Step 4: Verify storage tests pass**

Run: `python3.11 -m pytest tests/test_storage.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add news_intel/storage.py tests/test_storage.py
git commit -m "feat: add json artifact storage utilities"
```

---

## Task 4: Extend Source Configuration with Tiers and Fetch Strategy

**Files:**
- Modify: `sources/feeds.yaml`
- Create: `news_intel/config.py`
- Create: `tests/test_source_health.py`
- Create: `news_intel/source_health.py`

- [ ] **Step 1: Write config and health tests**

```python
# tests/test_source_health.py
from news_intel.config import load_sources
from news_intel.models import SourceTier
from news_intel.source_health import build_health_record


def test_load_sources_reads_tiers():
    sources = load_sources("sources/feeds.yaml")
    openai = next(s for s in sources if s["name"] == "OpenAI Blog")
    assert openai["tier"] == SourceTier.T0_FIRST_HAND
    assert openai["fetch_strategy"] in {"rss", "html", "browser", "manual"}


def test_build_health_record_for_failed_fetch():
    source = {
        "name": "Anthropic Blog",
        "tier": SourceTier.T0_FIRST_HAND,
    }
    record = build_health_record(
        source=source,
        status="failed",
        fetched_count=0,
        failure_reason="proxy timeout",
        proxy_used="http://127.0.0.1:7890",
        now="2026-06-01T08:30:00+08:00",
        previous={"consecutive_failures": 1, "last_success_at": "2026-05-31T08:30:00+08:00"},
    )
    assert record.consecutive_failures == 2
    assert record.is_stale is True
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_source_health.py -v`

Expected: FAIL because `news_intel.config` and `news_intel.source_health` do not exist.

- [ ] **Step 3: Update `sources/feeds.yaml` schema**

For every source, add:

```yaml
    tier: T1_HIGH_QUALITY_SECONDARY
    fetch_strategy: rss
    use_proxy: true
```

Use these exact tier assignments:

- `T0_FIRST_HAND`: OpenAI Blog, Google DeepMind Blog, Meta AI Blog, Anthropic Blog, GitHub Changelog, Papers With Code when it links to primary papers.
- `T1_HIGH_QUALITY_SECONDARY`: TechCrunch, The Verge, Ars Technica, Wired, MIT Tech Review, VentureBeat AI, Latent Space, Simon Willison Blog, InfoQ.
- `T2_COMMUNITY_DISCOVERY`: Hacker News, Product Hunt, GitHub Trending, AI Reddit.
- `T3_CHINESE_SECONDARY`: 36氪, 爱范儿, 极客公园, 少数派, 钛媒体, 机器之心, 量子位, Solidot.

Use `fetch_strategy: html` for first-hand sources that have no working RSS. Keep disabled sources disabled unless the source can be fetched reliably by the selected strategy.

- [ ] **Step 4: Implement config loader**

```python
# news_intel/config.py
from __future__ import annotations

from pathlib import Path

import yaml

from news_intel.models import SourceTier


def load_sources(path: str | Path) -> list[dict]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    sources = []
    for source in data.get("sources", []):
        tier = source.get("tier")
        if not tier:
            raise ValueError(f"source {source.get('name')} missing tier")
        item = dict(source)
        item["tier"] = SourceTier(tier)
        item.setdefault("fetch_strategy", "rss")
        item.setdefault("use_proxy", True)
        sources.append(item)
    return sources
```

- [ ] **Step 5: Implement source health builder**

```python
# news_intel/source_health.py
from __future__ import annotations

from typing import Literal

from news_intel.models import SourceHealth


def build_health_record(
    *,
    source: dict,
    status: Literal["ok", "failed", "empty", "stale"],
    fetched_count: int,
    failure_reason: str,
    proxy_used: str,
    now: str,
    previous: dict | None,
) -> SourceHealth:
    previous = previous or {}
    previous_failures = int(previous.get("consecutive_failures", 0))
    consecutive_failures = 0 if status == "ok" else previous_failures + 1
    last_success_at = now if status == "ok" else previous.get("last_success_at")
    return SourceHealth(
        source=source["name"],
        tier=source["tier"],
        last_attempt_at=now,
        last_success_at=last_success_at,
        status=status,
        consecutive_failures=consecutive_failures,
        fetched_count=fetched_count,
        failure_reason=failure_reason,
        proxy_used=proxy_used,
    )
```

- [ ] **Step 6: Verify tests pass**

Run: `python3.11 -m pytest tests/test_source_health.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add sources/feeds.yaml news_intel/config.py news_intel/source_health.py tests/test_source_health.py
git commit -m "feat: add source tiers and health contracts"
```

---

## Task 5: Refactor Fetch into a Source-Health-Aware Stage

**Files:**
- Create: `news_intel/fetcher.py`
- Modify: `scripts/fetch.py`
- Test: `tests/test_ingest.py`

- [ ] **Step 1: Write fetch output fixture test**

```python
# tests/test_ingest.py
from pathlib import Path

from news_intel.fetcher import article_id_from_path, source_slug


def test_source_slug_is_stable():
    assert source_slug("OpenAI Blog") == "openai-blog"
    assert source_slug("36氪") == "36"


def test_article_id_from_path_uses_date_and_stem():
    path = Path("raw/2026/06/01/001-openai-blog-example.md")
    assert article_id_from_path(path) == "2026-06-01-001-openai-blog-example"
```

- [ ] **Step 2: Run test and verify failure**

Run: `python3.11 -m pytest tests/test_ingest.py -v`

Expected: FAIL because `news_intel.fetcher` does not exist.

- [ ] **Step 3: Implement fetch helper functions**

```python
# news_intel/fetcher.py
from __future__ import annotations

import re
import unicodedata
from pathlib import Path


def source_slug(text: str, max_len: int = 40) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    normalized = re.sub(r"[^\w\s-]", "", normalized.lower())
    normalized = re.sub(r"[\s_-]+", "-", normalized).strip("-")
    return normalized[:max_len] or "untitled"


def article_id_from_path(path: Path) -> str:
    parts = path.parts
    raw_idx = parts.index("raw")
    yyyy, mm, dd = parts[raw_idx + 1 : raw_idx + 4]
    return f"{yyyy}-{mm}-{dd}-{path.stem}"
```

- [ ] **Step 4: Modify `scripts/fetch.py` to delegate helpers**

Change `slugify` to call `news_intel.fetcher.source_slug`. When saving each source result, also update `state/source_health.json` using `build_health_record`. The script should write raw markdown exactly as before, then write source health atomically at the end.

Use this observable behavior:

- If a source fetch succeeds and returns articles, status is `ok`.
- If a source fetch succeeds but returns zero articles, status is `empty`.
- If RSS or content request raises, status is `failed`.
- `proxy_used` is the active `HTTPS_PROXY`/`HTTP_PROXY` value or an empty string.

- [ ] **Step 5: Verify helper test passes**

Run: `python3.11 -m pytest tests/test_ingest.py -v`

Expected: PASS.

- [ ] **Step 6: Run fetch with a small limit**

Run: `python3.11 scripts/fetch.py --date 2026-06-01 --limit 1`

Expected:

- Raw files appear under `raw/2026/06/01/`.
- `state/source_health.json` exists.
- The command prints the raw output directory.

- [ ] **Step 7: Commit**

```bash
git add news_intel/fetcher.py scripts/fetch.py tests/test_ingest.py state/source_health.json raw/2026/06/01
git commit -m "feat: record source health during fetch"
```

---

## Task 6: Normalize Raw Articles into `data/articles`

**Files:**
- Create: `news_intel/ingest.py`
- Extend: `tests/test_ingest.py`

- [ ] **Step 1: Add fixture files**

```markdown
<!-- tests/fixtures/article_official.md -->
---
title: "Introducing Example Model"
source: OpenAI Blog
url: https://openai.com/example
published: 2026-06-01T08:00:00+08:00
lang: en
category: ai_official
---

# Introducing Example Model

## RSS 摘要

Official announcement.

## 正文

OpenAI introduced an example model with new coding capabilities.
```

```markdown
<!-- tests/fixtures/article_pr.md -->
---
title: "限时优惠：AI神器震撼上线"
source: 36氪
url: https://36kr.com/example
published: 2026-06-01T08:00:00+08:00
lang: zh
category: tech_startup
---

# 限时优惠：AI神器震撼上线

## RSS 摘要

广告软文。

## 正文

限时优惠，点击领取福利。
```

- [ ] **Step 2: Add ingest tests**

```python
# append to tests/test_ingest.py
from pathlib import Path

from news_intel.ingest import parse_raw_article, should_drop_article
from news_intel.models import SourceTier


def test_parse_raw_article_maps_source_tier():
    source_map = {"OpenAI Blog": SourceTier.T0_FIRST_HAND}
    article = parse_raw_article(
        Path("tests/fixtures/article_official.md"),
        date="2026-06-01",
        source_tiers=source_map,
    )
    assert article.source == "OpenAI Blog"
    assert article.source_tier == SourceTier.T0_FIRST_HAND
    assert "coding capabilities" in article.body


def test_should_drop_article_filters_obvious_ad():
    source_map = {"36氪": SourceTier.T3_CHINESE_SECONDARY}
    article = parse_raw_article(
        Path("tests/fixtures/article_pr.md"),
        date="2026-06-01",
        source_tiers=source_map,
    )
    assert should_drop_article(article) is True
```

- [ ] **Step 3: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_ingest.py -v`

Expected: FAIL because `news_intel.ingest` does not exist.

- [ ] **Step 4: Implement ingest parser and filter**

```python
# news_intel/ingest.py
from __future__ import annotations

from pathlib import Path

from news_intel.fetcher import article_id_from_path
from news_intel.models import Article, SourceTier


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end < 0:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta, text[end + 3 :].strip()


def parse_raw_article(path: Path, *, date: str, source_tiers: dict[str, SourceTier]) -> Article:
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    source = meta.get("source", "")
    return Article(
        id=article_id_from_path(path),
        date=date,
        source=source,
        source_tier=source_tiers.get(source, SourceTier.T1_HIGH_QUALITY_SECONDARY),
        title=meta.get("title", path.stem),
        url=meta.get("url", ""),
        published=meta.get("published", "")[:10],
        category=meta.get("category", ""),
        raw_path=str(path),
        summary=extract_section(body, "RSS 摘要"),
        body=extract_section(body, "正文") or body,
    )


def extract_section(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in markdown:
        return ""
    tail = markdown.split(marker, 1)[1]
    next_heading = tail.find("\n## ")
    if next_heading >= 0:
        tail = tail[:next_heading]
    return tail.strip()


def should_drop_article(article: Article) -> bool:
    text = f"{article.title}\n{article.summary}\n{article.body}".lower()
    ad_markers = ["限时优惠", "点击领取", "memorial day deals", "best deals", "coupon", "优惠券"]
    if any(marker.lower() in text for marker in ad_markers):
        return True
    if len(article.body.strip()) < 80 and not article.is_first_hand:
        return True
    return False
```

- [ ] **Step 5: Add a CLI stage implementation**

Extend `news_intel/cli.py` so `stage ingest --date YYYY-MM-DD`:

- Loads source tiers from `sources/feeds.yaml`.
- Reads `raw/YYYY/MM/DD/*.md`.
- Drops articles where `should_drop_article` is true.
- Writes kept articles to `data/articles/YYYY-MM-DD.jsonl`.

- [ ] **Step 6: Verify ingest tests pass**

Run: `python3.11 -m pytest tests/test_ingest.py -v`

Expected: PASS.

- [ ] **Step 7: Run ingest on existing raw data**

Run: `python3.11 -m news_intel.cli stage ingest --date 2026-05-26`

Expected: `data/articles/2026-05-26.jsonl` exists and contains fewer rows than raw files if ad/deal filtering matched.

- [ ] **Step 8: Commit**

```bash
git add news_intel/ingest.py news_intel/cli.py tests/fixtures tests/test_ingest.py data/articles/2026-05-26.jsonl
git commit -m "feat: normalize raw articles into structured article data"
```

---

## Task 7: Add LLM Client and Structured Candidate Extraction

**Files:**
- Create: `news_intel/llm.py`
- Create: `news_intel/extraction.py`
- Create: `tests/test_extraction.py`

- [ ] **Step 1: Write extraction tests with a fake LLM**

```python
# tests/test_extraction.py
from news_intel.extraction import extract_candidate
from news_intel.models import Article, SourceTier


class FakeLLM:
    def complete_json(self, prompt: str) -> dict:
        return {
            "event_key": "openai-example-model",
            "title": "OpenAI introduces Example Model",
            "summary": "OpenAI introduced an example model with coding capabilities.",
            "entities": ["OpenAI", "Example Model"],
            "intent": "official_announcement",
            "importance": 4,
            "confidence": "high",
            "caveats": ["Performance claims are from official announcement only."],
            "evidence_quote": "OpenAI introduced an example model with new coding capabilities.",
        }


def test_extract_candidate_preserves_source_tier_and_url():
    article = Article(
        id="art-001",
        date="2026-06-01",
        source="OpenAI Blog",
        source_tier=SourceTier.T0_FIRST_HAND,
        title="Introducing Example Model",
        url="https://openai.com/example",
        published="2026-06-01",
        category="ai_official",
        raw_path="raw/2026/06/01/001.md",
        body="OpenAI introduced an example model with new coding capabilities.",
    )
    candidate = extract_candidate(article, llm=FakeLLM())
    assert candidate.article_id == "art-001"
    assert candidate.source_tier == SourceTier.T0_FIRST_HAND
    assert candidate.importance == 4
    assert candidate.evidence_quote.startswith("OpenAI introduced")
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_extraction.py -v`

Expected: FAIL because extraction modules do not exist.

- [ ] **Step 3: Implement OpenAI-compatible LLM client**

```python
# news_intel/llm.py
from __future__ import annotations

import json
import os
import urllib.request


class OpenAICompatibleClient:
    def __init__(self, *, api_key: str | None = None, api_host: str | None = None, model: str | None = None):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        self.api_host = (api_host or os.environ.get("LLM_API_HOST", "https://api.minimaxi.com")).rstrip("/")
        self.model = model or os.environ.get("LLM_MODEL", "MiniMax-M2.7")

    def complete_json(self, prompt: str) -> dict:
        payload = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 1200,
        }).encode()
        req = urllib.request.Request(
            f"{self.api_host}/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read())
        text = data["choices"][0]["message"]["content"]
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end < start:
            raise ValueError(f"LLM did not return JSON object: {text[:200]}")
        return json.loads(text[start : end + 1])
```

- [ ] **Step 4: Implement candidate extraction**

```python
# news_intel/extraction.py
from __future__ import annotations

from news_intel.models import Article, Candidate


EXTRACTION_PROMPT = """你是个人科技情报系统的信息抽取器。
只输出 JSON 对象，不输出 Markdown。

字段:
- event_key: kebab-case 事件键，优先使用公司/产品/动作
- title: 事实标题，不使用营销措辞
- summary: 80字以内事实摘要，保留限定词
- entities: 专有名词列表
- intent: one of official_announcement, reporting, commentary, pr, community_discussion, deal, tutorial, research, regulatory
- importance: 1-5
- confidence: low, medium, high
- caveats: 重要限制或缺失信息数组
- evidence_quote: 原文中最关键的一句证据

文章:
{article_text}
"""


def extract_candidate(article: Article, *, llm) -> Candidate:
    article_text = f"标题: {article.title}\n来源: {article.source}\n正文:\n{article.body[:5000]}"
    data = llm.complete_json(EXTRACTION_PROMPT.format(article_text=article_text))
    return Candidate(
        id=f"cand-{article.id}",
        article_id=article.id,
        date=article.date,
        event_key=data["event_key"],
        title=data["title"],
        summary=data["summary"],
        source=article.source,
        source_tier=article.source_tier,
        entities=data.get("entities", []),
        category=article.category,
        intent=data["intent"],
        importance=int(data["importance"]),
        confidence=data["confidence"],
        caveats=data.get("caveats", []),
        evidence_quote=data.get("evidence_quote", ""),
        url=article.url,
    )
```

- [ ] **Step 5: Add CLI extract stage**

Extend `news_intel/cli.py` so `stage extract --date YYYY-MM-DD`:

- Reads `data/articles/YYYY-MM-DD.jsonl`.
- Calls `extract_candidate` for each article.
- Writes valid candidates to `data/candidates/YYYY-MM-DD.jsonl`.
- Prints candidate count and any failed article IDs to stderr.

- [ ] **Step 6: Verify extraction tests pass**

Run: `python3.11 -m pytest tests/test_extraction.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add news_intel/llm.py news_intel/extraction.py news_intel/cli.py tests/test_extraction.py
git commit -m "feat: extract structured candidates with routed llm"
```

---

## Task 8: Cluster Candidates into Events and Evidence

**Files:**
- Create: `news_intel/clustering.py`
- Create: `tests/test_clustering.py`

- [ ] **Step 1: Write clustering tests**

```python
# tests/test_clustering.py
from news_intel.clustering import cluster_candidates
from news_intel.models import Candidate, SourceTier


def candidate(id_: str, source: str, tier: SourceTier, key: str) -> Candidate:
    return Candidate(
        id=id_,
        article_id=f"art-{id_}",
        date="2026-06-01",
        event_key=key,
        title="OpenAI introduces Example Model",
        summary="OpenAI introduced an example model.",
        source=source,
        source_tier=tier,
        entities=["OpenAI", "Example Model"],
        category="ai_official",
        intent="official_announcement",
        importance=4,
        confidence="high",
        evidence_quote="OpenAI introduced an example model.",
        url=f"https://example.com/{id_}",
    )


def test_cluster_candidates_merges_same_event_key():
    events, evidence = cluster_candidates([
        candidate("001", "OpenAI Blog", SourceTier.T0_FIRST_HAND, "openai-example-model"),
        candidate("002", "The Verge", SourceTier.T1_HIGH_QUALITY_SECONDARY, "openai-example-model"),
    ])
    assert len(events) == 1
    assert len(evidence) == 2
    assert events[0].source_tiers == [SourceTier.T0_FIRST_HAND, SourceTier.T1_HIGH_QUALITY_SECONDARY]
    assert events[0].importance == 4
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_clustering.py -v`

Expected: FAIL because `news_intel.clustering` does not exist.

- [ ] **Step 3: Implement clustering**

```python
# news_intel/clustering.py
from __future__ import annotations

import hashlib

from news_intel.models import Candidate, Event, Evidence, SourceTier


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def cluster_candidates(candidates: list[Candidate]) -> tuple[list[Event], list[Evidence]]:
    groups: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        groups.setdefault(candidate.event_key, []).append(candidate)

    events: list[Event] = []
    evidence_rows: list[Evidence] = []
    for event_key, group in groups.items():
        group = sorted(group, key=lambda c: (c.source_tier.value, c.source, c.id))
        event_id = stable_id("evt", f"{group[0].date}:{event_key}")
        evidence_ids: list[str] = []
        for item in group:
            evidence_id = stable_id("evd", f"{event_id}:{item.id}:{item.url}")
            evidence_rows.append(Evidence(
                id=evidence_id,
                event_id=event_id,
                source=item.source,
                source_tier=item.source_tier,
                url=item.url,
                quote=item.evidence_quote,
            ))
            evidence_ids.append(evidence_id)
        source_tiers = []
        for tier in [SourceTier.T0_FIRST_HAND, SourceTier.T1_HIGH_QUALITY_SECONDARY, SourceTier.T2_COMMUNITY_DISCOVERY, SourceTier.T3_CHINESE_SECONDARY]:
            if any(item.source_tier == tier for item in group):
                source_tiers.append(tier)
        best = max(group, key=lambda c: (c.importance, c.source_tier == SourceTier.T0_FIRST_HAND))
        events.append(Event(
            id=event_id,
            date=best.date,
            title=best.title,
            summary=best.summary,
            importance=max(item.importance for item in group),
            confidence="high" if any(item.source_tier == SourceTier.T0_FIRST_HAND for item in group) else best.confidence,
            source_tiers=source_tiers,
            article_ids=[item.article_id for item in group],
            entity_ids=[normalize_entity_id(e) for item in group for e in item.entities],
            evidence_ids=evidence_ids,
            claim_links={},
        ))
    return events, evidence_rows


def normalize_entity_id(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "-")
```

- [ ] **Step 4: Add CLI cluster stage**

Extend `news_intel/cli.py` so `stage cluster --date YYYY-MM-DD`:

- Reads `data/candidates/YYYY-MM-DD.jsonl`.
- Writes `data/events/YYYY-MM-DD.jsonl`.
- Appends evidence to `data/evidence.jsonl`.

- [ ] **Step 5: Verify clustering tests pass**

Run: `python3.11 -m pytest tests/test_clustering.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add news_intel/clustering.py news_intel/cli.py tests/test_clustering.py
git commit -m "feat: cluster candidates into events and evidence"
```

---

## Task 9: Maintain Entities and Claims

**Files:**
- Create: `news_intel/knowledge.py`
- Create: `tests/test_knowledge.py`

- [ ] **Step 1: Write knowledge update tests**

```python
# tests/test_knowledge.py
from news_intel.knowledge import update_entities, update_claims
from news_intel.models import Claim, Event, SourceTier


def event(id_: str, entity_ids: list[str], claim_links: dict[str, str]) -> Event:
    return Event(
        id=id_,
        date="2026-06-01",
        title="Event",
        summary="Summary",
        importance=4,
        confidence="high",
        source_tiers=[SourceTier.T0_FIRST_HAND],
        article_ids=["art-001"],
        entity_ids=entity_ids,
        evidence_ids=["evd-001"],
        claim_links=claim_links,
    )


def test_update_entities_appends_event_ids():
    entities = update_entities([], [event("evt-001", ["openai"], {})], now="2026-06-01T09:00:00+08:00")
    assert entities[0].id == "openai"
    assert entities[0].event_ids == ["evt-001"]


def test_update_claims_tracks_support_and_contradiction():
    existing = [
        Claim(
            id="claim-agentic-coding",
            title="Coding agents are becoming engineering environments",
            status="watching",
            confidence="low",
            summary="Early evidence only.",
            updated_at="2026-05-30T09:00:00+08:00",
        )
    ]
    claims = update_claims(
        existing,
        [event("evt-001", ["openai"], {"claim-agentic-coding": "supports"})],
        now="2026-06-01T09:00:00+08:00",
    )
    assert claims[0].supporting_event_ids == ["evt-001"]
    assert claims[0].status == "active"
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_knowledge.py -v`

Expected: FAIL because `news_intel.knowledge` does not exist.

- [ ] **Step 3: Implement knowledge updates**

```python
# news_intel/knowledge.py
from __future__ import annotations

from news_intel.models import Claim, Entity, Event


def update_entities(existing: list[Entity], events: list[Event], *, now: str) -> list[Entity]:
    by_id = {entity.id: entity for entity in existing}
    for event in events:
        for entity_id in event.entity_ids:
            entity = by_id.get(entity_id)
            if entity is None:
                entity = Entity(
                    id=entity_id,
                    name=entity_id.replace("-", " ").title(),
                    kind="topic",
                    event_ids=[],
                    updated_at=now,
                )
            if event.id not in entity.event_ids:
                entity.event_ids.append(event.id)
            entity.updated_at = now
            by_id[entity_id] = entity
    return sorted(by_id.values(), key=lambda e: e.id)


def update_claims(existing: list[Claim], events: list[Event], *, now: str) -> list[Claim]:
    by_id = {claim.id: claim for claim in existing}
    for event in events:
        for claim_id, relation in event.claim_links.items():
            claim = by_id.get(claim_id)
            if claim is None:
                claim = Claim(
                    id=claim_id,
                    title=claim_id.replace("claim-", "").replace("-", " "),
                    status="watching",
                    confidence="low",
                    summary="Created from event linkage.",
                    updated_at=now,
                )
            if relation == "supports" and event.id not in claim.supporting_event_ids:
                claim.supporting_event_ids.append(event.id)
            if relation == "weakens" and event.id not in claim.weakening_event_ids:
                claim.weakening_event_ids.append(event.id)
            if relation == "contradicts" and event.id not in claim.contradicting_event_ids:
                claim.contradicting_event_ids.append(event.id)
            claim.status = derive_claim_status(claim)
            claim.confidence = derive_claim_confidence(claim)
            claim.updated_at = now
            by_id[claim_id] = claim
    return sorted(by_id.values(), key=lambda c: c.id)


def derive_claim_status(claim: Claim) -> str:
    if len(claim.contradicting_event_ids) >= 2:
        return "contradicted"
    if len(claim.weakening_event_ids) > len(claim.supporting_event_ids):
        return "weakened"
    if len(claim.supporting_event_ids) >= 1:
        return "active"
    return claim.status


def derive_claim_confidence(claim: Claim) -> str:
    total = len(claim.supporting_event_ids) + len(claim.weakening_event_ids) + len(claim.contradicting_event_ids)
    if total >= 5:
        return "high"
    if total >= 2:
        return "medium"
    return "low"
```

- [ ] **Step 4: Add CLI knowledge stage**

Extend `news_intel/cli.py` so `stage knowledge --date YYYY-MM-DD`:

- Reads `data/events/YYYY-MM-DD.jsonl`.
- Reads current `data/entities.jsonl` and `data/claims.jsonl`.
- Writes updated `data/entities.jsonl` and `data/claims.jsonl`.

- [ ] **Step 5: Verify knowledge tests pass**

Run: `python3.11 -m pytest tests/test_knowledge.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add news_intel/knowledge.py news_intel/cli.py tests/test_knowledge.py
git commit -m "feat: maintain entity and claim history"
```

---

## Task 10: Add Strong-Model Investigation Hooks

**Files:**
- Create: `news_intel/investigation.py`
- Create: `tests/test_extraction.py`

- [ ] **Step 1: Add investigation selection tests**

```python
# append to tests/test_extraction.py
from news_intel.investigation import select_events_for_investigation
from news_intel.models import Event, SourceTier


def test_select_events_for_investigation_prioritizes_important_and_non_first_hand():
    events = [
        Event(
            id="evt-low",
            date="2026-06-01",
            title="Low",
            summary="Low",
            importance=2,
            confidence="medium",
            source_tiers=[SourceTier.T1_HIGH_QUALITY_SECONDARY],
            article_ids=["art-1"],
        ),
        Event(
            id="evt-important-secondary",
            date="2026-06-01",
            title="Important",
            summary="Important",
            importance=5,
            confidence="medium",
            source_tiers=[SourceTier.T1_HIGH_QUALITY_SECONDARY],
            article_ids=["art-2"],
        ),
    ]
    selected = select_events_for_investigation(events, limit=3)
    assert [event.id for event in selected] == ["evt-important-secondary"]
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_extraction.py -v`

Expected: FAIL because `news_intel.investigation` does not exist.

- [ ] **Step 3: Implement investigation selector**

```python
# news_intel/investigation.py
from __future__ import annotations

from news_intel.models import Event, SourceTier


def select_events_for_investigation(events: list[Event], *, limit: int = 5) -> list[Event]:
    candidates = [
        event for event in events
        if event.importance >= 4 and SourceTier.T0_FIRST_HAND not in event.source_tiers
    ]
    return sorted(candidates, key=lambda e: (e.importance, e.confidence), reverse=True)[:limit]
```

- [ ] **Step 4: Add investigation prompt contract**

Add this constant to `news_intel/investigation.py`:

```python
INVESTIGATION_PROMPT = """你是个人科技情报系统的调查 agent。
目标: 对少量高价值事件做证据核验和历史关联，不写日报。

输入包括:
- event JSON
- related evidence JSON
- existing claims JSON

输出严格 JSON:
{
  "event_id": "...",
  "confidence": "low|medium|high",
  "additional_caveats": ["..."],
  "claim_links": {"claim-id": "supports|weakens|contradicts|neutral"},
  "reasoning_summary": "不超过120字，说明证据如何影响判断"
}

规则:
- 优先寻找一手来源。
- 找不到一手来源时，明确说明证据来自二手报道。
- 不根据单一社区讨论建立高置信判断。
- 不创造不存在的历史关联。
"""
```

- [ ] **Step 5: Add CLI investigation stage**

Extend `news_intel/cli.py` so `stage investigate --date YYYY-MM-DD`:

- Reads daily events and evidence.
- Selects events with `select_events_for_investigation`.
- Calls the strong model client configured by `STRONG_LLM_MODEL` when available.
- Updates daily event `confidence`, `claim_links`, and caveats from validated JSON.
- Writes the revised events back to `data/events/YYYY-MM-DD.jsonl`.
- If `STRONG_LLM_MODEL` is not configured, writes `state/investigation/YYYY-MM-DD-skipped.json` with selected event IDs and reason `STRONG_LLM_MODEL not configured`.

- [ ] **Step 6: Verify tests pass**

Run: `python3.11 -m pytest tests/test_extraction.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add news_intel/investigation.py news_intel/cli.py tests/test_extraction.py
git commit -m "feat: add targeted investigation stage"
```

---

## Task 11: Generate Push-First Daily Briefs

**Files:**
- Create: `news_intel/briefing.py`
- Create: `tests/test_briefing.py`

- [ ] **Step 1: Write briefing tests**

```python
# tests/test_briefing.py
from news_intel.briefing import render_daily_brief
from news_intel.models import Event, Evidence, SourceHealth, SourceTier


def test_daily_brief_contains_evidence_and_source_health():
    event = Event(
        id="evt-001",
        date="2026-06-01",
        title="OpenAI introduces Example Model",
        summary="OpenAI introduced an example model.",
        importance=4,
        confidence="high",
        source_tiers=[SourceTier.T0_FIRST_HAND],
        article_ids=["art-001"],
        entity_ids=["openai"],
        evidence_ids=["evd-001"],
        claim_links={"claim-agentic-coding": "supports"},
    )
    evidence = {
        "evd-001": Evidence(
            id="evd-001",
            event_id="evt-001",
            source="OpenAI Blog",
            source_tier=SourceTier.T0_FIRST_HAND,
            url="https://openai.com/example",
            quote="OpenAI introduced an example model.",
        )
    }
    health = [
        SourceHealth(
            source="OpenAI Blog",
            tier=SourceTier.T0_FIRST_HAND,
            last_attempt_at="2026-06-01T08:30:00+08:00",
            last_success_at="2026-06-01T08:30:00+08:00",
            status="ok",
            fetched_count=1,
        )
    ]
    text = render_daily_brief("2026-06-01", [event], evidence, health)
    assert "# Personal Tech Radar · 2026-06-01" in text
    assert "Source health" in text
    assert "OpenAI Blog" in text
    assert "Evidence:" in text
    assert "https://openai.com/example" in text
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_briefing.py -v`

Expected: FAIL because `news_intel.briefing` does not exist.

- [ ] **Step 3: Implement daily brief renderer**

```python
# news_intel/briefing.py
from __future__ import annotations

from news_intel.models import Event, Evidence, SourceHealth


def render_daily_brief(
    date: str,
    events: list[Event],
    evidence_by_id: dict[str, Evidence],
    source_health: list[SourceHealth],
) -> str:
    selected = sorted(events, key=lambda e: (e.importance, e.confidence), reverse=True)[:8]
    lines = [
        f"# Personal Tech Radar · {date}",
        "",
        f"> {len(events)} events processed · {len(selected)} selected",
        "",
        "## Source health",
        "",
    ]
    for health in sorted(source_health, key=lambda h: (h.tier.value, h.source)):
        suffix = f" · {health.failure_reason}" if health.failure_reason else ""
        lines.append(f"- {health.source}: {health.status} · {health.fetched_count} items{suffix}")
    lines.extend(["", "## Worth reading", ""])
    for index, event in enumerate(selected, 1):
        lines.append(f"### {index}. {event.title}")
        lines.append("")
        lines.append(f"Importance: {event.importance}/5 · Confidence: {event.confidence}")
        if event.claim_links:
            claim_text = ", ".join(f"{claim_id}={relation}" for claim_id, relation in event.claim_links.items())
            lines.append(f"History: {claim_text}")
        lines.append("")
        lines.append(event.summary)
        lines.append("")
        for evidence_id in event.evidence_ids[:2]:
            evidence = evidence_by_id.get(evidence_id)
            if evidence:
                lines.append(f"- Evidence: {evidence.source} ({evidence.source_tier.value}) - {evidence.url}")
                if evidence.quote:
                    lines.append(f"  Quote: {evidence.quote}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
```

- [ ] **Step 4: Add CLI brief stage**

Extend `news_intel/cli.py` so `stage brief --date YYYY-MM-DD`:

- Reads `data/events/YYYY-MM-DD.jsonl`.
- Reads `data/evidence.jsonl`.
- Reads `state/source_health.json`.
- Writes `brief/daily/YYYY-MM-DD.md`.
- Writes the same content to `report/YYYY-MM-DD.md` as a compatibility mirror.

- [ ] **Step 5: Verify briefing tests pass**

Run: `python3.11 -m pytest tests/test_briefing.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add news_intel/briefing.py news_intel/cli.py tests/test_briefing.py
git commit -m "feat: render evidence-first daily briefs"
```

---

## Task 12: Add Weekly and Monthly Synthesis

**Files:**
- Modify: `news_intel/briefing.py`
- Extend: `tests/test_briefing.py`

- [ ] **Step 1: Add weekly synthesis test**

```python
# append to tests/test_briefing.py
from news_intel.briefing import render_weekly_review
from news_intel.models import Claim


def test_weekly_review_renders_claim_updates():
    claim = Claim(
        id="claim-agentic-coding",
        title="Coding agents are becoming engineering environments",
        status="active",
        confidence="medium",
        summary="Multiple events support the shift from chat assistants to agentic coding environments.",
        supporting_event_ids=["evt-001", "evt-002"],
        updated_at="2026-06-01T09:00:00+08:00",
    )
    text = render_weekly_review("2026-W23", [claim], [])
    assert "# Weekly Tech Radar · 2026-W23" in text
    assert "Coding agents are becoming engineering environments" in text
    assert "active · medium" in text
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_briefing.py -v`

Expected: FAIL because `render_weekly_review` is missing.

- [ ] **Step 3: Implement weekly and monthly renderers**

Add to `news_intel/briefing.py`:

```python
from news_intel.models import Claim


def render_weekly_review(week_id: str, claims: list[Claim], notable_events: list[Event]) -> str:
    lines = [
        f"# Weekly Tech Radar · {week_id}",
        "",
        "## Claim updates",
        "",
    ]
    for claim in sorted(claims, key=lambda c: (c.status, c.id)):
        evidence_count = len(claim.supporting_event_ids) + len(claim.weakening_event_ids) + len(claim.contradicting_event_ids)
        if evidence_count == 0:
            continue
        lines.append(f"### {claim.title}")
        lines.append("")
        lines.append(f"Status: {claim.status} · {claim.confidence}")
        lines.append("")
        lines.append(claim.summary)
        lines.append("")
        lines.append(f"Supporting: {len(claim.supporting_event_ids)} · Weakening: {len(claim.weakening_event_ids)} · Contradicting: {len(claim.contradicting_event_ids)}")
        lines.append("")
    lines.append("## Notable events")
    lines.append("")
    for event in sorted(notable_events, key=lambda e: e.importance, reverse=True)[:10]:
        lines.append(f"- {event.title} ({event.importance}/5): {event.summary}")
    return "\n".join(lines).rstrip() + "\n"


def render_monthly_review(month_id: str, claims: list[Claim], notable_events: list[Event]) -> str:
    lines = [
        f"# Monthly Tech Radar · {month_id}",
        "",
        "## What changed",
        "",
    ]
    for claim in sorted(claims, key=lambda c: (c.confidence, c.id), reverse=True):
        if claim.status in {"active", "weakened", "contradicted"}:
            lines.append(f"- {claim.title}: {claim.status} · {claim.confidence}")
    lines.extend(["", "## Events to remember", ""])
    for event in sorted(notable_events, key=lambda e: e.importance, reverse=True)[:15]:
        lines.append(f"- {event.date} · {event.title}")
    return "\n".join(lines).rstrip() + "\n"
```

- [ ] **Step 4: Add CLI weekly/monthly support**

Extend CLI with:

- `stage weekly --date YYYY-MM-DD`: derives ISO week from date, reads claims and events from that week, writes `brief/weekly/YYYY-WW.md`.
- `stage monthly --date YYYY-MM-DD`: derives month from date, reads claims and events from that month, writes `brief/monthly/YYYY-MM.md`.

- [ ] **Step 5: Verify briefing tests pass**

Run: `python3.11 -m pytest tests/test_briefing.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add news_intel/briefing.py news_intel/cli.py tests/test_briefing.py
git commit -m "feat: render weekly and monthly radar reviews"
```

---

## Task 13: Add Delivery Layer

**Files:**
- Create: `news_intel/delivery.py`
- Create: `tests/test_delivery.py`
- Modify: `scripts/send_report.py`

- [ ] **Step 1: Write delivery tests**

```python
# tests/test_delivery.py
from news_intel.delivery import delivery_payload


def test_delivery_payload_contains_title_and_body():
    payload = delivery_payload("2026-06-01", "# Personal Tech Radar · 2026-06-01\n\nBody")
    assert payload["title"] == "Personal Tech Radar · 2026-06-01"
    assert payload["body"].startswith("# Personal Tech Radar")
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python3.11 -m pytest tests/test_delivery.py -v`

Expected: FAIL because `news_intel.delivery` does not exist.

- [ ] **Step 3: Implement payload helper**

```python
# news_intel/delivery.py
from __future__ import annotations


def delivery_payload(date: str, markdown: str) -> dict:
    first_line = next((line for line in markdown.splitlines() if line.startswith("# ")), f"# Personal Tech Radar · {date}")
    return {
        "title": first_line.removeprefix("# ").strip(),
        "body": markdown,
    }
```

- [ ] **Step 4: Update `scripts/send_report.py`**

Modify it to read from `brief/daily/YYYY-MM-DD.md` first. If that file does not exist, fall back to `report/YYYY-MM-DD.md`. Preserve existing Feishu sending behavior and success output.

- [ ] **Step 5: Add CLI delivery stage**

Extend `news_intel/cli.py` so `stage deliver --date YYYY-MM-DD` invokes `scripts/send_report.py YYYY-MM-DD` unless `--skip-delivery` was passed to `run`.

- [ ] **Step 6: Verify delivery tests pass**

Run: `python3.11 -m pytest tests/test_delivery.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add news_intel/delivery.py news_intel/cli.py scripts/send_report.py tests/test_delivery.py
git commit -m "feat: deliver daily brief from push-first artifact"
```

---

## Task 14: Rebuild Site Around Radar Artifacts

**Files:**
- Modify: `site/lib/reports.js`
- Create: `site/lib/radar.js`
- Modify: `site/app/page.js`
- Create: `site/app/topics/page.js`
- Create: `site/app/entities/[id]/page.js`
- Create: `site/app/claims/[id]/page.js`
- Modify: `site/app/feed.xml/route.js`
- Modify: `site/app/globals.css`

- [ ] **Step 1: Add radar data reader**

Create `site/lib/radar.js` with functions:

```js
import fs from 'fs'
import path from 'path'

const ROOT = path.join(process.cwd(), '..')

function readJsonl(filePath) {
  if (!fs.existsSync(filePath)) return []
  return fs.readFileSync(filePath, 'utf-8')
    .split('\n')
    .filter(Boolean)
    .map(line => JSON.parse(line))
}

export function getLatestDailyBriefs(limit = 20) {
  const dir = path.join(ROOT, 'brief', 'daily')
  if (!fs.existsSync(dir)) return []
  return fs.readdirSync(dir)
    .filter(name => name.endsWith('.md'))
    .sort()
    .reverse()
    .slice(0, limit)
    .map(name => ({
      date: name.replace('.md', ''),
      markdown: fs.readFileSync(path.join(dir, name), 'utf-8'),
    }))
}

export function getAllEntities() {
  return readJsonl(path.join(ROOT, 'data', 'entities.jsonl'))
}

export function getAllClaims() {
  return readJsonl(path.join(ROOT, 'data', 'claims.jsonl'))
}

export function getAllEvents() {
  const dir = path.join(ROOT, 'data', 'events')
  if (!fs.existsSync(dir)) return []
  return fs.readdirSync(dir)
    .filter(name => name.endsWith('.jsonl'))
    .flatMap(name => readJsonl(path.join(dir, name)))
}
```

- [ ] **Step 2: Change homepage role**

Modify `site/app/page.js` so the first viewport shows:

- Latest daily brief.
- Source health summary.
- Top active claims.
- Links to topics/entities/claims.

Keep the existing layout and typography. Remove language that frames the site as only a daily report archive.

- [ ] **Step 3: Add entity and claim pages**

`site/app/entities/[id]/page.js`:

- Reads entity by id from `getAllEntities`.
- Reads related events from `getAllEvents`.
- Renders a timeline sorted by date descending.

`site/app/claims/[id]/page.js`:

- Reads claim by id from `getAllClaims`.
- Renders status, confidence, summary, supporting events, weakening events, and contradicting events.

- [ ] **Step 4: Update feed route**

Modify `site/app/feed.xml/route.js` to read from `brief/daily/*.md` instead of `report/*.md`. Keep the feed item count at 20.

- [ ] **Step 5: Verify Next build**

Run: `npm --prefix site run build`

Expected: Next build succeeds and Pagefind indexes `site/out`.

- [ ] **Step 6: Commit**

```bash
git add site/lib/radar.js site/app site/lib/reports.js site/app/globals.css
git commit -m "feat: rebuild site around radar artifacts"
```

---

## Task 15: Add Full Pipeline Runner and Cron Contract

**Files:**
- Modify: `news_intel/cli.py`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `.agents/skills/news-intel/SKILL.md`

- [ ] **Step 1: Implement `run` command**

Modify `news_intel/cli.py` so `run --date YYYY-MM-DD` runs stages in this order:

```text
fetch
ingest
extract
cluster
investigate
knowledge
brief
deliver
site
```

If `--skip-delivery` is set, skip `deliver`. If one source fails during `fetch`, continue. If `extract` fails for one article, continue. If `cluster`, `knowledge`, or `brief` fails, stop with non-zero exit because downstream artifacts would be misleading.

- [ ] **Step 2: Add dry execution test**

Add to `tests/test_cli.py`:

```python
def test_run_order_is_stable():
    from news_intel.cli import PIPELINE_ORDER
    assert PIPELINE_ORDER == [
        "fetch",
        "ingest",
        "extract",
        "cluster",
        "investigate",
        "knowledge",
        "brief",
        "deliver",
        "site",
    ]
```

- [ ] **Step 3: Update README**

Document:

- Personal Tech Radar positioning.
- Source tier model.
- Daily, weekly, and monthly artifact locations.
- Full command: `python3.11 -m news_intel.cli run --date YYYY-MM-DD`.
- Server cron command with proxy note.
- GitHub Pages role as archive/research surface.

- [ ] **Step 4: Update agent instructions**

Update `AGENTS.md` and `.agents/skills/news-intel/SKILL.md` so daily work uses the new CLI pipeline. Remove instructions that say `scripts/digest.py` or agent role prompts are the main generator. Keep agent role prompts as fallback investigation guidance only.

- [ ] **Step 5: Run unit tests**

Run: `python3.11 -m pytest -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add news_intel/cli.py tests/test_cli.py README.md AGENTS.md .agents/skills/news-intel/SKILL.md
git commit -m "feat: wire full personal radar pipeline"
```

---

## Task 16: Backfill Existing May 2026 Data

**Files:**
- Create: `scripts/backfill_radar.py`
- Generated: `data/articles/*.jsonl`
- Generated: `data/candidates/*.jsonl`
- Generated: `data/events/*.jsonl`
- Generated: `data/entities.jsonl`
- Generated: `data/claims.jsonl`
- Generated: `data/evidence.jsonl`
- Generated: `brief/daily/*.md`

- [ ] **Step 1: Create backfill script**

```python
# scripts/backfill_radar.py
#!/usr/bin/env python3.11
from __future__ import annotations

import argparse
import subprocess


def date_range(start: str, end: str) -> list[str]:
    from datetime import date, timedelta

    current = date.fromisoformat(start)
    final = date.fromisoformat(end)
    days = []
    while current <= final:
        days.append(current.isoformat())
        current += timedelta(days=1)
    return days


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    args = parser.parse_args()

    for day in date_range(args.start, args.end):
        stages = ["ingest", "extract", "cluster", "investigate", "knowledge", "brief"]
        for stage in stages:
            subprocess.run(["python3.11", "-m", "news_intel.cli", "stage", stage, "--date", day], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run backfill**

Run: `python3.11 scripts/backfill_radar.py --start 2026-05-01 --end 2026-05-26`

Expected:

- Daily article, candidate, event, and brief artifacts exist for dates with raw data.
- `data/entities.jsonl`, `data/claims.jsonl`, and `data/evidence.jsonl` exist.

- [ ] **Step 3: Build the site**

Run: `npm --prefix site run build`

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add scripts/backfill_radar.py data brief report site/out
git commit -m "data: backfill personal radar artifacts for existing archive"
```

---

## Task 17: Verification and Deployment

**Files:**
- No new source files.

- [ ] **Step 1: Run all Python tests**

Run: `python3.11 -m pytest -v`

Expected: PASS.

- [ ] **Step 2: Run a no-delivery full pipeline**

Run: `python3.11 -m news_intel.cli run --date 2026-06-01 --skip-delivery`

Expected:

- Raw files under `raw/2026/06/01/`.
- `state/source_health.json`.
- `data/articles/2026-06-01.jsonl`.
- `data/candidates/2026-06-01.jsonl`.
- `data/events/2026-06-01.jsonl`.
- `brief/daily/2026-06-01.md`.
- `report/2026-06-01.md`.

- [ ] **Step 3: Build site**

Run: `npm --prefix site run build`

Expected: PASS.

- [ ] **Step 4: Inspect the daily brief manually**

Open `brief/daily/2026-06-01.md` and verify:

- Five to eight items are selected when enough events exist.
- Each selected item has evidence URL and source tier.
- Source health section shows failed or stale T0 sources.
- No item reads like a generic AI-written news paragraph without evidence.

- [ ] **Step 5: Commit verification artifact updates**

```bash
git add state data brief report
git commit -m "verify: run personal radar pipeline for 2026-06-01"
```

- [ ] **Step 6: Push**

```bash
node scripts/git_push.js
```

Expected: output contains `push ok`.

---

## Self-Review

**Spec coverage:**

- Core rationale is preserved in `docs/strategy/personal-tech-radar.md`.
- First-hand source reliability and proxy instability are handled by source tiers and source health.
- AI depth is routed across deterministic processing, lightweight extraction, and targeted investigation.
- Historical synthesis is implemented through events, entities, claims, evidence, daily briefs, weekly reviews, and monthly reviews.
- The primary output is push-first daily brief, with the site serving archive, timeline, entity, and claim exploration.
- The plan covers migration from existing raw/report artifacts and updates agent instructions.

**Placeholder scan:**

- The document does not contain open-ended placeholder instructions or unresolved placeholder paths.
- Every task has explicit files, commands, and expected outcomes.

**Type consistency:**

- `SourceTier`, `Article`, `Candidate`, `Evidence`, `Event`, `Entity`, `Claim`, and `SourceHealth` are defined before later tasks consume them.
- CLI stage names are stable across tests, docs, and pipeline order.
- Artifact paths are consistent across Python stages and Next.js site readers.
