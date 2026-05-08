# Agent Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure news-intel into an agent-driven workspace where `fetch.py` handles data acquisition and Claude Code / OpenClaw agents handle all analysis, historical association, and report generation.

**Architecture:** Three-role pipeline — Orchestrator (selects articles + extracts keywords) → Analyst sub-agents (grep historical digest + deep analysis, run in parallel) → Reporter (assembles daily report + publishes). Historical association uses targeted `Grep` on `digest/*.md` files, replacing the MiniMax API KB injection with real semantic search.

**Tech Stack:** Markdown role files in `.claude/skills/news-intel/roles/`, `CLAUDE.md` workspace entry, existing `fetch.py` + `build_site.py` unchanged.

---

## File Map

**Created:**
- `CLAUDE.md` — workspace entry point for agents
- `.claude/skills/news-intel/SKILL.md` — skill routing entry (replaces root `SKILL.md` logic)
- `.claude/skills/news-intel/roles/analyst.md` — single-article deep analysis role (grep + analyze)
- `.claude/skills/news-intel/roles/orchestrator.md` — article selection + task dispatch role
- `.claude/skills/news-intel/roles/reporter.md` — report assembly + publish role

**Modified:**
- `SKILL.md` (root) — redirect to new structure, mark old pipeline as deprecated

**Deprecated (not deleted):**
- `scripts/digest.py` — LLM analysis via MiniMax API (replaced by analyst role)
- `scripts/kb_update.py` — KB maintenance (no longer needed)
- `scripts/cluster.py` — never wired into pipeline, now officially deprecated

---

## Task 1: Create CLAUDE.md workspace entry

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Write CLAUDE.md**

```markdown
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
```

- [ ] **Step 2: Verify file created**

```bash
head -5 CLAUDE.md
```

Expected: `# News Intel — 科技资讯工作区`

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md workspace entry for agent workflows"
```

---

## Task 2: Create role directory structure

**Files:**
- Create: `.claude/skills/news-intel/roles/` (directory)

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p .claude/skills/news-intel/roles
```

- [ ] **Step 2: Verify**

```bash
ls .claude/skills/news-intel/roles/
```

Expected: empty directory (no error)

---

## Task 3: Write analyst.md — the core role

This is the most important role. An analyst receives one article + keywords, greps historical digest files, and produces a structured analysis. Test this manually before building orchestrator/reporter.

**Files:**
- Create: `.claude/skills/news-intel/roles/analyst.md`

- [ ] **Step 1: Write analyst.md**

```markdown
---
name: analyst
description: |
  单篇文章深度分析。收到一篇原文路径 + 关键词列表，
  用关键词 grep 历史 digest 文件找真实历史关联，然后写深度分析。
  由 orchestrator 以子 agent 方式调用。
---

# Analyst Role — 单篇文章深度分析

## 输入

你会收到：
- `文件路径`: 原文的绝对路径（如 `raw/2026/05/05/008-techcrunch-xxx.md`）
- `关键词列表`: 2-4 个专有名词（公司名/产品名/人名），如 `["豆包", "字节跳动"]`
- `工作区路径`: 仓库根目录（如 `/root/.openclaw/workspace/news-intel/` 或 `/Users/zcs/code2/news-intel/`）

## 执行步骤

### 步骤 1: 读取原文

使用 Read 工具读取完整原文：
```
Read(file_path="<工作区路径>/<文件路径>")
```

提取：标题、来源、发布时间、正文核心内容。

### 步骤 2: 用关键词 grep 历史 digest

对每个关键词，在历史 digest 文件中搜索：

```
Grep(
  pattern="关键词1|关键词2",
  path="<工作区路径>/digest/",
  glob="*.md",
  output_mode="content",
  context=3
)
```

**关键词使用规则：**
- 优先使用专有名词（公司名、产品名、人名）
- 避免通用词（"AI"、"科技"、"创业"单独使用）
- 若 grep 结果超过 100 行，缩窄关键词（加更多组合条件）
- 若关键词全是通用词，则标注"历史关联: 无（关键词过于通用）"

### 步骤 3: 分析历史关联

- 如果 grep 找到相关内容：
  - 读取对应 digest 文件的相关段落（Read 工具，只读相关行附近）
  - 总结真实关联：具体日期 + 具体事件（不超过2句话）
- 如果 grep 无结果：
  - 历史关联字段写"无相关历史记录"
  - **不要凭想象编写关联，不要硬凌**

### 步骤 4: 写深度分析

输出以下结构（Markdown 格式）：

```markdown
## [文章标题]

**来源**: [信源名] | **发布**: [YYYY-MM-DD] | **评分**: ⭐×N (N/5)
**链接**: [URL]

**核心事件**: [50字以内，忠实还原，保留限定词如"据报道"/"allegedly"/"计划"，不夸大]

**原文引用**: "[直接引用原文最关键的1-2句，保留原语言（中文/英文）]"

**🔗 历史关联**: [基于 grep 结果的真实关联，格式: "YYYY-MM-DD 报道了XX事件，与本文的关联是..."]
（如果无相关历史，写"无相关历史记录"）

**💡 底层驱动力**: [为什么现在发生？市场动机/技术演进/商业逻辑，1-2句]

**⚠️ 缺失信息**: [原文未说但读者需要知道的关键前提，若无写"无"]

**🔍 批判判断**: [识别标题党/PR夸大/数据缺失/逻辑漏洞，若无写"叙述客观"]

**背景补充**: [补充1-2句有价值的行业背景]
```

### 评分标准

- 5 = 影响行业走向的重大突破或决策
- 4 = 值得关注的重要事件或产品发布
- 3 = 有价值的行业动态
- 2 = 一般资讯，价值有限
- 1 = 无关内容/纯广告/重复旧闻

## 核心原则

- **历史关联必须基于实际 grep 结果，不能凭想象**
- 忠实还原原文，不夸大不缩小，保留限定词
- 原文说"nearly"就写"nearly"，说"据报道"就保留

## 完成后

将完整分析内容（Markdown 格式）返回给调用者（orchestrator）。
```

- [ ] **Step 2: Verify file created**

```bash
head -5 .claude/skills/news-intel/roles/analyst.md
```

Expected: `---` (YAML frontmatter start)

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/news-intel/roles/analyst.md
git commit -m "feat: add analyst role — grep-based historical association + deep analysis"
```

---

## Task 4: Manual test of analyst role

Before building orchestrator, manually verify the analyst role works on a real article.

**Files:** None (test only)

- [ ] **Step 1: Pick a test article with likely historical matches**

```bash
ls raw/2026/05/05/ | grep -i "doubao\|36\|豆包" | head -3
# If none, use:
ls raw/2026/05/05/ | head -5
```

Pick one article. Note its full path (e.g., `raw/2026/05/05/002-36-untitled.md`).

- [ ] **Step 2: Manually run a simulated analyst pass**

Read the article:
```bash
head -20 raw/2026/05/05/002-36-untitled.md
```

Extract keywords from title/content (e.g., `["豆包", "字节"]`).

Run grep manually:
```bash
grep -r "豆包\|字节" digest/ --include="*.md" -l
```

If matches found:
```bash
grep -r "豆包\|字节" digest/ --include="*.md" -C 3 | head -50
```

- [ ] **Step 3: Verify grep finds meaningful historical context**

Expected: Lines from `digest/2026-05-04.md` or earlier mentioning 豆包/字节 with context.

If grep finds nothing (too short a history), try a known entity:
```bash
grep -r "Salesforce\|Slack\|Microsoft\|OpenAI" digest/ --include="*.md" -l
```

Expected: At least 1-2 files with matches.

- [ ] **Step 4: Document test result**

Note in a comment what you found:
- Did grep return meaningful context? (yes/no)
- Were the matches genuinely related to the article? (yes/no)
- Any keyword quality issues?

This validates the core mechanism before building the full pipeline.

---

## Task 5: Write orchestrator.md

**Files:**
- Create: `.claude/skills/news-intel/roles/orchestrator.md`

- [ ] **Step 1: Write orchestrator.md**

```markdown
---
name: orchestrator
description: |
  今日原文快速评估 + 任务分发。
  读取 raw/ 目录中今日所有原文，快速筛选 15-25 篇值得深度分析的文章，
  提取每篇的关键词，然后以子 agent 方式调用 analyst role 并行分析。
---

# Orchestrator Role — 文章选择与任务分发

## 输入

- `日期`: YYYY-MM-DD 格式（默认今天）
- `工作区路径`: 仓库根目录

## 执行步骤

### 步骤 1: 获取今日原文列表

```bash
ls <工作区路径>/raw/YYYY/MM/DD/
```

将文件名列表记录下来（通常 40-80 篇）。

### 步骤 2: 快速评估每篇文章

对每篇原文，读取前 500 字（标题 + 摘要 + 导语）：

```
Read(file_path="<工作区路径>/raw/YYYY/MM/DD/<filename>", limit=20)
```

根据以下标准快速打分（不做深度分析）：

**入选标准**（满足任一）：
- 有明确的新产品/新功能/新政策发布
- 涉及重要公司（Anthropic/OpenAI/Google/Apple/Meta/字节/腾讯/阿里 等）的重要动态
- 有实际商业影响（融资、裁员、合并、监管）
- 有技术突破或重要研究发现

**排除标准**（命中即排除）：
- 纯广告/软文（无新闻价值）
- 重复旧闻（同一事件在多个信源出现，只保留最详细的一篇）
- 与科技/AI/商业完全无关的内容（娱乐、体育等，除非有科技维度）

### 步骤 3: 提取每篇关键词

对每篇入选文章，提取 2-4 个**专有名词**作为关键词：
- 公司名（中英文都要）：`["豆包", "字节跳动", "ByteDance"]`
- 产品名：`["Claude Code", "GPT-5", "Copilot"]`
- 人名：`["黄仁勋", "Jensen Huang", "Sam Altman"]`
- 特定技术/事件名：`["CopyFail", "RAMpocalypse"]`

**避免通用词**：不要用 "AI"、"科技"、"创业"、"startup" 单独作为关键词。

### 步骤 4: 派发分析任务

对每篇入选文章，以子 agent 方式调用 analyst role：

```
Agent(
  prompt="按照 .claude/skills/news-intel/roles/analyst.md 的要求分析以下文章：
  文件路径: <工作区路径>/raw/YYYY/MM/DD/<filename>
  关键词: [<keyword1>, <keyword2>, ...]
  工作区路径: <工作区路径>
  
  请完整执行 analyst role 中的所有步骤，返回完整的 Markdown 分析。"
)
```

**并行执行**：一次最多同时派发 5-8 个子 agent（防止并发过多）。分批处理，每批完成后再派发下一批。

**如果不支持子 agent**：按顺序逐篇执行，每篇直接调用 analyst role 的步骤（同一 agent 顺序处理）。

### 步骤 5: 收集所有分析结果

等待所有子 agent 返回分析结果。如果某篇分析失败，在结果列表中标记"分析失败"，继续处理其他文章。

### 步骤 6: 写入 digest 文件

将所有分析结果汇总，写入 `digest/YYYY-MM-DD.md`：

```markdown
# 科技资讯分析 · YYYY-MM-DD

> 共处理 N 篇，入选 M 篇
> 生成时间：YYYY-MM-DD HH:MM CST

---

[按评分降序排列的所有分析结果]
```

### 步骤 7: 调用 Reporter

将汇总好的分析内容传给 reporter role，生成最终日报。

## 错误处理

- **文章过多（>80篇）**: 将入选上限从 25 降为 15，grep 时间窗口建议缩短到 14 天
- **某篇分析失败**: 跳过，在 digest 中标注"[分析失败]"
- **不支持子 agent**: 退化为串行，性能变慢但结果一致
```

- [ ] **Step 2: Verify file created**

```bash
wc -l .claude/skills/news-intel/roles/orchestrator.md
```

Expected: 80+ lines

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/news-intel/roles/orchestrator.md
git commit -m "feat: add orchestrator role — article selection + keyword extraction + analyst dispatch"
```

---

## Task 6: Write reporter.md

**Files:**
- Create: `.claude/skills/news-intel/roles/reporter.md`

- [ ] **Step 1: Write reporter.md**

```markdown
---
name: reporter
description: |
  日报汇总生成。接收所有 analyst 的分析结果（已写入 digest/YYYY-MM-DD.md），
  生成格式化日报，发送到飞书群，更新静态站点，commit + push。
---

# Reporter Role — 日报生成与发布

## 输入

- `日期`: YYYY-MM-DD
- `工作区路径`: 仓库根目录
- `digest 文件`: `<工作区路径>/digest/YYYY-MM-DD.md`（已由 orchestrator 写入）

## 执行步骤

### 步骤 1: 读取 digest 分析

```
Read(file_path="<工作区路径>/digest/YYYY-MM-DD.md")
```

从分析结果中提取所有文章的：标题、评分、来源、核心事件、历史关联。

### 步骤 2: 参考历史日报格式

读取最近一篇日报作为格式参考：
```
Read(file_path="<工作区路径>/report/<最近日期>.md", limit=50)
```

### 步骤 3: 生成日报

按以下格式生成日报：

```markdown
📰 科技资讯日报 · YYYY年MM月DD日

🔴 本日重点
[评分 4-5 分的重要事件，每个展开 3-5 句话：
 - 核心事件（忠实还原，保留限定词）
 - 历史关联（若 digest 中有真实关联，展开背景）
 - 值得注意的问题或疑点]

🤖 AI & 大模型
[评分 3-4 分的 AI 相关内容，每条 2-3 句]

🚀 科技创业 & 商业  
[评分 3-4 分的商业内容，每条 2-3 句]

📱 产品 & 硬件
[相关内容，每条 1-2 句]

⚡ 快讯
[评分 3 分的内容，每条一行，格式: | 来源 | 内容摘要 |]

💡 今日洞察
[如果多篇文章有共同主题或趋势，用 2-4 句话点出]

---
本日报基于真实数据生成 | 信源: [列出本日使用的信源，逗号分隔]
```

**重磅事件的历史关联展开规则：**
- 只展开 digest 中明确标注了真实历史关联的内容
- 不要凭空添加历史背景
- 若无历史关联，直接写事件本身

### 步骤 4: 存档日报

```
Write(
  file_path="<工作区路径>/report/YYYY-MM-DD.md",
  content="[日报内容]"
)
```

### 步骤 5: 发送到飞书群

使用 `feishu_chat` 工具发送：
```
feishu_chat(
  action="send",
  chat_id="oc_d170dda09264716d786cd28cc48e5f78",
  message="[日报内容]"
)
```

⚠️ 必须使用 `feishu_chat` 工具，不要用 curl 调 webhook，不要把 chat_id 当 token。

### 步骤 6: 更新静态站点

```bash
python3.11 <工作区路径>/scripts/build_site.py
```

### 步骤 7: Commit + Push

```bash
git -C <工作区路径> add raw/ digest/ report/ docs/
git -C <工作区路径> commit -m "daily: YYYY-MM-DD 科技资讯日报"
node <工作区路径>/scripts/git_push.js
```

## 错误处理

- **飞书发送失败**: 记录错误，日报仍存档到 report/，继续 commit + push
- **build_site.py 失败**: 记录错误，继续 commit + push（静态站点可稍后补跑）
- **git push 失败**: git_push.js 会自动尝试代理，若仍失败，记录错误，日报已本地存档
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/news-intel/roles/reporter.md
git commit -m "feat: add reporter role — report assembly, feishu publish, git push"
```

---

## Task 7: Write the new SKILL.md entry point

**Files:**
- Create: `.claude/skills/news-intel/SKILL.md`

- [ ] **Step 1: Write .claude/skills/news-intel/SKILL.md**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/news-intel/SKILL.md
git commit -m "feat: add .claude/skills/news-intel/SKILL.md — new agent pipeline entry"
```

---

## Task 8: Update root SKILL.md to redirect

Keep the root `SKILL.md` working for OpenClaw backward compatibility, but redirect to the new structure.

**Files:**
- Modify: `SKILL.md`

- [ ] **Step 1: Read current SKILL.md**

```bash
head -10 SKILL.md
```

- [ ] **Step 2: Replace SKILL.md content**

Write the following (full replacement):

```markdown
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
```

- [ ] **Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: update root SKILL.md to redirect to new agent pipeline"
```

---

## Task 9: Mark deprecated scripts

Add a deprecation header to the three deprecated scripts so agents (and humans) don't accidentally use them.

**Files:**
- Modify: `scripts/digest.py` (first line comment)
- Modify: `scripts/kb_update.py` (first line comment)
- Modify: `scripts/cluster.py` (first line comment)

- [ ] **Step 1: Add deprecation notice to digest.py**

Read current first line of digest.py:
```bash
head -3 scripts/digest.py
```

Add after the shebang line (line 1):

```python
# DEPRECATED: This script is replaced by the analyst role in .claude/skills/news-intel/roles/analyst.md
# Do not use for new daily report generation. Kept for reference only.
```

- [ ] **Step 2: Add deprecation notice to kb_update.py**

```python
# DEPRECATED: Knowledge base maintenance is no longer needed.
# The analyst role grep-searches digest/ files directly. Kept for reference only.
```

- [ ] **Step 3: Add deprecation notice to cluster.py**

```python
# DEPRECATED: Was never wired into the main pipeline. Kept for reference only.
```

- [ ] **Step 4: Commit**

```bash
git add scripts/digest.py scripts/kb_update.py scripts/cluster.py
git commit -m "chore: mark digest.py, kb_update.py, cluster.py as deprecated"
```

---

## Task 10: End-to-end smoke test

Verify the new pipeline works by running the analyst role manually on one real article.

**Files:** None (test only)

- [ ] **Step 1: Pick a test article**

```bash
ls raw/2026/05/05/ | grep -v "^001" | head -3
```

Pick an article about a company with likely history (豆包, VS Code, OpenAI, Anthropic).
For example: `raw/2026/05/05/008-techcrunch-us-government-warns-of-severe-copyfail-b.md`

- [ ] **Step 2: Run analyst flow manually**

Read the file:
```bash
head -15 raw/2026/05/05/008-techcrunch-us-government-warns-of-severe-copyfail-b.md
```

Note the title: "US government warns of severe CopyFail bug affecting major versions of Linux"
Keywords: `["CopyFail", "Linux", "CISA", "CVE-2026-31431"]`

Run grep:
```bash
grep -r "Linux\|CISA\|security vulnerability" digest/ --include="*.md" -l
```

Then:
```bash
grep -r "Linux\|CISA" digest/ --include="*.md" -C 3 | head -30
```

- [ ] **Step 3: Verify analyst produces valid output**

The analyst role should produce:
- A "核心事件" that matches the actual article (no hallucination)
- A "历史关联" that either cites a real grep match OR says "无相关历史记录"
- A "批判判断" that identifies PR language or missing info
- A numeric score 1-5

**Pass criteria:** No hallucinated historical associations. If no history exists, the field says "无相关历史记录", not a made-up connection.

- [ ] **Step 4: Document result**

Run the full analyst flow (Read article → Grep digest/ → Write analysis) and confirm output quality.

Expected: Historical association is either grounded in grep results or honestly says "无".

- [ ] **Step 5: Final commit (if any fixes needed)**

```bash
git add .
git commit -m "fix: adjust analyst/orchestrator based on smoke test"
```

---

## Self-Review

**Spec coverage check:**

| Spec requirement | Task |
|---|---|
| fetch.py continues unchanged | Task 8 (SKILL.md mentions it, scripts not modified) ✓ |
| CLAUDE.md workspace entry | Task 1 ✓ |
| .claude/skills/news-intel/SKILL.md | Task 7 ✓ |
| analyst.md with grep-based history | Task 3 ✓ |
| orchestrator.md with parallel dispatch | Task 5 ✓ |
| reporter.md with feishu + git | Task 6 ✓ |
| deprecate digest.py, kb_update.py, cluster.py | Task 9 ✓ |
| Manual test before orchestrator | Task 4 ✓ |
| End-to-end smoke test | Task 10 ✓ |

**Placeholder scan:** None found. All steps have exact commands or file content.

**Type consistency:** Role files are Markdown documents, not code — no type issues.

**Missing spec item:** The design says `build_site.py` continues to run (agent-triggered). This is handled in reporter.md (Task 6, step 6). ✓

All spec requirements covered.
