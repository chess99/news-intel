# news-intel

每日 AI 与科技深度资讯 pipeline。自动抓取 30+ 信源，LLM 批判性分析，生成日报。

📰 **[在线日报归档](https://news.cearl.cc/)** — 每日自动更新

---

## 特点

- **30+ 信源**：AI 官方博客（Anthropic/OpenAI/Google/Meta）、顶级 newsletter、中文 AI 媒体、工程实践
- **批判性分析**：识别 PR 语言、标注缺失信息、保留原文限定词
- **历史关联**：30 天知识库，分析时自动关联历史事件
- **事件聚合**：同一事件多个来源合并对比（cluster.py）
- **完全自动化**：cron 每日 08:30 触发，09:00 前准备就绪
- **开源友好**：兼容任何 OpenAI-format API，proxy 可选

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

# 4. 抓取今日文章
source .env
python3.11 scripts/fetch.py

# 5. 生成深度分析
python3.11 scripts/digest.py
```

分析结果在 `digest/YYYY-MM-DD.md`，可以直接阅读或交给 AI 生成日报。

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

# 每天 08:30 抓取 + 分析，09:00 由 AI agent 生成日报
30 8 * * * cd /path/to/news-intel && source .env && python3.11 scripts/fetch.py >> /tmp/news-fetch.log 2>&1 && python3.11 scripts/digest.py >> /tmp/news-digest.log 2>&1 && python3.11 scripts/kb_update.py >> /tmp/news-kb.log 2>&1
```

---

## 文件结构

```
news-intel/
├── scripts/
│   ├── fetch.py        # Layer 1: 并发抓取 RSS + 全文（含日期过滤）
│   ├── digest.py       # Layer 3: LLM 批判性分析 + 历史关联注入
│   ├── cluster.py      # Layer 2: 事件聚合（同一事件多来源合并）
│   ├── kb_update.py    # Layer 4: 维护 30 天知识库
│   ├── build_site.py   # Layer 5: 生成 GitHub Pages 静态站点
│   └── git_push.js     # 用 GitHub App token 推送（可选）
├── sources/
│   └── feeds.yaml      # 信源配置（可直接增删）
├── raw/YYYY/MM/DD/     # 原文存档（脚本自动生成）
├── digest/             # LLM 分析结果（脚本自动生成）
│   ├── YYYY-MM-DD.md   # 人类可读格式
│   └── YYYY-MM-DD.jsonl # 结构化数据（供 kb_update.py 读取）
├── kb/
│   └── events.jsonl    # 30 天知识库（kb_update.py 维护）
├── clusters/           # 事件聚合结果（cluster.py 生成）
├── report/             # 最终日报（AI agent 或手工生成）
├── docs/               # GitHub Pages 静态文件（build_site.py 生成）
├── .env.example        # 环境变量模板
└── requirements.txt    # Python 依赖
```

---

## 完整 pipeline

```
fetch.py → cluster.py → digest.py → kb_update.py → [AI生成日报] → build_site.py
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
