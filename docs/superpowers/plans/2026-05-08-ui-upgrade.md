# UI Upgrade & Search Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复搜索功能、对齐问题和对比度问题，并对整体 UI 进行视觉升级，走「情报室」风格：深蓝黑底、细边框分割、monospace 点缀、内容优先。

**Architecture:** 所有改动集中在 CSS（`globals.css`）和三个页面组件（`search/page.js`、`app/page.js`、`app/[date]/page.js`）以及 `Sidebar.js`。不改变数据层和构建流程。

**Tech Stack:** Next.js 14 App Router, CSS Variables, Pagefind UI

---

## 文件结构

**修改：**
- `site/app/globals.css` — 全局样式升级：header 对齐、搜索页 Pagefind 样式覆盖、对比度修复、整体细节
- `site/app/search/page.js` — 修复搜索功能（Pagefind 加载路径 + 等待 DOM）、移除 dev 提示、改用全宽布局
- `site/app/page.js` — header 中搜索/RSS 入口视觉改善（已有但不够显眼）
- `site/app/[date]/page.js` — 与 page.js 保持一致
- `site/components/Sidebar.js` — 侧边栏底部加搜索/RSS 入口，搜索页 active 状态

**不改变：**
- `site/lib/reports.js`
- `site/app/layout.js`
- `site/components/ReportBody.js`
- `.github/workflows/deploy.yml`

---

## Task 1: 修复搜索功能 + 重设计搜索页

**问题：**
1. `PagefindUI` 构造函数在 script 加载完成时立即调用，但脚本注入到 `<head>` 后 `PagefindUI` 可能还未在 `window` 上注册（类定义在模块内）。需要改用轮询或事件等待。
2. Pagefind 默认 UI 样式是白色主题，覆盖不完整导致白底输入框漂浮在深色背景上。
3. "搜索功能在构建后可用" 提示不应在前端显示。
4. 搜索页布局用了 `gridColumn: '1 / -1'` 但没有利用好整个宽度。

**Files:**
- Modify: `site/app/search/page.js`
- Modify: `site/app/globals.css` (追加 Pagefind 样式覆盖)

- [ ] **Step 1: 重写 search/page.js**

完整替换 `site/app/search/page.js`：

```js
'use client'

import { useEffect, useRef } from 'react'
import Link from 'next/link'

export default function SearchPage() {
  const initialized = useRef(false)

  useEffect(() => {
    if (initialized.current) return
    initialized.current = true

    // Load pagefind-ui.css
    if (!document.querySelector('link[href*="pagefind-ui.css"]')) {
      const link = document.createElement('link')
      link.rel = 'stylesheet'
      link.href = '/news-intel/pagefind/pagefind-ui.css'
      document.head.appendChild(link)
    }

    // Load pagefind-ui.js and wait for PagefindUI to be available
    const script = document.createElement('script')
    script.src = '/news-intel/pagefind/pagefind-ui.js'
    script.type = 'text/javascript'
    script.onload = () => {
      // Poll until PagefindUI is available (it may register async)
      let attempts = 0
      const poll = setInterval(() => {
        attempts++
        if (typeof window.PagefindUI !== 'undefined') {
          clearInterval(poll)
          new window.PagefindUI({
            element: '#search-container',
            showImages: false,
            resetStyles: false,
            excerptLength: 20,
          })
        } else if (attempts > 20) {
          clearInterval(poll)
          console.warn('PagefindUI did not load in time')
        }
      }, 100)
    }
    script.onerror = () => console.info('Pagefind not available')
    document.head.appendChild(script)
  }, [])

  return (
    <div className="site-wrapper">
      <header className="site-header">
        <Link href="/" className="site-logo">Intel Daily</Link>
        <span className="site-header-sep" />
        <span className="site-tagline">科技资讯 · 批判性分析 · 每日更新</span>
        <div className="site-header-right">
          <Link href="/search/" className="header-nav-btn header-nav-btn--active" aria-label="搜索">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <span>搜索</span>
          </Link>
          <a
            href={`/news-intel/feed.xml`}
            className="header-nav-btn"
            target="_blank"
            rel="noopener"
            aria-label="RSS 订阅"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/>
            </svg>
            <span>RSS</span>
          </a>
        </div>
      </header>

      <div className="search-page-wrapper">
        <div className="search-page-inner">
          <h1 className="search-page-title">搜索日报</h1>
          <div id="search-container" className="search-container-wrap" />
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: 在 globals.css 末尾追加搜索页样式和 Pagefind 深色主题覆盖**

在 `site/app/globals.css` 末尾（`/* ── PRINT ── */` 之前）追加以下内容：

```css
/* ── SEARCH PAGE ── */
.search-page-wrapper {
  grid-column: 1 / -1;
  display: flex;
  justify-content: center;
  padding: 3rem 2rem 5rem;
}

.search-page-inner {
  width: 100%;
  max-width: 720px;
}

.search-page-title {
  font-family: var(--serif);
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 2rem;
  letter-spacing: -0.02em;
}

.search-container-wrap {
  /* Pagefind UI dark theme overrides */
}

/* Pagefind UI 深色主题强制覆盖 */
#search-container .pagefind-ui__search-input,
.pagefind-ui .pagefind-ui__search-input {
  background: var(--bg-card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
  font-family: var(--sans) !important;
  font-size: 15px !important;
  padding: 0.7rem 1rem 0.7rem 2.75rem !important;
  box-shadow: none !important;
  outline: none !important;
}
#search-container .pagefind-ui__search-input:focus,
.pagefind-ui .pagefind-ui__search-input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px var(--accent-glow) !important;
}

#search-container .pagefind-ui__search-clear,
.pagefind-ui .pagefind-ui__search-clear {
  background: var(--bg-hover) !important;
  color: var(--text-muted) !important;
  border: 1px solid var(--border) !important;
  border-radius: 3px !important;
  font-family: var(--mono) !important;
  font-size: 11px !important;
  letter-spacing: 0.05em !important;
  cursor: pointer !important;
}
#search-container .pagefind-ui__search-clear:hover,
.pagefind-ui .pagefind-ui__search-clear:hover {
  background: var(--bg-card) !important;
  color: var(--text) !important;
  border-color: var(--accent) !important;
}

#search-container .pagefind-ui__message,
.pagefind-ui .pagefind-ui__message {
  color: var(--text-muted) !important;
  font-size: 13px !important;
  font-family: var(--sans) !important;
}

#search-container .pagefind-ui__result,
.pagefind-ui .pagefind-ui__result {
  border-color: var(--border-light) !important;
  padding: 1.25rem 0 !important;
}

#search-container .pagefind-ui__result-link,
.pagefind-ui .pagefind-ui__result-link {
  color: var(--text) !important;
  font-family: var(--serif) !important;
  font-size: 1.05rem !important;
  font-weight: 600 !important;
  text-decoration: none !important;
}
#search-container .pagefind-ui__result-link:hover,
.pagefind-ui .pagefind-ui__result-link:hover {
  color: var(--accent) !important;
}

#search-container .pagefind-ui__result-excerpt,
.pagefind-ui .pagefind-ui__result-excerpt {
  color: var(--text-sub) !important;
  font-size: 13.5px !important;
  line-height: 1.7 !important;
  margin-top: 0.4rem !important;
}

#search-container .pagefind-ui__result-excerpt mark,
.pagefind-ui .pagefind-ui__result-excerpt mark {
  background: rgba(79, 142, 247, 0.2) !important;
  color: var(--accent) !important;
  border-radius: 2px !important;
  padding: 0 2px !important;
}

#search-container .pagefind-ui__button,
.pagefind-ui .pagefind-ui__button {
  background: var(--bg-card) !important;
  color: var(--text-muted) !important;
  border: 1px solid var(--border) !important;
  border-radius: 3px !important;
  font-family: var(--mono) !important;
  font-size: 11px !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  cursor: pointer !important;
  padding: 0.5rem 1.25rem !important;
  transition: border-color 0.15s, color 0.15s !important;
}
#search-container .pagefind-ui__button:hover,
.pagefind-ui .pagefind-ui__button:hover {
  border-color: var(--accent) !important;
  color: var(--accent) !important;
}

/* 修复搜索框内图标颜色（如有） */
.pagefind-ui__search-input::placeholder {
  color: var(--text-dim) !important;
}

@media (max-width: 768px) {
  .search-page-wrapper { padding: 2rem 1rem 4rem; }
  .search-page-title { font-size: 1.3rem; }
}
```

- [ ] **Step 3: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/search/page.js site/app/globals.css
git commit -m "fix: repair search functionality and redesign search page with dark theme"
```

---

## Task 2: 升级 Header — 对齐修复 + 导航按钮重设计

**问题：**
- `header-search-link` 用 `font-size: 10px` + `color: var(--text-dim)` 导致对比度不足且视觉偏小
- 按钮 `border-radius: 3px` 加文字，在视觉上显得孤立，不像导航元素
- 首页有搜索/RSS 按钮，但配色太暗导致「没有入口」的感觉

**Files:**
- Modify: `site/app/globals.css` (修改 `.header-search-link` → 新增 `.header-nav-btn`)
- Modify: `site/app/page.js`
- Modify: `site/app/[date]/page.js`

- [ ] **Step 1: 在 globals.css 中替换 .header-search-link 样式**

找到 globals.css 中的：
```css
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
```

**替换为：**
```css
.header-nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 0.1em;
  text-decoration: none;
  padding: 5px 10px;
  border: 1px solid var(--border);
  border-radius: 3px;
  transition: border-color 0.15s, color 0.15s, background 0.15s;
  cursor: pointer;
  white-space: nowrap;
}
.header-nav-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
  text-decoration: none;
}
.header-nav-btn--active {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-glow);
}
.header-nav-btn svg { flex-shrink: 0; }

/* 保留旧类名兼容 */
.header-search-link { display: none; }
```

- [ ] **Step 2: 更新 app/page.js 中的 header**

完整替换 `site/app/page.js`：

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
          <Link href="/search/" className="header-nav-btn" aria-label="搜索">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <span>搜索</span>
          </Link>
          <a
            href={`${process.env.NEXT_PUBLIC_BASE_PATH}/feed.xml`}
            className="header-nav-btn"
            target="_blank"
            rel="noopener"
            aria-label="RSS 订阅"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/>
            </svg>
            <span>RSS</span>
          </a>
        </div>
      </header>

      <Sidebar reports={reports} latestDate={reports[0]?.date} />

      <main className="main-content">
        {report ? (
          <ReportBody htmlContent={report.htmlContent} />
        ) : (
          <div style={{ padding: '4rem', fontFamily: 'var(--mono)', color: 'var(--text-muted)', fontSize: '12px', letterSpacing: '0.1em' }}>
            暂无日报数据
          </div>
        )}
      </main>
    </div>
  )
}
```

- [ ] **Step 3: 更新 app/[date]/page.js 的 header（与 page.js 保持一致）**

完整替换 `site/app/[date]/page.js`：

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
          <Link href="/search/" className="header-nav-btn" aria-label="搜索">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <span>搜索</span>
          </Link>
          <a
            href={`${process.env.NEXT_PUBLIC_BASE_PATH}/feed.xml`}
            className="header-nav-btn"
            target="_blank"
            rel="noopener"
            aria-label="RSS 订阅"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/>
            </svg>
            <span>RSS</span>
          </a>
        </div>
      </header>

      <Sidebar reports={reports} latestDate={reports[0]?.date} />

      <main className="main-content">
        <ReportBody htmlContent={report.htmlContent} />
      </main>
    </div>
  )
}
```

- [ ] **Step 4: 验证构建**

```bash
cd /Users/zcs/code2/news-intel/site
npm run build 2>&1 | tail -10
```

预期：构建成功，无报错。

- [ ] **Step 5: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/globals.css site/app/page.js "site/app/[date]/page.js"
git commit -m "feat: redesign header nav buttons with SVG icons and better contrast"
```

---

## Task 3: Sidebar 底部添加导航入口 + 视觉细节升级

**改动：**
- Sidebar 底部固定区域：搜索链接 + RSS 链接（对移动端尤其重要，header 按钮在移动端会被收窄）
- `sidebar-label` 文字颜色从 `--text-dim` 提升到 `--text-muted`（当前 `#4e5a6e` 对比度不足）

**Files:**
- Modify: `site/components/Sidebar.js`
- Modify: `site/app/globals.css`

- [ ] **Step 1: 更新 Sidebar.js，添加底部导航区**

完整替换 `site/components/Sidebar.js`：

```js
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Sidebar({ reports, latestDate }) {
  const pathname = usePathname()

  return (
    <aside className="sidebar">
      <div className="sidebar-section">
        <div className="sidebar-label">
          归档 <span className="count-badge">{reports.length}</span>
        </div>
        <ul className="archive-list">
          {reports.map(r => {
            const isActive =
              pathname === `/${r.date}/` ||
              pathname === `/${r.date}` ||
              (pathname === '/' && r.date === latestDate)
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

      <div className="sidebar-footer">
        <Link
          href="/search/"
          className={`sidebar-footer-link${pathname === '/search/' || pathname === '/search' ? ' active' : ''}`}
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
          搜索
        </Link>
        <a
          href="/news-intel/feed.xml"
          className="sidebar-footer-link"
          target="_blank"
          rel="noopener"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/>
          </svg>
          RSS
        </a>
      </div>
    </aside>
  )
}
```

- [ ] **Step 2: 在 globals.css 中修改 sidebar-label 对比度并追加 sidebar-footer 样式**

在 globals.css 中，找到：
```css
.sidebar-label {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-dim);
```

把 `color: var(--text-dim);` 改为 `color: var(--text-muted);`

然后在 `/* ── MAIN CONTENT ── */` 注释之前追加：

```css
.sidebar-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.75rem 1rem;
  border-top: 1px solid var(--border-light);
  background: var(--bg-sidebar);
  display: flex;
  gap: 0.5rem;
}

.sidebar-footer-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  text-decoration: none;
  padding: 4px 8px;
  border: 1px solid var(--border);
  border-radius: 3px;
  transition: border-color 0.15s, color 0.15s;
  cursor: pointer;
}
.sidebar-footer-link:hover,
.sidebar-footer-link.active {
  color: var(--accent);
  border-color: var(--accent);
  text-decoration: none;
}
```

同时在 `.sidebar` 样式中确保 `position: relative;`（已有 `sticky` 定位，需要加 `position: relative` 到内层容器）。

实际上 sidebar 已经是 `position: sticky`，`sidebar-footer` 用 `position: absolute` 需要 sidebar 有 `position` 上下文。由于 sidebar 是 `position: sticky`，已是定位上下文，`absolute` 会相对 sticky 父元素定位。这没问题。

另外需要给 `.sidebar-section` 加底部 padding，防止内容被 footer 遮住：

在 globals.css 的 `.sidebar-section` 规则末尾加：
```css
.sidebar-section:last-of-type { padding-bottom: 3.5rem; }
```

- [ ] **Step 3: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/components/Sidebar.js site/app/globals.css
git commit -m "feat: add sidebar footer nav links, fix sidebar-label contrast"
```

---

## Task 4: 整体视觉细节升级

**改动清单：**
- `--text-dim: #4e5a6e` → 提升到 `#5d6b82`（仍是装饰性，但稍微可见）
- header 高度从 52px → 54px，左右 padding 更宽松
- `.main-content` 加 `padding-top: 2.5rem`，与 header 分离感更好
- `.report-html h1` 前加日期标注（通过 CSS 伪元素无法实现，跳过）
- `.archive-link` hover 状态加背景色，而不只是颜色变化
- 搜索/RSS 按钮在移动端的处理

**Files:**
- Modify: `site/app/globals.css`

- [ ] **Step 1: 应用细节修复到 globals.css**

**修改 1：提升 --text-dim 对比度**

找到：
```css
  --text-dim:     #4e5a6e;
```
替换为：
```css
  --text-dim:     #5d6b82;
```

**修改 2：archive-link hover 加背景**

找到：
```css
.archive-link:hover { color: var(--text-sub); text-decoration: none; }
```
替换为：
```css
.archive-link:hover { color: var(--text-sub); background: rgba(255,255,255,0.02); text-decoration: none; }
```

**修改 3：移动端 header-nav-btn 文字隐藏，只保留图标（防止拥挤）**

在 `@media (max-width: 768px)` 块内追加：
```css
  .header-nav-btn span { display: none; }
  .header-nav-btn { padding: 6px 8px; min-width: 32px; justify-content: center; }
  .site-header-right { gap: 0.5rem; }
```

**修改 4：`.report-html h2` 前加左装饰线**

找到：
```css
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
```
替换为：
```css
.report-html h2 {
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 3rem 0 1.25rem;
  padding-bottom: 0.6rem;
  padding-left: 0.75rem;
  border-bottom: 1px solid var(--border);
  border-left: 2px solid var(--accent);
}
```

- [ ] **Step 2: 验证构建**

```bash
cd /Users/zcs/code2/news-intel/site
npm run build 2>&1 | tail -10
```

预期：构建成功。

- [ ] **Step 3: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/globals.css
git commit -m "feat: visual polish - contrast, hover states, mobile nav, h2 decoration"
```

---

## Task 5: Push 并验证线上

- [ ] **Step 1: Push 到 main**

```bash
cd /Users/zcs/code2/news-intel
git push
```

- [ ] **Step 2: 等待 GitHub Actions 完成**

```bash
sleep 5
RUN_ID=$(gh run list --repo chess99/news-intel --limit 1 --json databaseId -q '.[0].databaseId')
gh run watch $RUN_ID --repo chess99/news-intel
```

- [ ] **Step 3: 验证线上**

```bash
curl -s -o /dev/null -w "%{http_code}" https://cearl.cc/news-intel/
curl -s -o /dev/null -w "%{http_code}" https://cearl.cc/news-intel/search/
curl -s -o /dev/null -w "%{http_code}" https://cearl.cc/news-intel/feed.xml
```

预期：三个都返回 200。

- [ ] **Step 4: Commit（如有未提交内容）**

```bash
cd /Users/zcs/code2/news-intel
git status
# 如有未提交内容再 commit，否则跳过
```

---

## 自检：需求覆盖

| 用户反馈 | 对应 Task |
|---------|----------|
| 搜索功能不可用（"正在搜索"卡住） | Task 1（轮询等待 PagefindUI 注册） |
| "搜索功能在构建后可用" 提示不该显示 | Task 1（search/page.js 移除该提示） |
| "搜索" 按钮歪 | Task 2（`display: inline-flex; align-items: center`） |
| 搜索框下方文字对比度不行 | Task 1（移除了该提示段落） + Task 4（`--text-dim` 提升） |
| 首页没有搜索/RSS 入口 | Task 2（header 按钮提升对比度）+ Task 3（sidebar footer） |
| 整体 UI 升级 | Task 2-4（header 图标按钮、h2 装饰线、hover 背景、细节）|
| Pagefind 白色主题漂浮 | Task 1（完整深色主题覆盖） |
