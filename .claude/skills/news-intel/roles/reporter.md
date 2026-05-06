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

```
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
- 只展开 digest 中明确标注了真实历史关联（基于 grep 结果）的内容
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

使用 feishu_chat 工具发送：
```
feishu_chat(
  action="send",
  chat_id="oc_d170dda09264716d786cd28cc48e5f78",
  message="[日报内容]"
)
```

⚠️ 必须使用 feishu_chat 工具，不要用 curl 调 webhook，不要把 chat_id 当 token。

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
