---
name: news-intel
description: |
  科技资讯日报生成入口。每天 09:00 CST 由 cron 触发。
  当用户提到"发资讯"、"今日日报"、"科技新闻"、"资讯群"时触发。
---

# News Intel — 科技资讯工作区

> ⚠️ 新流程：见 `.claude/skills/news-intel/SKILL.md`
> 本文件保留用于 OpenClaw 向后兼容。

## 工作区路径

服务器: `/root/.openclaw/workspace/news-intel/`
本地: `/Users/zcs/code2/news-intel/`

## 日常任务

按 `.claude/skills/news-intel/SKILL.md` 中的三阶段流程执行：

1. **Orchestrator**（本 agent）：选文章 + 提取关键词 + 派发子 agent
2. **Analyst**（子 agent，并行）：grep 历史 digest + 深度分析
3. **Reporter**（本 agent）：汇总 → 日报 → 飞书 → git push

每个阶段的详细说明见对应的 role 文件：
- `.claude/skills/news-intel/roles/orchestrator.md`
- `.claude/skills/news-intel/roles/analyst.md`
- `.claude/skills/news-intel/roles/reporter.md`

## 手动触发数据采集

```bash
cd /root/.openclaw/workspace/news-intel
source .env
python3.11 scripts/fetch.py
```

## 废弃组件（勿用）

- `scripts/digest.py` — 已废弃，由 analyst role 替代
- `scripts/kb_update.py` — 已废弃，不再需要 KB 维护
- `scripts/cluster.py` — 已废弃，从未接入主流程
- `kb/events.jsonl` — 停止更新，历史存档保留
