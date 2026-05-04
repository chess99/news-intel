---
name: news-intel
description: |
  科技资讯日报生成入口。每天 09:00 CST 由 cron 触发。
  当用户提到"发资讯"、"今日日报"、"科技新闻"、"资讯群"时触发。
  告诉你工作区路径、文件结构、如何生成日报。
---

# News Intel — 科技资讯工作区

## 工作区路径

```
/root/.openclaw/workspace/news-intel/
```

## 文件结构

```
raw/YYYY/MM/DD/     原文存档（fetch.py 生成）
digest/YYYY-MM-DD.md       LLM 批判性分析汇总（digest.py 生成）
digest/YYYY-MM-DD.jsonl    结构化分析数据（kb_update.py 读取）
kb/events.jsonl            30天历史事件知识库（kb_update.py 维护）
clusters/YYYY-MM-DD.json   事件聚合结果（cluster.py 生成）
report/YYYY-MM-DD.md       最终日报（你生成后保存）
docs/                      GitHub Pages 静态文件（build_site.py 生成）
```

## 完整 Pipeline

```
fetch.py → cluster.py → digest.py → kb_update.py → [你生成日报] → build_site.py
```

**前四步由 crontab 在 08:30 CST 自动完成，你不需要管。**

## 你的任务（09:00 CST cron 触发）

1. 读取今日分析文件：`digest/YYYY-MM-DD.md`
2. 参考 `report/` 目录近期历史报告的格式
3. 参考 `kb/events.jsonl` 中的历史事件（如有相关联事件，展开背景分析）
4. 生成日报，用 **`feishu_chat` 工具**发送到资讯群：
   ```
   feishu_chat(action="send", chat_id="oc_d170dda09264716d786cd28cc48e5f78", message="日报内容")
   ```
   ⚠️ 不要用 curl 调 webhook，不要把 chat_id 当 token，必须用 feishu_chat 工具
5. 将日报内容存档到 `report/YYYY-MM-DD.md`
6. 运行 `python3.11 /root/.openclaw/workspace/news-intel/scripts/build_site.py` 更新静态站点
7. commit 并 push（三层归档 + 站点同时入库）：
   ```bash
   git -C /root/.openclaw/workspace/news-intel add raw/ digest/ report/ docs/ kb/
   git -C /root/.openclaw/workspace/news-intel commit -m "daily: $(date +%Y-%m-%d) 科技资讯日报"
   node /root/.openclaw/workspace/news-intel/scripts/git_push.js
   ```

## 日报格式参考

```
📰 科技资讯日报 · YYYY年MM月DD日

🔴 重磅
[评分5分的事件，结合 kb/ 历史背景深度解读]

🤖 AI & 大模型
[评分4-5分的AI相关内容]

🚀 科技创业 & 商业
[...]

📱 产品 & 硬件
[...]

📊 快讯
[评分3分的内容，每条一行]

---
本报告基于真实数据生成 | 信源: TechCrunch、36氪、VentureBeat、Latent Space 等
```

## 手动触发前四步

```bash
cd /root/.openclaw/workspace/news-intel
source .env
python3.11 scripts/fetch.py
python3.11 scripts/cluster.py
python3.11 scripts/digest.py
python3.11 scripts/kb_update.py
```

## 注意事项

- 环境变量在 `.env` 文件中，脚本会自动加载（无需手动 source）
- digest.py 分析完成后同时输出 `.md`（人类可读）和 `.jsonl`（结构化数据）
- kb/events.jsonl 保存 30 天滚动历史，分析时自动关联同一事件的历史报道
- git_push.js 先尝试直连 GitHub，失败再走代理 7890
