# News Intel — Personal Tech Radar

## Workspace Paths

- Server: `/root/.openclaw/workspace/news-intel/`
- Local: `/Users/zcs/code2/news-intel/`

Use the actual current workspace path when running commands.

## Direction

This repository is a Personal Tech Radar. It is not a generic news site. The useful product is a concise daily push brief backed by first-hand or high-quality sources, explicit source health, structured events, evidence, entities, and long-running claims.

Core strategy: `docs/strategy/personal-tech-radar.md`.

## Daily Pipeline

```bash
python3.11 -m news_intel.cli run --date YYYY-MM-DD
```

Local validation without Feishu delivery:

```bash
python3 -m news_intel.cli run --date YYYY-MM-DD --skip-delivery
```

Local cron runner:

```bash
/Users/zcs/code2/news-intel/scripts/run_local_daily.sh YYYY-MM-DD
```

Execution order:

```text
fetch -> ingest -> extract -> cluster -> investigate -> knowledge -> brief -> deliver -> site
```

## Artifacts

```text
raw/YYYY/MM/DD/                  raw article archive
state/source_health.json         source health state
data/articles/YYYY-MM-DD.jsonl   normalized articles
data/candidates/YYYY-MM-DD.jsonl extracted candidates
data/events/YYYY-MM-DD.jsonl     clustered events
data/evidence.jsonl              evidence snippets
data/entities.jsonl              entity timelines
data/claims.jsonl                tracked claims
brief/daily/YYYY-MM-DD.md        daily push brief
brief/weekly/YYYY-WW.md          weekly review
brief/monthly/YYYY-MM.md         monthly review
site/                            static research console
```

## Operating Notes

- `.env` is loaded automatically.
- Use `LLM_PROVIDER=openai` with `LLM_API_KEY`, `LLM_API_HOST`, and `LLM_MODEL` for OpenAI-compatible extraction.
- Use `LLM_PROVIDER=command` with `LLM_COMMAND` when delegating extraction to a local agent command such as `mc --code -p` or `codex exec`.
- Use `STRONG_LLM_MODEL` only for targeted investigation.
- Use `HTTPS_PROXY=http://127.0.0.1:7890` when the source needs mihomo.
- Feishu delivery requires `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, and `FEISHU_CHAT_ID`.
- A source failure must appear in `state/source_health.json`; do not silently hide first-hand source failure.
- The daily brief should stay small and evidence-first.
