# news-intel

Personal Tech Radar：个人科技情报系统。它不是通用新闻站，而是抓取一手与高质量二手信源，结构化为文章、候选事件、事件、证据、实体和判断假设，再生成可推送的每日简报与可检索的历史研究页面。

📰 **[在线日报归档](https://news.cearl.cc/)** — 每日自动更新

---

## 核心定位

- **一手信源优先**：官方博客、产品 changelog、论文、监管/标准机构作为事实依据。
- **信源健康显式化**：墙外源依赖 mihomo 代理，失败不会静默消失，会写入 `state/source_health.json` 并出现在简报里。
- **AI 分层使用**：规则和轻量 LLM 做抽取/分类/聚类；强模型或 agent 只处理少数高价值调查与周/月度综合。
- **历史结构化**：用 `Event`、`Entity`、`Claim` 和 `Evidence` 拉通历史，不把历史日报整篇塞给模型硬总结。
- **推送优先**：主产物是 `brief/daily/YYYY-MM-DD.md`；GitHub Pages 是归档、搜索、主题、实体和假设页面。

详见 [Personal Tech Radar Strategy](docs/strategy/personal-tech-radar.md)。

---

## 快速上手

**前提条件**
- Python 3.11+
- 一个 LLM API Key（MiniMax 或任何 OpenAI-compatible API）
- （中国大陆用户）HTTP 代理

```bash
# 1. 克隆仓库
git clone https://github.com/chess99/news-intel.git
cd news-intel

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key 和代理地址

# 4. 运行完整 pipeline
python3.11 -m news_intel.cli run --date YYYY-MM-DD
```

主输出：

- `brief/daily/YYYY-MM-DD.md`：每日推送简报
- `brief/weekly/YYYY-WW.md`：周度判断更新
- `brief/monthly/YYYY-MM.md`：月度复盘
- `data/events/YYYY-MM-DD.jsonl`：结构化事件
- `data/entities.jsonl`：实体时间线数据
- `data/claims.jsonl`：长期假设与判断状态
- `state/source_health.json`：信源健康状态

---

## 环境变量

编辑 `.env`（从 `.env.example` 复制）：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `MINIMAX_API_KEY` | LLM API Key（必填） | — |
| `LLM_API_HOST` | API 地址 | `https://api.minimaxi.com` |
| `LLM_MODEL` | 模型名称 | `MiniMax-M2.7` |
| `HTTPS_PROXY` | HTTP 代理（海外用户留空） | — |

**切换 LLM：** 本工具兼容任何 OpenAI-format API，只需修改 `LLM_API_HOST` 和 `LLM_MODEL`：

```bash
# OpenAI
LLM_API_HOST=https://api.openai.com
LLM_MODEL=gpt-4o

# Groq（免费）
LLM_API_HOST=https://api.groq.com/openai
LLM_MODEL=llama-3.3-70b-versatile

# 本地 Ollama
LLM_API_HOST=http://localhost:11434
LLM_MODEL=qwen2.5:14b
```

---

## 自动化（cron）

```bash
# 编辑 crontab
crontab -e

# 每天 08:30 运行完整 radar pipeline
30 8 * * * cd /path/to/news-intel && python3.11 -m news_intel.cli run --date $(TZ=Asia/Shanghai date +\\%F) >> /tmp/news-radar.log 2>&1
```

---

## 文件结构

```
news-intel/
├── news_intel/         # Personal Tech Radar pipeline package
├── scripts/
│   ├── fetch.py        # RSS/全文抓取，保留 raw/ 兼容
│   ├── send_report.py  # 发送 brief/daily 到飞书，report/ 作为 fallback
│   └── git_push.js     # 用 GitHub App token 推送（可选）
├── sources/
│   └── feeds.yaml      # 信源配置：tier / fetch_strategy / proxy
├── raw/YYYY/MM/DD/     # 原文存档（脚本自动生成）
├── data/               # articles / candidates / events / entities / claims / evidence
├── state/              # source health and investigation state
├── brief/              # daily / weekly / monthly human-facing briefs
├── report/             # daily brief compatibility mirror
├── digest/             # historical legacy artifacts
├── clusters/           # historical legacy artifacts
├── site/               # Next.js GitHub Pages site
├── .env.example        # 环境变量模板
└── requirements.txt    # Python 依赖
```

---

## 完整 pipeline

```
fetch → ingest → extract → cluster → investigate → knowledge → brief → deliver → site
```

每个步骤独立运行，失败会降级而不中断整个 pipeline：
- `cluster.py` 失败 → `digest.py` 自动回退到单篇分析模式
- 单个信源抓取失败 → 跳过该源，继续处理其他源
- `kb_update.py` 失败 → 日报生成不受影响（只是无历史关联）

---

## 添加信源

编辑 `sources/feeds.yaml`，新增一条：

```yaml
- name: 你的信源名称
  url: https://example.com/feed.rss
  lang: en        # 或 zh
  category: ai    # 见 yaml 文件顶部的 category 说明
  enabled: true
```

保存后下次运行 `fetch.py` 即生效，无需重启。

---

## GitHub Pages

设置后每次日报更新（push `report/*.md`）自动发布到 GitHub Pages：

1. 在 GitHub 仓库 Settings → Pages → Source 选择 `gh-pages` branch
2. GitHub Actions (`.github/workflows/deploy.yml`) 会自动在每次日报 push 后构建

---

## License

MIT
