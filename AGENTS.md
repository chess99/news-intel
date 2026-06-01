# News Intel — Personal Tech Radar 工作区

## 工作区路径

服务器: `/root/.openclaw/workspace/news-intel/`
本地开发: `/Users/zcs/code2/news-intel/`

## 核心方向

本仓库的目标是 Personal Tech Radar，不是通用科技日报站点。核心依据见 `docs/strategy/personal-tech-radar.md`。

系统应优先抓取一手和高质量二手信源，显式记录墙外源和代理失败，生成结构化事件、实体、证据和长期判断假设，再输出小而可信的每日推送简报。

## 文件结构

```
raw/YYYY/MM/DD/                  原文归档
state/source_health.json         信源健康状态
data/articles/YYYY-MM-DD.jsonl   标准化文章
data/candidates/YYYY-MM-DD.jsonl 候选事件
data/events/YYYY-MM-DD.jsonl     聚类后的事件
data/evidence.jsonl              证据片段
data/entities.jsonl              实体时间线
data/claims.jsonl                长期判断假设
brief/daily/YYYY-MM-DD.md        每日推送简报
brief/weekly/YYYY-WW.md          周度判断更新
brief/monthly/YYYY-MM.md         月度复盘
report/YYYY-MM-DD.md             daily brief 兼容镜像
site/                            GitHub Pages 研究/归档站点
```

`digest/`、`clusters/` 和 `scripts/digest.py` 是历史遗留产物，不再作为主流程输入。

## 日常任务流

每日运行：

```bash
python3.11 -m news_intel.cli run --date YYYY-MM-DD
```

Pipeline 顺序：

```
fetch → ingest → extract → cluster → investigate → knowledge → brief → deliver → site
```

如果只是本地验证，不发送飞书：

```bash
python3.11 -m news_intel.cli run --date YYYY-MM-DD --skip-delivery
```

## 注意事项

- `.env` 文件包含 API 密钥，脚本会自动加载（无需手动 source）。
- 代理地址: `http://127.0.0.1:7890`，境外一手信源可能依赖 mihomo，失败必须记录在 `state/source_health.json`。
- 低成本模型用于抽取、分类、聚类；强模型或 agent 只用于少数高价值 investigation 和周/月度综合。
- 每日简报应保持 5-8 条，必须包含来源层级、原文链接、证据和置信度。
