---
name: news-intel
description: |
  Personal Tech Radar entrypoint. Trigger when the user asks for "发资讯",
  "今日日报", "科技新闻", "资讯群", "日报", or asks to run/update the radar.
---

# News Intel — Personal Tech Radar

## Paths

- Server: `/root/.openclaw/workspace/news-intel/`
- Local: `/Users/zcs/code2/news-intel/`

Use the active workspace path.

## Main Command

```bash
python3.11 -m news_intel.cli run --date YYYY-MM-DD
```

For local validation:

```bash
python3 -m news_intel.cli run --date YYYY-MM-DD --skip-delivery
```

## Pipeline

```text
fetch -> ingest -> extract -> cluster -> investigate -> knowledge -> brief -> deliver -> site
```

## Outputs

- `raw/YYYY/MM/DD/`: raw article archive
- `state/source_health.json`: source health
- `data/articles/YYYY-MM-DD.jsonl`: normalized articles
- `data/candidates/YYYY-MM-DD.jsonl`: extracted candidates
- `data/events/YYYY-MM-DD.jsonl`: clustered events
- `data/evidence.jsonl`: evidence snippets
- `data/entities.jsonl`: entity timelines
- `data/claims.jsonl`: tracked claims
- `brief/daily/YYYY-MM-DD.md`: daily push brief
- `brief/weekly/YYYY-WW.md`: weekly review
- `brief/monthly/YYYY-MM.md`: monthly review

## Rules

- Prefer first-hand and high-quality sources.
- Keep source health explicit, especially proxy failures.
- Use lightweight LLM extraction for article-level structure.
- Use strong model investigation only for a small number of high-value events.
- Do not generate prose without evidence links and confidence.
- Keep the daily brief concise.
