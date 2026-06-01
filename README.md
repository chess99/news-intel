# news-intel

Personal Tech Radar: a personal technology intelligence pipeline. It watches tiered sources, records source health, extracts structured events and evidence, updates entities and long-running claims, then produces a concise daily brief for push delivery and a static research console.

Online archive: [news.cearl.cc](https://news.cearl.cc/)

## Core Flow

```text
fetch -> ingest -> extract -> cluster -> investigate -> knowledge -> brief -> deliver -> site
```

Primary output:

- `brief/daily/YYYY-MM-DD.md`: daily push brief
- `brief/weekly/YYYY-WW.md`: weekly claim review
- `brief/monthly/YYYY-MM.md`: monthly review
- `data/articles/YYYY-MM-DD.jsonl`: normalized articles
- `data/candidates/YYYY-MM-DD.jsonl`: extracted candidates
- `data/events/YYYY-MM-DD.jsonl`: clustered events
- `data/evidence.jsonl`: evidence snippets
- `data/entities.jsonl`: entity timelines
- `data/claims.jsonl`: tracked claims
- `state/source_health.json`: source health

## Setup

```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```bash
LLM_API_HOST=https://api.minimaxi.com
LLM_MODEL=MiniMax-M2.7
LLM_API_KEY=your_openai_compatible_api_key
HTTPS_PROXY=http://127.0.0.1:7890

FEISHU_APP_ID=
FEISHU_APP_SECRET=
FEISHU_CHAT_ID=
```

`MINIMAX_API_KEY` is still accepted for older MiniMax setups, but `LLM_API_KEY` is preferred.

## Daily Use

Local run without sending:

```bash
python3 -m news_intel.cli run --date YYYY-MM-DD --skip-delivery
```

Server run with Feishu delivery:

```bash
python3.11 -m news_intel.cli run --date YYYY-MM-DD
```

Run one stage:

```bash
python3 -m news_intel.cli stage fetch --date YYYY-MM-DD
python3 -m news_intel.cli stage brief --date YYYY-MM-DD
python3 -m news_intel.cli stage site --date YYYY-MM-DD
```

## Site

```bash
npm --prefix site run dev
npm --prefix site run build
```

The site reads only `brief/`, `data/`, and `state/`. It is a research console for daily briefs, source health, events, entities, claims, search, RSS, and historical exploration.

## Automation

```cron
30 8 * * * cd /root/.openclaw/workspace/news-intel && python3.11 -m news_intel.cli run --date $(TZ=Asia/Shanghai date +\%F) >> /tmp/news-radar.log 2>&1
```

GitHub Pages deploys when `brief/**`, `data/**`, `state/source_health.json`, or `site/**` changes on `main`.

## Repository Shape

```text
news_intel/          pipeline package
scripts/fetch.py     RSS/full-text fetch entrypoint
scripts/send_report.py
sources/feeds.yaml   tiered source configuration
raw/                 generated raw article archive
data/                generated structured artifacts
state/               generated operational state
brief/               generated human-facing briefs
site/                Next.js static research console
docs/                architecture and strategy notes
tests/               pytest coverage
```

Generated runtime directories start empty after a clean checkout and are populated by the pipeline.
