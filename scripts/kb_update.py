#!/usr/bin/env python3.11
# DEPRECATED: Knowledge base maintenance is no longer needed.
# The analyst role grep-searches digest/ files directly. Kept for reference only.
"""
kb_update.py — 从 digest sidecar JSONL 中提取高分事件，维护 kb/events.jsonl（30天滚动窗口）

用法:
    python3.11 scripts/kb_update.py [--date YYYY-MM-DD]

依赖: digest.py 先写出 digest/YYYY-MM-DD.jsonl（sidecar）
"""
import sys, json
from datetime import datetime, timezone, timedelta
from pathlib import Path
import argparse

WORKDIR = Path(__file__).parent.parent
DIGEST_DIR = WORKDIR / "digest"
KB_DIR = WORKDIR / "kb"
KB_FILE = KB_DIR / "events.jsonl"
WINDOW_DAYS = 30
MIN_SCORE = 4
CST = timezone(timedelta(hours=8))


def main():
    parser = argparse.ArgumentParser(description="Update knowledge base from digest sidecar")
    parser.add_argument("--date", default=None, help="日期 YYYY-MM-DD（默认今天）")
    args = parser.parse_args()

    today = datetime.now(CST)
    date_str = args.date or today.strftime("%Y-%m-%d")

    # 滑动窗口锚点: max(today, digest_date)，防止回填时截掉历史
    try:
        digest_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=CST)
    except ValueError:
        digest_date = today
    anchor_date = max(today, digest_date)
    cutoff = (anchor_date - timedelta(days=WINDOW_DAYS)).strftime("%Y-%m-%d")

    # 读取 sidecar JSONL
    sidecar = DIGEST_DIR / f"{date_str}.jsonl"
    if not sidecar.exists():
        print(f"[WARN] sidecar 不存在: {sidecar}，跳过 kb 更新", file=sys.stderr)
        print(f"请先运行: python3.11 scripts/digest.py --date {date_str}", file=sys.stderr)
        sys.exit(0)

    new_events = []
    with sidecar.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get("score", 0) >= MIN_SCORE:
                    new_events.append(record)
            except json.JSONDecodeError as e:
                print(f"[WARN] sidecar 解析失败: {e}", file=sys.stderr)

    print(f"[INFO] sidecar 中评分≥{MIN_SCORE} 的事件: {len(new_events)} 条", file=sys.stderr)

    # 读取现有 kb，保留 cutoff 后的记录
    existing = []
    if KB_FILE.exists():
        with KB_FILE.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if rec.get("date", "") >= cutoff:
                        existing.append(rec)
                except json.JSONDecodeError:
                    pass

    # 去重: 按 event_id（同一天同一文章不重复追加）
    existing_ids = {r["event_id"] for r in existing}
    to_add = [e for e in new_events if e["event_id"] not in existing_ids]

    all_events = existing + to_add
    all_events.sort(key=lambda r: r.get("date", ""), reverse=True)

    # 原子写：先写临时文件，再替换
    KB_DIR.mkdir(parents=True, exist_ok=True)
    tmp = KB_FILE.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for rec in all_events:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    tmp.replace(KB_FILE)

    print(
        f"[DONE] kb 更新: +{len(to_add)} 条新增，共 {len(all_events)} 条"
        f"（窗口: {cutoff} 至今）",
        file=sys.stderr
    )


if __name__ == "__main__":
    main()
