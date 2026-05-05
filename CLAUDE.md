# News Intel — 科技资讯工作区

## 工作区路径

服务器: `/root/.openclaw/workspace/news-intel/`
本地开发: `/Users/zcs/code2/news-intel/`

## 文件结构

```
raw/YYYY/MM/DD/            原文（fetch.py 每日 08:30 CST 生成）
digest/YYYY-MM-DD.md       分析汇总（agent 每日生成）
report/YYYY-MM-DD.md       日报（agent 每日生成 + 发送飞书）
docs/                      GitHub Pages 静态文件（build_site.py 生成）
scripts/fetch.py           数据采集（Python，保留）
scripts/build_site.py      HTML 生成（Python，保留）
```

## 日常任务流（09:00 CST 触发）

运行 `.claude/skills/news-intel/SKILL.md` 中描述的流程：

1. **Orchestrator**：读取今日 `raw/` 原文，选出 15-25 篇，提取关键词
2. **Analyst**（并行）：每篇文章独立分析，grep 历史 `digest/` 做历史关联
3. **Reporter**：汇总分析，生成日报，发飞书，commit + push

详见 `.claude/skills/news-intel/SKILL.md`。

## 注意事项

- `.env` 文件包含 API 密钥，脚本会自动加载（无需手动 source）
- 代理地址: `http://127.0.0.1:7890`（境外信源抓取需要）
- `scripts/digest.py` 保留但已废弃，勿用于新的日报生成流程
