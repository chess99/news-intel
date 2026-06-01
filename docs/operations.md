# Operations

## Local Validation

```bash
python3 -m news_intel.cli run --date YYYY-MM-DD --skip-delivery
python3 -m pytest -v
npm --prefix site run build
```

Use `--skip-delivery` locally unless Feishu credentials are intentionally configured.

## Server Cron

```cron
30 8 * * * cd /root/.openclaw/workspace/news-intel && python3.11 -m news_intel.cli run --date $(TZ=Asia/Shanghai date +\%F) >> /tmp/news-radar.log 2>&1
```

## Failure Handling

- Source fetch failures should be recorded in `state/source_health.json`.
- If extraction produces zero candidates from non-empty article input, the pipeline fails before rendering an empty brief.
- Missing Feishu configuration fails the `deliver` stage with an explicit error.
- Use `--skip-delivery` for dry runs and debugging.

## Site Deployment

GitHub Pages builds the Next.js static site when `brief/**`, `data/**`, `state/source_health.json`, or `site/**` changes on `main`.
