# Next.js 静态站重构 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `site/` 从 Python 单文件站点迁移为 Next.js 静态站，支持独立 URL、全文搜索（Pagefind）和 RSS Feed。

**Architecture:** Next.js 14 App Router + `output: 'export'` 生成纯静态文件到 `site/out/`。数据层在构建时读取 `../report/*.md`，用 remark 转 HTML。GitHub Actions 改为 `npm run build`，产物路径不变（`site/out/`）。

**Tech Stack:** Next.js 14, React 18, remark + remark-html, gray-matter, Pagefind

---

## 文件结构

**新建：**
- `site/package.json` — 依赖和脚本
- `site/next.config.js` — basePath、output: export
- `site/app/layout.js` — 根布局（HTML shell、全局 CSS）
- `site/app/globals.css` — 设计 token 和全局样式
- `site/app/page.js` — 首页（渲染最新日报）
- `site/app/[date]/page.js` — 单篇日报页
- `site/app/search/page.js` — Pagefind 搜索页
- `site/app/feed.xml/route.js` — RSS Feed Route Handler
- `site/lib/reports.js` — 数据层：读取 md、解析、导出
- `site/components/Sidebar.js` — 日期列表侧边栏
- `site/components/ReportBody.js` — 日报正文渲染

**删除（实现完成并验证后）：**
- `site/build_site.py` — Python 构建脚本

**修改：**
- `.github/workflows/deploy.yml` — 替换 Python 构建步骤为 npm

---

## Task 1: 初始化 Next.js 工程

**Files:**
- Create: `site/package.json`
- Create: `site/next.config.js`

- [ ] **Step 1: 删除旧 Python 站点文件，保留 out/**

```bash
cd /Users/zcs/code2/news-intel/site
# 只删除 Python 脚本，out/ 暂时保留（后续被 next build 覆盖）
rm build_site.py
```

- [ ] **Step 2: 创建 package.json**

```bash
cd /Users/zcs/code2/news-intel/site
```

创建 `site/package.json`：

```json
{
  "name": "news-intel-site",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "postbuild": "npx pagefind --site out --output-path out/pagefind"
  },
  "dependencies": {
    "next": "^14",
    "react": "^18",
    "react-dom": "^18",
    "remark": "^15",
    "remark-html": "^16",
    "gray-matter": "^4"
  },
  "devDependencies": {
    "pagefind": "^1"
  }
}
```

- [ ] **Step 3: 创建 next.config.js**

创建 `site/next.config.js`：

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  basePath: '/news-intel',
  output: 'export',
  trailingSlash: true,
  images: { unoptimized: true },
  env: {
    NEXT_PUBLIC_BASE_PATH: '/news-intel',
    NEXT_PUBLIC_SITE_URL: 'https://cearl.cc',
  },
}

module.exports = nextConfig
```

- [ ] **Step 4: 安装依赖**

```bash
cd /Users/zcs/code2/news-intel/site
npm install
```

预期：`node_modules/` 出现，`package-lock.json` 生成。

- [ ] **Step 5: 验证 Next.js 可识别**

```bash
cd /Users/zcs/code2/news-intel/site
npx next --version
```

预期：输出 Next.js 版本号，如 `14.x.x`。

- [ ] **Step 6: 添加 .gitignore**

在 `site/` 目录创建 `.gitignore`：

```
node_modules/
.next/
```

- [ ] **Step 7: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/package.json site/next.config.js site/.gitignore site/package-lock.json
git commit -m "feat: init Next.js site scaffold"
```

---

## Task 2: 数据层 lib/reports.js

**Files:**
- Create: `site/lib/reports.js`

这是整个系统的数据基础，所有页面都依赖它。

- [ ] **Step 1: 创建 lib/ 目录并编写 reports.js**

创建 `site/lib/reports.js`：

```js
import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { remark } from 'remark'
import remarkHtml from 'remark-html'

// report/ 目录相对于 site/ 的位置
const REPORT_DIR = path.join(process.cwd(), '..', 'report')

/**
 * 从 markdown 第一个 # 标题中提取标题
 * 若无标题则返回默认值
 */
function extractTitle(content, date) {
  const match = content.match(/^#\s+(.+)$/m)
  return match ? match[1].replace(/[^\w\s·年月日\-/]/g, '').trim() : `科技资讯日报 · ${date}`
}

/**
 * 从正文中提取前 200 字作为摘要（去除 markdown 标记）
 */
function extractExcerpt(content) {
  const plain = content
    .replace(/^#+\s+.+$/gm, '')     // 去除标题
    .replace(/^>\s+.+$/gm, '')      // 去除引用
    .replace(/\*\*(.+?)\*\*/g, '$1') // 去除加粗
    .replace(/\*(.+?)\*/g, '$1')    // 去除斜体
    .replace(/\n+/g, ' ')           // 合并换行
    .trim()
  return plain.slice(0, 200)
}

/**
 * 返回所有日报的摘要列表，按日期倒序
 * @returns {{ date: string, title: string, excerpt: string }[]}
 */
export function getAllReports() {
  if (!fs.existsSync(REPORT_DIR)) return []

  return fs
    .readdirSync(REPORT_DIR)
    .filter(f => f.endsWith('.md'))
    .map(f => {
      const date = f.replace('.md', '')
      const raw = fs.readFileSync(path.join(REPORT_DIR, f), 'utf-8')
      const { content } = matter(raw)
      return {
        date,
        title: extractTitle(content, date),
        excerpt: extractExcerpt(content),
      }
    })
    .sort((a, b) => b.date.localeCompare(a.date))
}

/**
 * 返回单篇日报的完整内容
 * @param {string} date  格式 "2026-05-08"
 * @returns {{ date: string, title: string, htmlContent: string } | null}
 */
export async function getReport(date) {
  const filePath = path.join(REPORT_DIR, `${date}.md`)
  if (!fs.existsSync(filePath)) return null

  const raw = fs.readFileSync(filePath, 'utf-8')
  const { content } = matter(raw)

  const processed = await remark().use(remarkHtml, { sanitize: false }).process(content)
  const htmlContent = processed.toString()

  return {
    date,
    title: extractTitle(content, date),
    htmlContent,
  }
}
```

- [ ] **Step 2: 手动验证数据层可读取文件**

```bash
cd /Users/zcs/code2/news-intel/site
node -e "
const path = require('path');
const fs = require('fs');
const dir = path.join(process.cwd(), '..', 'report');
console.log('report dir:', dir);
console.log('exists:', fs.existsSync(dir));
console.log('files:', fs.readdirSync(dir).filter(f => f.endsWith('.md')));
"
```

预期：输出 8 个 `.md` 文件名。

- [ ] **Step 3: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/lib/reports.js
git commit -m "feat: add data layer lib/reports.js"
```

---

## Task 3: 全局布局和样式

**Files:**
- Create: `site/app/layout.js`
- Create: `site/app/globals.css`

- [ ] **Step 1: 创建 app/globals.css**

创建 `site/app/globals.css`：

```css
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,600;0,700;1,400;1,600&family=JetBrains+Mono:wght@400;500&family=Noto+Serif+SC:wght@400;600;700&display=swap');

:root {
  --bg:          #0e1117;
  --bg-card:     #161b27;
  --bg-hover:    #1c2333;
  --bg-sidebar:  #0b0f1a;
  --border:       #2a3040;
  --border-light: #1e2535;
  --text:         #f0f2f7;
  --text-sub:     #b8c0d0;
  --text-muted:   #7a8699;
  --text-dim:     #4e5a6e;
  --accent:       #4f8ef7;
  --accent-soft:  #3a6fd0;
  --accent-glow:  rgba(79, 142, 247, 0.10);
  --accent-line:  rgba(79, 142, 247, 0.30);
  --red:          #f26b5e;
  --green:        #5cba7d;
  --header-h:     52px;
  --mono:  'JetBrains Mono', 'Courier New', monospace;
  --serif: 'Newsreader', 'Noto Serif SC', Georgia, serif;
  --sans:  -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.75;
  min-height: 100dvh;
  -webkit-font-smoothing: antialiased;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
```

- [ ] **Step 2: 创建 app/layout.js**

创建 `site/app/layout.js`：

```js
import './globals.css'

export const metadata = {
  title: 'Intel Daily — 科技资讯日报',
  description: '每日 AI 与科技深度资讯，批判性分析',
}

export default function RootLayout({ children }) {
  return (
    <html lang="zh">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="alternate"
          type="application/rss+xml"
          title="Intel Daily RSS"
          href="/news-intel/feed.xml"
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

- [ ] **Step 3: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/layout.js site/app/globals.css
git commit -m "feat: add global layout and design tokens"
```

---

## Task 4: Sidebar 组件

**Files:**
- Create: `site/components/Sidebar.js`

- [ ] **Step 1: 创建 components/Sidebar.js**

创建 `site/components/Sidebar.js`：

```js
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Sidebar({ reports }) {
  const pathname = usePathname()

  return (
    <aside className="sidebar">
      <div className="sidebar-section">
        <div className="sidebar-label">
          归档 <span className="count-badge">{reports.length}</span>
        </div>
        <ul className="archive-list">
          {reports.map(r => {
            const href = `/news-intel/${r.date}/`
            const isActive = pathname === href || pathname === `/news-intel/${r.date}`
            const parts = r.date.split('-')
            const shortDate = parts.length === 3 ? `${parts[1]}/${parts[2]}` : r.date

            return (
              <li key={r.date} className="archive-item">
                <Link href={`/${r.date}/`} className={`archive-link${isActive ? ' active' : ''}`}>
                  <span className="archive-dot" />
                  <span className="archive-date desktop-date">{r.date}</span>
                  <span className="archive-date mobile-date">{shortDate}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </div>
    </aside>
  )
}
```

- [ ] **Step 2: 在 globals.css 末尾追加 Sidebar 样式**

在 `site/app/globals.css` 末尾追加：

```css
/* ── LAYOUT ── */
.site-wrapper {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr;
  min-height: 100dvh;
  max-width: 1400px;
  margin: 0 auto;
}

/* ── HEADER ── */
.site-header {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 0 2rem;
  height: var(--header-h);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  background: rgba(14,17,23,0.95);
  backdrop-filter: blur(14px);
  z-index: 100;
}

.site-logo {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--accent);
  white-space: nowrap;
  text-decoration: none;
}
.site-logo:hover { text-decoration: none; }

.site-header-sep { width: 1px; height: 14px; background: var(--border); }

.site-tagline { font-size: 12px; color: var(--text-muted); letter-spacing: 0.04em; }

.site-header-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-search-link {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--text-dim);
  letter-spacing: 0.1em;
  text-decoration: none;
  padding: 4px 8px;
  border: 1px solid var(--border);
  border-radius: 3px;
  transition: border-color 0.15s, color 0.15s;
}
.header-search-link:hover { border-color: var(--accent); color: var(--accent); text-decoration: none; }

/* ── SIDEBAR ── */
.sidebar {
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  padding: 1.5rem 0;
  position: sticky;
  top: var(--header-h);
  height: calc(100dvh - var(--header-h));
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar-section { padding: 0 1rem; margin-bottom: 1.5rem; }

.sidebar-label {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin-bottom: 0.75rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--mono);
  font-size: 9px;
  padding: 1px 5px;
  border: 1px solid var(--border);
  color: var(--text-muted);
  border-radius: 2px;
}

.archive-list { list-style: none; }
.archive-item { border-bottom: 1px solid var(--border-light); }

.archive-link {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 0.25rem;
  color: var(--text-muted);
  font-size: 12px;
  transition: color 0.15s;
  text-decoration: none;
}
.archive-link:hover { color: var(--text-sub); text-decoration: none; }
.archive-link.active { color: var(--text); }
.archive-link.active .archive-dot {
  background: var(--accent);
  box-shadow: 0 0 6px rgba(79, 142, 247, 0.5);
}
.archive-link.active .archive-date { color: var(--accent); }

.archive-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--border);
  flex-shrink: 0;
  transition: all 0.15s;
}

.archive-date {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-muted);
  flex-shrink: 0;
  transition: color 0.15s;
}

.mobile-date { display: none; }
.desktop-date { display: inline; }

/* ── MAIN CONTENT ── */
.main-content {
  padding: 2rem 3rem 4rem;
  overflow-x: hidden;
  max-width: 860px;
}

/* ── MOBILE ── */
@media (max-width: 768px) {
  .site-wrapper { grid-template-columns: 1fr; }

  .site-header { padding: 0 1rem; gap: 0.6rem; }
  .site-tagline, .site-header-sep { display: none; }
  .site-logo { font-size: 10px; }

  .sidebar {
    position: sticky;
    top: var(--header-h);
    height: auto;
    border-right: none;
    border-bottom: 1px solid var(--border);
    padding: 0;
    background: rgba(11,15,26,0.97);
    backdrop-filter: blur(12px);
    z-index: 90;
    overflow: hidden;
  }
  .sidebar-section { padding: 0; margin: 0; }
  .sidebar-label { display: none; }

  .archive-list {
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 0.5rem 1rem;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }
  .archive-list::-webkit-scrollbar { display: none; }

  .archive-item { border-bottom: none; flex-shrink: 0; }

  .archive-link {
    flex-direction: column;
    align-items: center;
    gap: 2px;
    padding: 0.3rem 0.65rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    margin-right: 0.4rem;
    white-space: nowrap;
    min-width: 52px;
  }
  .archive-link.active { border-color: var(--accent); background: var(--accent-glow); }
  .archive-link:hover { background: var(--bg-hover); text-decoration: none; }

  .archive-dot { display: none; }
  .archive-date { font-size: 11.5px; letter-spacing: 0; line-height: 1.2; }

  .desktop-date { display: none; }
  .mobile-date { display: inline; }

  .main-content { padding: 1.25rem 1rem 3rem; max-width: 100%; }
}

/* ── ANIMATIONS ── */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.report-fade-in { animation: fadeIn 0.2s ease-out; }

@media (prefers-reduced-motion: reduce) {
  .report-fade-in { animation: none; }
}

/* ── PRINT ── */
@media print {
  .sidebar, .site-header { display: none; }
  .site-wrapper { grid-template-columns: 1fr; }
  .main-content { padding: 0; max-width: 100%; }
  body { background: white; color: black; }
}
```

- [ ] **Step 3: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/components/Sidebar.js site/app/globals.css
git commit -m "feat: add Sidebar component and layout styles"
```

---

## Task 5: ReportBody 组件

**Files:**
- Create: `site/components/ReportBody.js`

- [ ] **Step 1: 创建 components/ReportBody.js**

创建 `site/components/ReportBody.js`：

```js
export default function ReportBody({ date, title, htmlContent }) {
  return (
    <div className="report-body report-fade-in">
      <div
        className="report-html"
        dangerouslySetInnerHTML={{ __html: htmlContent }}
      />
    </div>
  )
}
```

- [ ] **Step 2: 在 globals.css 末尾追加 ReportBody 样式**

在 `site/app/globals.css` 末尾追加：

```css
/* ── REPORT BODY ── */
.report-body { }

.report-html h1 {
  font-family: var(--serif);
  font-size: 1.9rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
  margin-bottom: 0.75rem;
  color: var(--text);
}

.report-html .report-intro,
.report-html blockquote:first-of-type {
  font-family: var(--mono);
  font-size: 11.5px;
  color: var(--text-muted);
  letter-spacing: 0.04em;
  padding: 0.65rem 1rem;
  border-left: 2px solid var(--accent-soft);
  background: var(--accent-glow);
  margin-bottom: 2.5rem;
  line-height: 1.7;
}

.report-html h2 {
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 3rem 0 1.25rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--border);
}

.report-html h3 {
  font-family: var(--serif);
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text);
  margin: 2rem 0 0.55rem;
  line-height: 1.45;
  letter-spacing: -0.01em;
}

.report-html p {
  color: var(--text-sub);
  margin-bottom: 0.85rem;
  line-height: 1.9;
  font-size: 15px;
}

.report-html blockquote {
  border-left: 2px solid var(--accent-line);
  margin: 1.25rem 0;
  padding: 0.65rem 1.1rem;
  background: var(--accent-glow);
  font-style: italic;
  font-size: 14px;
}
.report-html blockquote p { color: var(--text-muted); margin: 0; line-height: 1.7; }

.report-html strong { color: var(--text); font-weight: 600; }
.report-html em { font-style: italic; color: var(--text-sub); }

.report-html hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}

.report-html ul, .report-html ol {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}
.report-html li {
  color: var(--text-sub);
  margin: 0.3rem 0;
  font-size: 15px;
  line-height: 1.8;
}
.report-html li strong { color: var(--text); }

.report-html table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.25rem 0 1.75rem;
  font-size: 13.5px;
}
.report-html th {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-muted);
  text-align: left;
  padding: 0.55rem 0.85rem;
  border-bottom: 1px solid var(--border);
}
.report-html td {
  padding: 0.55rem 0.85rem;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-sub);
  vertical-align: top;
  line-height: 1.65;
}
.report-html tr:hover td { background: var(--bg-hover); }

.report-html code {
  font-family: var(--mono);
  font-size: 12.5px;
  background: var(--bg-card);
  color: var(--accent);
  padding: 2px 6px;
  border-radius: 3px;
  border: 1px solid var(--border);
}
.report-html pre {
  background: var(--bg-card);
  border: 1px solid var(--border);
  padding: 1.1rem;
  border-radius: 4px;
  overflow-x: auto;
  margin: 1.25rem 0;
}
.report-html pre code { background: none; border: none; padding: 0; font-size: 12.5px; color: var(--text-sub); }

@media (max-width: 768px) {
  .report-html h1 { font-size: 1.5rem; }
  .report-html h3 { font-size: 1.05rem; }
  .report-html p, .report-html li { font-size: 14.5px; }
  .report-html table {
    display: block;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    font-size: 12px;
  }
}
```

- [ ] **Step 3: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/components/ReportBody.js site/app/globals.css
git commit -m "feat: add ReportBody component and report styles"
```

---

## Task 6: 首页和日报页

**Files:**
- Create: `site/app/page.js`
- Create: `site/app/[date]/page.js`

- [ ] **Step 1: 创建首页 app/page.js**

创建 `site/app/page.js`：

```js
import { getAllReports, getReport } from '../lib/reports'
import Sidebar from '../components/Sidebar'
import ReportBody from '../components/ReportBody'
import Link from 'next/link'

export default async function HomePage() {
  const reports = getAllReports()
  const latest = reports[0]
  const report = latest ? await getReport(latest.date) : null

  return (
    <div className="site-wrapper">
      <header className="site-header">
        <Link href="/" className="site-logo">Intel Daily</Link>
        <span className="site-header-sep" />
        <span className="site-tagline">科技资讯 · 批判性分析 · 每日更新</span>
        <div className="site-header-right">
          <Link href="/search/" className="header-search-link">搜索</Link>
          <a href="/news-intel/feed.xml" className="header-search-link" target="_blank" rel="noopener">RSS</a>
        </div>
      </header>

      <Sidebar reports={reports} />

      <main className="main-content">
        {report ? (
          <ReportBody
            date={report.date}
            title={report.title}
            htmlContent={report.htmlContent}
          />
        ) : (
          <div className="welcome-screen">
            <div style={{ fontFamily: 'var(--mono)', color: 'var(--text-dim)', fontSize: '11px', letterSpacing: '0.1em' }}>
              暂无日报数据
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
```

- [ ] **Step 2: 创建日报页 app/[date]/page.js**

```bash
mkdir -p /Users/zcs/code2/news-intel/site/app/\[date\]
```

创建 `site/app/[date]/page.js`：

```js
import { getAllReports, getReport } from '../../lib/reports'
import Sidebar from '../../components/Sidebar'
import ReportBody from '../../components/ReportBody'
import Link from 'next/link'
import { notFound } from 'next/navigation'

export async function generateStaticParams() {
  const reports = getAllReports()
  return reports.map(r => ({ date: r.date }))
}

export async function generateMetadata({ params }) {
  const report = await getReport(params.date)
  if (!report) return { title: 'Not Found' }
  return { title: `${report.title} — Intel Daily` }
}

export default async function DatePage({ params }) {
  const reports = getAllReports()
  const report = await getReport(params.date)
  if (!report) notFound()

  return (
    <div className="site-wrapper">
      <header className="site-header">
        <Link href="/" className="site-logo">Intel Daily</Link>
        <span className="site-header-sep" />
        <span className="site-tagline">科技资讯 · 批判性分析 · 每日更新</span>
        <div className="site-header-right">
          <Link href="/search/" className="header-search-link">搜索</Link>
          <a href="/news-intel/feed.xml" className="header-search-link" target="_blank" rel="noopener">RSS</a>
        </div>
      </header>

      <Sidebar reports={reports} />

      <main className="main-content">
        <ReportBody
          date={report.date}
          title={report.title}
          htmlContent={report.htmlContent}
        />
      </main>
    </div>
  )
}
```

- [ ] **Step 3: 本地开发预览**

```bash
cd /Users/zcs/code2/news-intel/site
npm run dev
```

在浏览器打开 `http://localhost:3000/news-intel/`，验证：
- 最新日报内容正常显示
- Sidebar 列出所有日期
- 当前日期高亮
- 点击日期可跳转到对应页面

- [ ] **Step 4: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/page.js "site/app/[date]/page.js"
git commit -m "feat: add home page and date report pages"
```

---

## Task 7: RSS Feed

**Files:**
- Create: `site/app/feed.xml/route.js`

- [ ] **Step 1: 创建 RSS route**

```bash
mkdir -p /Users/zcs/code2/news-intel/site/app/feed.xml
```

创建 `site/app/feed.xml/route.js`：

```js
import { getAllReports } from '../../lib/reports'

const SITE_URL = 'https://cearl.cc'
const BASE_PATH = '/news-intel'

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

- [ ] **Step 2: 验证 RSS（dev 模式）**

```bash
cd /Users/zcs/code2/news-intel/site
npm run dev
```

访问 `http://localhost:3000/news-intel/feed.xml`，验证：
- 返回有效 XML
- 包含最近若干篇日报
- 每篇有标题、链接、日期、摘要

- [ ] **Step 3: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/feed.xml/route.js
git commit -m "feat: add RSS feed route"
```

---

## Task 8: 搜索页

**Files:**
- Create: `site/app/search/page.js`

注意：Pagefind 索引在 `npm run build` 后的 `postbuild` 阶段生成，开发模式下搜索框不会有结果，这是正常的。

- [ ] **Step 1: 创建搜索页**

```bash
mkdir -p /Users/zcs/code2/news-intel/site/app/search
```

创建 `site/app/search/page.js`：

```js
'use client'

import { useEffect } from 'react'
import Link from 'next/link'

export default function SearchPage() {
  useEffect(() => {
    // 动态加载 Pagefind UI（仅在构建后可用）
    async function loadPagefind() {
      if (typeof window === 'undefined') return
      try {
        const pagefind = await import('/news-intel/pagefind/pagefind.js')
        await pagefind.init()

        const { PagefindUI } = await import('/news-intel/pagefind/pagefind-ui.js')
        new PagefindUI({
          element: '#search-container',
          showImages: false,
          resetStyles: false,
        })
      } catch {
        // 开发模式下 pagefind 未生成，静默忽略
        console.info('Pagefind not available in dev mode')
      }
    }
    loadPagefind()
  }, [])

  return (
    <div className="site-wrapper">
      <header className="site-header">
        <Link href="/" className="site-logo">Intel Daily</Link>
        <span className="site-header-sep" />
        <span className="site-tagline">科技资讯 · 批判性分析 · 每日更新</span>
        <div className="site-header-right">
          <Link href="/search/" className="header-search-link" style={{ color: 'var(--accent)' }}>搜索</Link>
          <a href="/news-intel/feed.xml" className="header-search-link" target="_blank" rel="noopener">RSS</a>
        </div>
      </header>

      <div style={{ gridColumn: '1 / -1', padding: '3rem 3rem 4rem', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        <h1 style={{ fontFamily: 'var(--serif)', fontSize: '1.5rem', marginBottom: '2rem', color: 'var(--text)' }}>
          搜索日报
        </h1>
        <link rel="stylesheet" href="/news-intel/pagefind/pagefind-ui.css" />
        <div id="search-container" />
        <p style={{ marginTop: '2rem', fontSize: '12px', color: 'var(--text-dim)', fontFamily: 'var(--mono)' }}>
          搜索功能在构建后可用。开发模式下请先运行 <code>npm run build</code>。
        </p>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/search/page.js
git commit -m "feat: add search page with Pagefind UI"
```

---

## Task 9: 完整构建验证

**Files:** 无新文件，验证构建产物

- [ ] **Step 1: 执行完整构建**

```bash
cd /Users/zcs/code2/news-intel/site
npm run build
```

预期输出（关键行）：
```
Route (app)                  Size
┌ ○ /                        ...
├ ○ /feed.xml                ...
├ ○ /search                  ...
└ ● /[date]                  ...
    ├ /2026-05-08
    ├ /2026-05-07
    └ ... (所有日报)
```

- [ ] **Step 2: 验证 Pagefind 索引已生成**

```bash
ls /Users/zcs/code2/news-intel/site/out/pagefind/
```

预期：`pagefind.js`, `pagefind-ui.js`, `pagefind-ui.css`, 以及若干 `.pf_index` 文件。

- [ ] **Step 3: 本地预览构建产物**

```bash
cd /Users/zcs/code2/news-intel/site
npx serve out -p 4000
```

访问 `http://localhost:4000/news-intel/`，验证：
- 首页加载最新日报
- 侧边栏日期列表正常
- 点击日期跳转正确（URL 含 `/news-intel/2026-05-08/`）
- `http://localhost:4000/news-intel/feed.xml` 返回 XML
- `http://localhost:4000/news-intel/search/` 搜索框可用

- [ ] **Step 4: 验证 RSS 有效性**

```bash
curl -s http://localhost:4000/news-intel/feed.xml | head -20
```

预期：输出 `<?xml version="1.0"...` 开头的 RSS XML。

- [ ] **Step 5: Commit 构建产物**

```bash
cd /Users/zcs/code2/news-intel
# out/ 目录由 GitHub Actions 构建，本地的 out 不需要提交
# 确保 out/ 在 .gitignore 中
grep -q "^out/" site/.gitignore || echo "out/" >> site/.gitignore
git add site/.gitignore
git commit -m "chore: exclude out/ from git tracking"
```

---

## Task 10: 更新 GitHub Actions

**Files:**
- Modify: `.github/workflows/deploy.yml`

- [ ] **Step 1: 更新 deploy.yml**

用以下内容完整替换 `.github/workflows/deploy.yml`：

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'report/**.md'
      - 'site/**'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: site/package-lock.json

      - name: Install dependencies
        run: cd site && npm ci

      - name: Build site
        run: cd site && npm run build

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./site/out

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: 本地验证 YAML 语法**

```bash
cd /Users/zcs/code2/news-intel
cat .github/workflows/deploy.yml
```

确认内容正确，无缩进错误。

- [ ] **Step 3: Commit 并 push**

```bash
cd /Users/zcs/code2/news-intel
git add .github/workflows/deploy.yml
git commit -m "ci: switch deploy to Next.js build"
git push
```

- [ ] **Step 4: 观察 GitHub Actions 运行**

```bash
gh run list --repo chess99/news-intel --limit 3
```

等待 run 完成后：

```bash
gh run watch --repo chess99/news-intel $(gh run list --repo chess99/news-intel --limit 1 --json databaseId -q '.[0].databaseId')
```

预期：所有 steps 显示 ✓。

- [ ] **Step 5: 验证线上站点**

访问 `https://cearl.cc/news-intel/`，验证：
- 最新日报正常显示
- 侧边栏日期列表可点击
- `https://cearl.cc/news-intel/feed.xml` 可访问
- `https://cearl.cc/news-intel/search/` 搜索框可用

---

## 自检：Spec 覆盖

| Spec 要求 | 覆盖任务 |
|-----------|---------|
| 每篇日报独立 URL | Task 6（`/[date]/page.js`） |
| 首页展示最新日报，不跳转 | Task 6（`app/page.js`） |
| 全文搜索（Pagefind） | Task 8 + Task 9（postbuild） |
| RSS Feed（最近 20 篇） | Task 7 |
| `basePath: /news-intel` | Task 1（next.config.js） |
| `output: export` 静态导出 | Task 1（next.config.js） |
| 沿用现有设计 token | Task 3 + Task 4 + Task 5 |
| 移动端横向日期条 | Task 4（Sidebar 样式） |
| GitHub Actions 切换为 npm | Task 10 |
| `report/` 不动 | Task 2（lib/reports.js 相对路径） |
