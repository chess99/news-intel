# Reporter Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the reporter role prompt so the daily report reads like a curated briefing for human readers, not an AI analysis log.

**Architecture:** The fix is entirely in the reporter's prompt template. The analyst role stays unchanged (it produces rich internal data). The reporter's job is to *distill* that data into user-facing prose — filtering out internal critique fields and rewriting content from the reader's perspective: "what happened and why does it matter to me."

**Tech Stack:** Markdown prompt files only. Validation via a clean-context agent that reruns the reporter against an existing digest and compares output quality.

---

## Root Cause Summary

The current reporter prompt has two problems:

1. **No filter on analyst fields.** The analyst produces `🔍 批判判断` and `⚠️ 缺失信息` fields as internal QC tools. The reporter's Step 3 template says "保留值得注意的问题或疑点" — which causes the LLM to include these verbatim. Readers see "标题'曝光'和'读心术'措辞带有营销色彩" with no context for what headline that refers to.

2. **Structure is analysis-report, not briefing.** Each featured article has three subsections: 核心发现 → 技术逻辑 → 批判性思考. This is peer-review structure. Readers want: what happened + why it matters + what to watch.

Secondary issues:
- Quick-takes (快讯) contain parenthetical analyst commentary that breaks the format
- 历史关联 presented as a detached table at the end instead of woven into context naturally
- 今日洞察 quality is inconsistent — sometimes good synthesis, sometimes just keyword restating

## Files Changed

- **Modify:** `.claude/skills/news-intel/roles/reporter.md` — the only file that needs to change

---

## Task 1: Rewrite reporter.md

**Files:**
- Modify: `.claude/skills/news-intel/roles/reporter.md`

- [ ] **Step 1: Read the current reporter.md in full**

```
Read(file_path=".claude/skills/news-intel/roles/reporter.md")
```

Confirm you have the full content before editing.

- [ ] **Step 2: Replace the report format template in Step 3**

Replace the entire `步骤 3: 生成日报` section with the following. The key changes are:

**A. New article format for featured stories** — no "批判性思考" subsection. Instead, critical caveats are woven into the narrative as natural qualifiers (e.g., "该数据来自内部测试，尚无独立验证" rather than a standalone critique paragraph).

**B. Quick-takes rule** — strip all parenthetical analyst commentary from 快讯 entries.

**C. 历史关联** — if a story has a meaningful historical link, include it as one sentence inside the story's paragraph, not in a separate table.

**D. 今日洞察 quality bar** — must name a non-obvious cross-story pattern; forbidden from simply restating individual headlines.

The new Step 3 content:

```markdown
### 步骤 3: 生成日报

**核心原则（必须遵守）：**

这份日报面向忙碌的读者，不是面向 AI 审稿人。
- **禁止**将 digest 中的 `批判判断`、`缺失信息` 字段直接复制到报告正文
- 如果某篇文章有值得读者知道的重要限定（如"数据来自内部测试"、"尚无独立验证"），将其作为自然限定词融入叙述句中，而不是单独列出
- **快讯条目不加括号注释**——一行只说一件事，无分析附言
- **历史关联不单独成表**——有实质关联的，用一句话自然融入该故事的段落里；没有实质关联的，不提

**日报格式：**

```
📰 科技资讯日报 · YYYY年MM月DD日
共处理 N 篇 | 入选 M 篇（评分≥3）| 生成时间：YYYY-MM-DD HH:MM CST

🔴 本日焦点
[评分 4-5 分的事件，每个写 3-5 句话，结构：
  第1句：发生了什么（忠实还原，保留限定词如"据报道"/"计划"）
  第2-3句：为什么现在发生，背后的逻辑或背景（若有历史关联，在此自然融入）
  最后1句（可选）：读者应该持续关注什么，或还有哪些关键信息尚不清楚
  注意：不要写独立的"批判"或"缺失信息"段落]

🤖 AI & 大模型
[评分 3-4 分的 AI 相关内容，每条 2-3 句，同上结构原则]

🚀 科技创业 & 商业
[评分 3-4 分的商业内容，每条 2-3 句]

📱 产品 & 硬件
[评分 3 分的产品/硬件内容，每条 1-2 句]

⚡ 快讯
[评分 3 分的其他内容，每条一行，格式: | 来源 | 一句话事实摘要 |
  规则：只写事实，不加括号注释，不加判断性用语]

💡 今日洞察
[必须满足：跨越至少两条不同新闻，提炼出一个读者单看任何一条都不会想到的模式或趋势
  禁止：只是重新列举今日头条的关键词
  字数：3-6句，不要更多]

---
本日报基于真实数据生成 | 信源: [列出本日使用的信源，逗号分隔]
```

**重磅事件示例（对比旧格式）：**

❌ 旧格式（禁止）：
> 批判性思考： 标题"曝光"和"读心术"措辞带有营销色彩；"意识特征""人机共处起点"属于过度哲学化延伸，超出研究本身范畴。

✅ 新格式（正确）：
> Anthropic开源NLA工具，可通过解读模型激活值让研究人员观察AI的内部推理状态。研究团队发现Claude存在"知道但不说"的现象——模型掌握某信息但不主动表达，这对AI安全审计从黑盒走向白盒具有实际意义。值得注意的是，该工具基于特定Claude版本训练，对其他模型的泛化效果尚未验证。

**快讯示例（对比旧格式）：**

❌ 旧格式（禁止）：
> | InfoQ | Cloudflare推出Artifacts公测版，为AI代理提供类Git的版本控制系统。营销话术较多，"Git-like"类比可能过于理想化——AI输出本质是非确定性的，与Git可复现的确定性代码可比性存疑 |

✅ 新格式（正确）：
> | InfoQ | Cloudflare推出Artifacts公测版，为AI代理提供版本控制能力，目前处于公测阶段 |
```

- [ ] **Step 3: Also update the historical association rule in Step 3 header**

Ensure the section on "重磅事件的历史关联展开规则" at the bottom of Step 3 is replaced with:

```markdown
**历史关联处理规则：**
- 若 digest 中有真实历史关联（基于 grep 结果），用一句话融入对应故事的正文段落中（例："此前 5月7日曾报道 Cloudflare 相关合作，与本次方向一致。"）
- 不要在报告末尾单独列"历史关联回顾"表格——这是内部分析工具，不是用户内容
- 若无实质历史关联，直接跳过，不要写"无历史关联"
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/news-intel/roles/reporter.md
git commit -m "feat: redesign reporter prompt - reader-first briefing format"
```

---

## Task 2: Backtest with clean-context agent

Run a fresh agent with no conversation history against an existing digest to verify the new prompt produces the correct output format.

**Files:**
- Read: `digest/2026-05-08.md` (input)
- Read: `.claude/skills/news-intel/roles/reporter.md` (new prompt)
- Output: `report/2026-05-08-v2.md` (test output, do not overwrite the original)

- [ ] **Step 1: Dispatch a clean-context agent**

```
Agent(
  prompt="你是一个 reporter agent。

请严格按照以下 reporter role 说明生成日报：

[在此粘贴 .claude/skills/news-intel/roles/reporter.md 的完整内容]

输入：
- 日期：2026-05-08
- digest 文件路径：/Users/zcs/code2/news-intel/digest/2026-05-08.md

执行步骤 1（读取 digest）和步骤 3（生成日报）。
不需要执行步骤 4（存档）、步骤 5（发飞书）、步骤 6（build site）、步骤 7（commit）。

直接将生成的完整日报文本返回给我。"
)
```

- [ ] **Step 2: Review output against these quality checks**

Read the agent's output and verify ALL of the following:

| Check | Pass condition |
|-------|---------------|
| No standalone critique sections | No paragraph starting with "批判性思考："、"批判："、"缺失信息：" |
| No parenthetical analyst commentary in 快讯 | Each 快讯 row contains only a factual summary, no `（...）` analysis |
| Historical links woven in naturally | No "历史关联回顾" table at the bottom |
| 今日洞察 is cross-story synthesis | Names a pattern that spans ≥2 stories, not a list of today's headlines |
| Critical caveats appear as natural qualifiers | Phrases like "尚无独立验证" or "据报道" appear inline in sentences |

- [ ] **Step 3: If any check fails, fix the reporter.md prompt and re-run**

Identify which rule in the prompt was insufficient to prevent the failure. Add a more explicit instruction or example to that rule. Repeat Step 1 and Step 2 until all checks pass.

- [ ] **Step 4: Save the passing test output**

```
Write(
  file_path="/Users/zcs/code2/news-intel/report/2026-05-08-v2.md",
  content="[agent output]"
)
```

- [ ] **Step 5: Commit test output**

```bash
git add .claude/skills/news-intel/roles/reporter.md report/2026-05-08-v2.md
git commit -m "test: backtest reporter v2 against 2026-05-08 digest - all checks pass"
```

---

## Self-Review

**Spec coverage:**
- ✅ "批判性思考" removed from featured articles → Task 1 Step 2 (new format template)
- ✅ Parenthetical commentary stripped from 快讯 → Task 1 Step 2 (快讯 rule + example)
- ✅ Historical links woven into prose → Task 1 Step 3 (历史关联处理规则)
- ✅ 今日洞察 quality bar → Task 1 Step 2 (今日洞察 required condition)
- ✅ Backtest with clean agent → Task 2

**Placeholder scan:** None found — all steps have concrete content, code blocks, and expected outputs.

**Type consistency:** N/A (prompt-only changes, no code types).
