# Personal Tech Radar Architecture

## Purpose

News Intel turns noisy technology feeds into a small evidence-first radar. The daily brief is the primary reading surface; the website is a research console for history, source health, entities, events, and claims.

## Pipeline

```text
fetch -> ingest -> extract -> cluster -> investigate -> knowledge -> brief -> deliver -> site
```

- `fetch`: read tiered sources from `sources/feeds.yaml`, write raw article markdown, update source health.
- `ingest`: parse raw markdown into normalized `Article` rows.
- `extract`: call an OpenAI-compatible model and produce validated `Candidate` rows.
- `cluster`: merge candidates into `Event` rows and append `Evidence` rows.
- `investigate`: optionally use a stronger model for selected high-value events.
- `knowledge`: update `Entity` timelines and `Claim` status.
- `brief`: render the daily Markdown brief.
- `deliver`: send the daily brief to Feishu.
- `site`: build the static research console.

## Data Contract

Generated artifacts live under:

```text
raw/YYYY/MM/DD/
state/source_health.json
data/articles/YYYY-MM-DD.jsonl
data/candidates/YYYY-MM-DD.jsonl
data/events/YYYY-MM-DD.jsonl
data/evidence.jsonl
data/entities.jsonl
data/claims.jsonl
brief/daily/YYYY-MM-DD.md
brief/weekly/YYYY-WW.md
brief/monthly/YYYY-MM.md
```

The site reads only `brief/`, `data/`, and `state/`. Feishu delivery reads only `brief/daily/YYYY-MM-DD.md`.

## Configuration

`.env` is loaded automatically. Required for full operation:

```text
LLM_API_KEY
LLM_API_HOST
LLM_MODEL
HTTPS_PROXY
FEISHU_APP_ID
FEISHU_APP_SECRET
FEISHU_CHAT_ID
```

`STRONG_LLM_MODEL` is optional and only affects investigation.
