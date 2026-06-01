---
name: news-intel
description: |
  Personal Tech Radar 入口。每天 09:00 CST 由 cron 触发。
  当用户提到"发资讯"、"今日日报"、"科技新闻"、"资讯群"、"日报"时触发。
  主流程使用 news_intel CLI；agent roles 仅作为高价值事件调查和人工兜底参考。
---

# News Intel — Personal Tech Radar 流程

## 工作区路径

- 服务器: `/root/.openclaw/workspace/news-intel/`
- 本地: `/Users/zcs/code2/news-intel/`

使用当前实际运行环境的路径。

## Pipeline（每日 09:00 CST 触发）

主流程：

```bash
python3.11 -m news_intel.cli run --date YYYY-MM-DD
```

本地验证可跳过发送：

```bash
python3.11 -m news_intel.cli run --date YYYY-MM-DD --skip-delivery
```

执行顺序：

```
fetch → ingest → extract → cluster → investigate → knowledge → brief → deliver → site
```

## 产物

- `raw/YYYY/MM/DD/`: 原文归档
- `state/source_health.json`: 信源健康状态
- `data/articles/YYYY-MM-DD.jsonl`: 标准化文章
- `data/candidates/YYYY-MM-DD.jsonl`: 候选事件
- `data/events/YYYY-MM-DD.jsonl`: 聚类后的事件
- `data/evidence.jsonl`: 证据片段
- `data/entities.jsonl`: 实体时间线
- `data/claims.jsonl`: 长期判断假设
- `brief/daily/YYYY-MM-DD.md`: 每日推送简报
- `report/YYYY-MM-DD.md`: brief 兼容镜像

## Agent 使用边界

`roles/orchestrator.md`、`roles/analyst.md`、`roles/reporter.md` 是旧日报生成流程的遗留参考，不再作为默认每日流程。

需要 agent 时，只用于：

- 对少量高价值事件做一手来源核验
- 判断事件是否支持、削弱或反驳已有 claim
- 生成周度/月度综合判断

不要用 agent 全量逐篇改写所有文章。

## 注意事项

- `.env` 文件包含 API 密钥，脚本自动加载。
- `scripts/digest.py` 已废弃，不要再用它生成分析。
- 代理: `http://127.0.0.1:7890`（境外信源需要）。代理失败必须通过 source health 暴露，而不是静默降级。
