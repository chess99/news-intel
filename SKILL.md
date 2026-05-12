---
name: news-intel
description: |
  科技资讯日报生成入口。每天 09:00 CST 由 cron 触发。
  当用户提到"发资讯"、"今日日报"、"科技新闻"、"资讯群"、"日报"时触发。
  三阶段流程：orchestrator 选文章 → analyst 并行分析 → reporter 生成日报。
---

# News Intel — 日报生成流程

## 工作区路径

- 服务器: `/root/.openclaw/workspace/news-intel/`
- 本地: `/Users/zcs/code2/news-intel/`

使用当前实际运行环境的路径。

## Pipeline（每日 09:00 CST 触发）

### Stage 1 — Orchestrator（本 agent 执行）

读取 `.claude/skills/news-intel/roles/orchestrator.md` 并完整执行：
- 获取今日 `raw/YYYY/MM/DD/` 下所有原文
- 快速评估，选出 15-25 篇值得分析的文章
- 为每篇提取关键词（专有名词）
- 以子 agent 方式派发 Analyst 任务（见下）
- 将所有分析结果写入 `digest/YYYY-MM-DD.md`

### Stage 2 — Analyst（子 agent 并行执行）

每篇文章独立运行一个子 agent，按 `.claude/skills/news-intel/roles/analyst.md` 执行：
- 读取完整原文
- 用关键词 grep `digest/` 历史文件
- 写深度分析（核心事件 / 原文引用 / **真实历史关联** / 驱动力 / 批判 / 评分）
- 返回 Markdown 分析给 orchestrator

最多同时 5-8 个并行子 agent，分批处理。

### Stage 3 — Reporter（本 agent 执行）

读取 `.claude/skills/news-intel/roles/reporter.md` 并完整执行：
- 读取 `digest/YYYY-MM-DD.md`
- 生成日报（格式见 reporter.md）
- 存档到 `report/YYYY-MM-DD.md`
- 发送到飞书群（feishu_chat 工具）
- 更新静态站点（build_site.py）
- git commit + push

## 手动触发抓取

如果今日 `raw/` 还没有原文（fetch.py 未跑），先运行：

```bash
cd <工作区路径>
source .env
python3.11 scripts/fetch.py
```

## 注意事项

- `.env` 文件包含 API 密钥，脚本自动加载
- `scripts/digest.py` 已废弃，不要再用它生成分析
- 飞书发送必须用 `feishu_chat` 工具（不要 curl）
- 代理: `http://127.0.0.1:7890`（境外信源需要）

## 废弃组件（勿用）

- `scripts/digest.py` — 已废弃，由 analyst role 替代
- `scripts/kb_update.py` — 已废弃，不再需要 KB 维护
- `scripts/cluster.py` — 已废弃，从未接入主流程
- `kb/events.jsonl` — 停止更新，历史存档保留
