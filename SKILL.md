---
name: news-intel
description: |
  科技资讯日报生成入口。每天 09:00 CST 由 cron 触发。
  当用户提到"发资讯"、"今日日报"、"科技新闻"、"资讯群"时触发。
  告诉你工作区路径、三层文件结构、如何生成日报。
---

# News Intel — 科技资讯工作区

## 工作区路径

```
/root/.openclaw/workspace/news-intel/
```

## 三层文件结构

```
raw/YYYY/MM/DD/NNN-source-slug.md   # 第一层：原文存档（脚本自动生成）
digest/YYYY-MM-DD.md                # 第二层：LLM 提炼列表（脚本自动生成）
report/YYYY-MM-DD.md                # 第三层：最终日报存档（你生成后保存）
```

## 日常流程

**前两步由 crontab 在 08:30 CST 自动完成，你不需要管：**

```bash
# 步骤1：抓取原文（约5-10分钟）
python3.11 /root/.openclaw/workspace/news-intel/scripts/fetch.py

# 步骤2：LLM 提炼（约5分钟）
python3.11 /root/.openclaw/workspace/news-intel/scripts/digest.py
```

**你的任务（09:00 CST cron 触发）：**

1. 读取今日提炼文件：`digest/YYYY-MM-DD.md`
2. 结合 `report/` 目录的近期历史报告，进行汇总分析
3. 对评分 4-5 分的重要事件，结合历史背景展开深度解读
4. 生成日报，发送到资讯群（飞书群 `oc_d170dda09264716d786cd28cc48e5f78`）
5. 将日报内容存档到 `report/YYYY-MM-DD.md`

## 日报格式参考

```
📰 科技资讯日报 · YYYY年MM月DD日

🔴 重磅
[评分5分的事件，结合历史深度解读]

🤖 AI & 大模型
[评分4-5分的AI相关内容]

🚀 科技创业 & 商业
[...]

📱 产品 & 硬件
[...]

📊 快讯
[评分2-3分的内容，每条一行]

---
本报告基于真实 RSS 数据生成 | 信源: TechCrunch、36氪、VentureBeat 等
```

## 信源配置

`sources/feeds.yaml` — 可随时增删信源，重启后生效。

## 手动触发

如果自动流程失败或需要补发：

```bash
# 手动抓取并提炼
python3.11 /root/.openclaw/workspace/news-intel/scripts/fetch.py
python3.11 /root/.openclaw/workspace/news-intel/scripts/digest.py

# 然后读 digest/YYYY-MM-DD.md 生成日报
```

## 注意事项

- `fetch.py` 抓全文，每篇约需 2-3 秒，17 个信源约 5-10 分钟
- `digest.py` 调 MiniMax API 逐篇提炼，约 5 分钟
- 两步合计约 15 分钟，因此 crontab 设在 08:30，09:00 龙虾来读时已就绪
- 原文和提炼文件全部进 git，历史可查
