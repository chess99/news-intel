#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/zcs/code2/news-intel"
PYTHON="/Users/zcs/miniforge3/bin/python3"
export PATH="/opt/homebrew/bin:/Users/zcs/.nvm/versions/node/v24.13.0/bin:/Users/zcs/miniforge3/bin:/Users/zcs/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export TZ="Asia/Shanghai"

DATE="${1:-$(date +%F)}"
SKIP_DELIVERY="${NEWS_INTEL_SKIP_DELIVERY:-0}"
LOG_DIR="$ROOT/logs/cron"
RUN_DIR="$ROOT/.run"
LOG_FILE="$LOG_DIR/news-intel-$DATE.log"
LOCK_DIR="$RUN_DIR/news-intel.lock"

mkdir -p "$LOG_DIR" "$RUN_DIR"

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "news-intel is already running; skip $DATE" >> "$LOG_FILE"
  exit 0
fi
trap 'rmdir "$LOCK_DIR"' EXIT

{
  echo "[$(date '+%F %T %Z')] start news-intel date=$DATE"
  cd "$ROOT"
  if [[ "$SKIP_DELIVERY" == "1" ]]; then
    "$PYTHON" -m news_intel.cli run --date "$DATE" --skip-delivery
  else
    "$PYTHON" -m news_intel.cli run --date "$DATE"
  fi
  echo "[$(date '+%F %T %Z')] done news-intel date=$DATE"
} >> "$LOG_FILE" 2>&1
