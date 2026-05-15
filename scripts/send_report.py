#!/usr/bin/env python3.11
"""发送今日日报到飞书资讯群"""
import urllib.request, json, ssl, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKDIR = Path("/root/.openclaw/workspace/news-intel")
APP_ID = "cli_a9257489d7f95cb0"
APP_SECRET = "Z0yMxON3tFvMs3hrPvnsjeUQCc7wCZwW"
CHAT_ID = "oc_d170dda09264716d786cd28cc48e5f78"
CST = timezone(timedelta(hours=8))

date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now(CST).strftime("%Y-%m-%d")
report_path = WORKDIR / "report" / f"{date_str}.md"

if not report_path.exists():
    print(f"ERROR: report not found: {report_path}", file=sys.stderr)
    sys.exit(1)

ctx = ssl._create_unverified_context()

# 获取 token
r = urllib.request.urlopen(urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
    headers={"Content-Type": "application/json"}
), context=ctx, timeout=15)
token = json.loads(r.read())["tenant_access_token"]

# 发消息
content = report_path.read_text()
r2 = urllib.request.urlopen(urllib.request.Request(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
    data=json.dumps({
        "receive_id": CHAT_ID,
        "msg_type": "text",
        "content": json.dumps({"text": content})
    }).encode(),
    headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}
), context=ctx, timeout=15)
result = json.loads(r2.read())

if result.get("code") == 0:
    print(f"send ok: message_id={result.get('data',{}).get('message_id','')}")
else:
    print(f"send failed: code={result.get('code')} msg={result.get('msg')}", file=sys.stderr)
    sys.exit(1)
