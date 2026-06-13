# Operations

## Local Validation

```bash
python3 -m news_intel.cli run --date YYYY-MM-DD --skip-delivery
python3 -m pytest -v
npm --prefix site run build
```

Use `--skip-delivery` locally unless Feishu credentials are intentionally configured.

## Local Cron

```cron
0 9 * * * /Users/zcs/code2/news-intel/scripts/run_local_daily.sh
```

Manual local run:

```bash
/Users/zcs/code2/news-intel/scripts/run_local_daily.sh YYYY-MM-DD
```

Manual local run without Feishu delivery:

```bash
NEWS_INTEL_SKIP_DELIVERY=1 /Users/zcs/code2/news-intel/scripts/run_local_daily.sh YYYY-MM-DD
```

Cron logs are written to:

```text
logs/cron/news-intel-YYYY-MM-DD.log
```

The runner uses `/Users/zcs/miniforge3/bin/python3` and loads `.env` through the Python pipeline.

Default daily execution order:

```text
fetch -> ingest -> extract -> cluster -> knowledge -> editorial -> brief -> deliver -> site
```

`investigate` remains available as a manual stage, but it is no longer in the default daily cron path.

## LLM Provider

The daily path uses LLM only for the batch `editorial` pass. Article extraction is rules-based so cron runtime does not grow linearly with article count.

API mode:

```env
LLM_PROVIDER=openai
LLM_API_HOST=https://api.openai.com
LLM_API_KEY=...
LLM_MODEL=...
```

Local command mode:

```env
LLM_PROVIDER=command
LLM_COMMAND=/opt/homebrew/bin/codex -s read-only -a never exec --ephemeral
LLM_COMMAND_INPUT=argv
LLM_COMMAND_TIMEOUT=180
```

If `mc` is installed locally, command mode can be switched to:

```env
LLM_PROVIDER=command
LLM_COMMAND=mc --code -p
LLM_COMMAND_INPUT=argv
```

## Failure Handling

- Source fetch failures should be recorded in `state/source_health.json`.
- If extraction produces zero candidates from non-empty article input, the pipeline fails before rendering an empty brief.
- If the editorial LLM pass fails, the pipeline writes a deterministic rules-based editorial file and still renders the daily brief.
- Missing Feishu configuration fails the `deliver` stage with an explicit error.
- Use `scripts/send_report.py --dry-run YYYY-MM-DD` to validate Feishu config and payload without sending.
- Use `--skip-delivery` for dry runs and debugging.

## Site Deployment

GitHub Pages builds the Next.js static site when `brief/**`, `data/**`, `state/source_health.json`, or `site/**` changes on `main`.
