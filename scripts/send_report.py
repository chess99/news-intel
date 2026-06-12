#!/usr/bin/env python3.11
"""Send the daily Personal Tech Radar brief to Feishu."""
from __future__ import annotations

import json
import ssl
import sys
import urllib.request
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from news_intel.config import load_env_file
from news_intel.delivery import brief_path, delivery_payload, require_feishu_config

CST = timezone(timedelta(hours=8))


def post_json(url: str, payload: dict, headers: dict[str, str] | None = None) -> dict:
    ctx = ssl._create_unverified_context()
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    with urllib.request.urlopen(request, context=ctx, timeout=15) as response:
        return json.loads(response.read())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send the daily Personal Tech Radar brief to Feishu.")
    parser.add_argument("date", nargs="?", help="Brief date in YYYY-MM-DD format. Defaults to today in Asia/Shanghai.")
    parser.add_argument("--dry-run", action="store_true", help="Validate config and brief payload without sending.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    date_str = args.date or datetime.now(CST).strftime("%Y-%m-%d")
    load_env_file(ROOT / ".env")

    try:
        config = require_feishu_config()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    path = brief_path(ROOT, date_str)
    if not path.exists():
        print(f"ERROR: daily brief not found: {path}", file=sys.stderr)
        return 1

    content = path.read_text(encoding="utf-8")
    payload = delivery_payload(date_str, content)
    if args.dry_run:
        print(f"dry-run ok: title={payload['title']} chars={len(payload['body'])} chat_id_set=yes")
        return 0

    token_result = post_json(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        {"app_id": config["FEISHU_APP_ID"], "app_secret": config["FEISHU_APP_SECRET"]},
    )
    token = token_result["tenant_access_token"]
    result = post_json(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        {
            "receive_id": config["FEISHU_CHAT_ID"],
            "msg_type": "text",
            "content": json.dumps({"text": content}),
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    if result.get("code") == 0:
        print(f"send ok: message_id={result.get('data', {}).get('message_id', '')}")
        return 0
    print(f"send failed: code={result.get('code')} msg={result.get('msg')}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
