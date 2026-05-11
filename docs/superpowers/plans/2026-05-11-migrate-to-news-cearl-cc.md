# Migrate to news.cearl.cc Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将站点从 `cearl.cc/news-intel/` 迁移到 `news.cearl.cc`，移除 basePath，更新所有硬编码的路径和 URL。

**Architecture:** 自定义域名已配置好（DNS CNAME + GitHub Pages custom domain），现在需要把代码里所有假设路径为 `/news-intel` 的地方改为根路径 `/`，并把 `SITE_URL` 从 `cearl.cc` 改为 `news.cearl.cc`。涉及 Next.js 配置、RSS feed、search page 的 pagefind 路径、README。

**Tech Stack:** Next.js 14 (static export), pagefind, GitHub Actions

---

## 受影响文件一览

| 文件 | 改动内容 |
|------|---------|
| `site/next.config.js` | 删除 `basePath`，更新 `NEXT_PUBLIC_BASE_PATH` 为 `''`，更新 `NEXT_PUBLIC_SITE_URL` 为 `https://news.cearl.cc` |
| `site/app/feed.xml/route.js` | 更新 `SITE_URL` 和 `BASE_PATH` |
| `site/app/search/page.js` | 更新 pagefind 硬编码路径 |
| `README.md` | 更新在线地址链接 |

**不需要改的：**
- `site/app/layout.js` — 用了 `process.env.NEXT_PUBLIC_BASE_PATH`，改完 next.config.js 就自动正确
- `site/app/page.js`, `site/app/[date]/page.js` — 同上，用了环境变量
- `scripts/git_push.js` — 只是注释里提到 repo 名，不影响功能
- `.claude/skills/` — 路径指的是文件系统路径，不是 URL，无需改动
- `CLAUDE.md` — 同上
- `site/out/` — 构建产物，build 后自动重新生成，不用手动改

---

### Task 1: 更新 next.config.js

**Files:**
- Modify: `site/next.config.js`

- [ ] **Step 1: 修改配置**

将文件改为：

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: { unoptimized: true },
  env: {
    NEXT_PUBLIC_BASE_PATH: '',
    NEXT_PUBLIC_SITE_URL: 'https://news.cearl.cc',
  },
}

module.exports = nextConfig
```

关键变化：
- 删除 `basePath: '/news-intel'`（有了自定义域名后不再需要 basePath）
- `NEXT_PUBLIC_BASE_PATH` 改为空字符串 `''`
- `NEXT_PUBLIC_SITE_URL` 改为 `https://news.cearl.cc`

- [ ] **Step 2: Commit**

```bash
git add site/next.config.js
git commit -m "config: remove basePath, update SITE_URL to news.cearl.cc"
```

---

### Task 2: 更新 RSS feed 路径

**Files:**
- Modify: `site/app/feed.xml/route.js`

- [ ] **Step 1: 修改文件**

```js
import { getAllReports } from '../../lib/reports'

export const dynamic = 'force-static'

const SITE_URL = 'https://news.cearl.cc'
const BASE_PATH = ''

export async function GET() {
  const reports = getAllReports().slice(0, 20)

  const items = reports.map(r => `
    <item>
      <title><![CDATA[${r.title}]]></title>
      <link>${SITE_URL}${BASE_PATH}/${r.date}/</link>
      <guid isPermaLink="true">${SITE_URL}${BASE_PATH}/${r.date}/</guid>
      <pubDate>${new Date(r.date).toUTCString()}</pubDate>
      <description><![CDATA[${r.excerpt}]]></description>
    </item>`).join('\n')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Intel Daily — 科技资讯日报</title>
    <link>${SITE_URL}${BASE_PATH}/</link>
    <description>每日 AI 与科技深度资讯，批判性分析</description>
    <language>zh-CN</language>
    <atom:link href="${SITE_URL}${BASE_PATH}/feed.xml" rel="self" type="application/rss+xml"/>
    ${items}
  </channel>
</rss>`

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  })
}
```

- [ ] **Step 2: Commit**

```bash
git add site/app/feed.xml/route.js
git commit -m "fix: update RSS feed SITE_URL to news.cearl.cc, remove /news-intel base path"
```

---

### Task 3: 修复 search page 的 pagefind 硬编码路径

**Files:**
- Modify: `site/app/search/page.js`

问题：pagefind 的 CSS 和 JS 路径被硬编码为 `/news-intel/pagefind/...`，改为 `/pagefind/...`。

- [ ] **Step 1: 修改两处硬编码路径**

在 `site/app/search/page.js` 中，将：
```js
cssLink.href = '/news-intel/pagefind/pagefind-ui.css'
```
改为：
```js
cssLink.href = '/pagefind/pagefind-ui.css'
```

将：
```js
script.src = '/news-intel/pagefind/pagefind-ui.js'
```
改为：
```js
script.src = '/pagefind/pagefind-ui.js'
```

- [ ] **Step 2: Commit**

```bash
git add site/app/search/page.js
git commit -m "fix: update pagefind paths to root /pagefind/ (no basePath)"
```

---

### Task 4: 更新 README 在线地址

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 更新在线日报链接**

将：
```markdown
📰 **[在线日报归档](https://chess99.github.io/news-intel/)** — 每日自动更新
```
改为：
```markdown
📰 **[在线日报归档](https://news.cearl.cc/)** — 每日自动更新
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update site URL to news.cearl.cc in README"
```

---

### Task 5: 构建并验证

- [ ] **Step 1: 本地构建**

```bash
cd site && npm run build
```

预期输出：构建成功，`out/` 目录生成，无报错。

- [ ] **Step 2: 检查构建产物中无残留 /news-intel 路径**

```bash
grep -r "news-intel" site/out --include="*.html" --include="*.js" --include="*.xml" | grep -v "node_modules" | head -20
```

预期输出：无任何包含 `/news-intel` 路径的结果（仓库名在注释里出现是正常的，路径出现是不正常的）。

- [ ] **Step 3: 检查 RSS feed 内容正确**

```bash
cat site/out/feed.xml | grep -E "link|href"
```

预期：所有 URL 均以 `https://news.cearl.cc/` 开头，无 `/news-intel`。

- [ ] **Step 4: Push，触发 CI 部署**

```bash
git push
```

在 GitHub Actions 看到 deploy 成功后，访问 `https://news.cearl.cc/` 验证：
- 首页正常加载
- RSS: `https://news.cearl.cc/feed.xml` 内容正确
- 搜索页: `https://news.cearl.cc/search/` 搜索功能正常
- 旧地址 `https://cearl.cc/news-intel/` 自动 301 跳转到 `https://news.cearl.cc/`（已验证，GitHub 自动处理）
