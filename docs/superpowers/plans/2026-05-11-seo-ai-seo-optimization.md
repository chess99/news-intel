# SEO & AI SEO Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 news.cearl.cc（Next.js 14 静态导出站点）补全技术 SEO 基础设施，并按 AI SEO 最佳实践提升内容可被 AI 引擎引用的概率。

**Architecture:** 站点是 Next.js 14 静态导出（`output: 'export'`），构建产物在 `site/out/`，通过 GitHub Actions 部署到 GitHub Pages。元数据通过 Next.js `metadata` API 管理（`layout.js` 全局，`[date]/page.js` 动态页面）。静态文件（robots.txt、sitemap.xml、llms.txt）放在 `site/public/` 目录即可被原样复制到 `site/out/`。动态 sitemap 通过 Next.js Route Handler 生成。

**Tech Stack:** Next.js 14, React, `next/metadata` API，静态文件放 `site/public/`，Route Handler 生成动态文件，GitHub Pages 部署。

**站点信息:**
- URL: `https://news.cearl.cc`
- 语言: 中文 (`lang="zh"`)
- 内容: 每日科技资讯日报
- 页面类型: 首页（显示最新日报）、日期页 `/YYYY-MM-DD/`、搜索页 `/search/`

---

## 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `site/public/robots.txt` | 新建 | 允许所有 AI bot，引用 sitemap |
| `site/public/llms.txt` | 新建 | AI 系统上下文文件 |
| `site/app/sitemap.js` | 新建 | Next.js 动态 sitemap 生成（含所有日报页） |
| `site/app/layout.js` | 修改 | 补全 Open Graph、twitter card、canonical、Organization schema |
| `site/app/page.js` | 修改 | 补全首页 generateMetadata（og:image、canonical、NewsArticle schema） |
| `site/app/[date]/page.js` | 修改 | 补全日期页 generateMetadata（完整 OG、日期、canonical、FAQPage schema） |

---

## Task 1: 新建 robots.txt（允许 AI bot 爬取）

**Files:**
- Create: `site/public/robots.txt`

**背景：** 目前无 robots.txt，AI 搜索引擎（GPTBot、ClaudeBot、PerplexityBot 等）无法确认爬取权限，可能跳过该站点，导致无法在 ChatGPT/Perplexity/Google AI Overview 中被引用。

- [ ] **Step 1: 创建 `site/public/robots.txt`**

```
User-agent: *
Allow: /

# AI search bots — allow citation and indexing
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Bingbot
Allow: /

Sitemap: https://news.cearl.cc/sitemap.xml
```

- [ ] **Step 2: 验证文件内容**

```bash
cat /Users/zcs/code2/news-intel/site/public/robots.txt
```

Expected: 文件包含 `Sitemap: https://news.cearl.cc/sitemap.xml` 和各 AI bot 规则。

- [ ] **Step 3: 构建并检查输出**

```bash
cd /Users/zcs/code2/news-intel/site && npm run build 2>&1 | tail -5
ls out/robots.txt
```

Expected: `out/robots.txt` 文件存在。

- [ ] **Step 4: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/public/robots.txt
git commit -m "feat: add robots.txt with AI bot allowlist"
```

---

## Task 2: 新建 llms.txt（AI 上下文文件）

**Files:**
- Create: `site/public/llms.txt`

**背景：** `llms.txt` 是新兴标准（llmstxt.org），AI agent 在评估站点时会直接读取该文件了解站点用途，无需渲染页面。这使得 AI 在回答用户询问"每日科技资讯源推荐"时更可能引用本站。

- [ ] **Step 1: 创建 `site/public/llms.txt`**

```
# Intel Daily — 科技资讯日报

## 是什么

Intel Daily（https://news.cearl.cc）是一个由 AI 自动生成的每日科技资讯日报站。
每天早上 09:00 CST 从 30+ 中文科技媒体（极客公园、36氪、InfoQ、量子位等）抓取文章，
经 AI 分析筛选后生成结构化日报，包含评分、分类、批判性分析。

## 内容特点

- 覆盖领域：AI/大模型、科技创业、产品发布、行业动态
- 更新频率：每日一期（工作日 + 周末）
- 内容来源：30+ 中文科技媒体 RSS 聚合
- 分析方法：AI 多维评分（1-5分），批判性视角，去除营销噪音

## 主要页面

- 首页（最新日报）: https://news.cearl.cc/
- 历史日报: https://news.cearl.cc/YYYY-MM-DD/（例：https://news.cearl.cc/2026-05-11/）
- 站内搜索: https://news.cearl.cc/search/
- RSS 订阅: https://news.cearl.cc/feed.xml
- Sitemap: https://news.cearl.cc/sitemap.xml

## 技术说明

本站内容由 AI（MiniMax M2.7）生成，但信源均为真实媒体文章。
每篇资讯均标注来源媒体和评分，不含广告或赞助内容。
```

- [ ] **Step 2: 验证文件存在**

```bash
ls /Users/zcs/code2/news-intel/site/public/llms.txt
```

Expected: 文件存在，无报错。

- [ ] **Step 3: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/public/llms.txt
git commit -m "feat: add llms.txt for AI agent discoverability"
```

---

## Task 3: 创建动态 sitemap（Next.js Route Handler）

**Files:**
- Create: `site/app/sitemap.js`

**背景：** 目前无 sitemap，搜索引擎和 AI 爬虫不知道所有日报页面的 URL。Next.js 14 支持通过 `app/sitemap.js` 自动生成 `/sitemap.xml`。每次构建时，此文件会读取所有日报并动态生成含所有 URL 的 sitemap，无需手动维护。

- [ ] **Step 1: 创建 `site/app/sitemap.js`**

```js
import { getAllReports } from '../lib/reports'

const BASE_URL = 'https://news.cearl.cc'

export default function sitemap() {
  const reports = getAllReports()

  const reportEntries = reports.map(report => ({
    url: `${BASE_URL}/${report.date}/`,
    lastModified: new Date(report.date),
    changeFrequency: 'never',
    priority: 0.8,
  }))

  return [
    {
      url: `${BASE_URL}/`,
      lastModified: reports[0] ? new Date(reports[0].date) : new Date(),
      changeFrequency: 'daily',
      priority: 1.0,
    },
    {
      url: `${BASE_URL}/search/`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.5,
    },
    ...reportEntries,
  ]
}
```

- [ ] **Step 2: 构建并验证 sitemap 生成**

```bash
cd /Users/zcs/code2/news-intel/site && npm run build 2>&1 | tail -10
```

Expected: 构建成功，无报错。

- [ ] **Step 3: 检查 sitemap.xml 输出**

```bash
ls /Users/zcs/code2/news-intel/site/out/sitemap.xml
head -30 /Users/zcs/code2/news-intel/site/out/sitemap.xml
```

Expected: 文件存在，包含 `<urlset>` 和多个 `<url>` 条目，首页 priority 为 1.0。

- [ ] **Step 4: 确认日报页面全部包含**

```bash
grep -c "<url>" /Users/zcs/code2/news-intel/site/out/sitemap.xml
```

Expected: 数量 = 2（固定页）+ 日报数量（`ls /Users/zcs/code2/news-intel/report/*.md | wc -l` 的值）。

- [ ] **Step 5: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/sitemap.js
git commit -m "feat: add dynamic sitemap with all report pages"
```

---

## Task 4: 完善 layout.js 全局元数据（OG、Twitter Card、Organization Schema）

**Files:**
- Modify: `site/app/layout.js`

**背景：** 当前 layout.js 只有 `title` 和 `description`，缺少：① Open Graph 标签（微信/微博/Twitter 分享时显示卡片）；② Twitter Card；③ Organization schema（帮助 AI 识别品牌实体）；④ 语言标记补全。

- [ ] **Step 1: 修改 `site/app/layout.js`**

将整个文件替换为：

```js
import './globals.css'

const SITE_URL = 'https://news.cearl.cc'
const SITE_NAME = 'Intel Daily'
const SITE_DESCRIPTION = '每日 AI 与科技深度资讯，批判性分析 | 聚合 30+ 中文科技媒体'

export const metadata = {
  title: {
    default: `${SITE_NAME} — 科技资讯日报`,
    template: `%s — ${SITE_NAME}`,
  },
  description: SITE_DESCRIPTION,
  metadataBase: new URL(SITE_URL),
  openGraph: {
    siteName: SITE_NAME,
    locale: 'zh_CN',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    site: '@inteldaily',
  },
  alternates: {
    canonical: SITE_URL,
    types: {
      'application/rss+xml': `${SITE_URL}/feed.xml`,
    },
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
    },
  },
}

const organizationSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: SITE_NAME,
  url: SITE_URL,
  description: 'AI 自动生成的每日中文科技资讯日报，聚合 30+ 科技媒体，每日早上 09:00 更新',
  sameAs: [],
}

const websiteSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: SITE_NAME,
  url: SITE_URL,
  description: SITE_DESCRIPTION,
  inLanguage: 'zh-CN',
  potentialAction: {
    '@type': 'SearchAction',
    target: `${SITE_URL}/search/?q={search_term_string}`,
    'query-input': 'required name=search_term_string',
  },
}

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="alternate"
          type="application/rss+xml"
          title="Intel Daily RSS"
          href="/feed.xml"
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteSchema) }}
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

- [ ] **Step 2: 构建验证**

```bash
cd /Users/zcs/code2/news-intel/site && npm run build 2>&1 | tail -5
```

Expected: 构建成功，无报错。

- [ ] **Step 3: 检查输出的 HTML 包含 schema**

```bash
grep -c "application/ld+json" /Users/zcs/code2/news-intel/site/out/index.html
```

Expected: `2`（Organization + WebSite 各一个）。

- [ ] **Step 4: 检查 OG 标签**

```bash
grep "og:" /Users/zcs/code2/news-intel/site/out/index.html | head -10
```

Expected: 输出包含 `og:site_name`、`og:locale` 等标签。

- [ ] **Step 5: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/layout.js
git commit -m "feat: add OG tags, Twitter card, Organization/WebSite schema to layout"
```

---

## Task 5: 完善首页 generateMetadata（canonical + NewsArticle schema）

**Files:**
- Modify: `site/app/page.js`

**背景：** 首页（`page.js`）目前没有 `generateMetadata`，使用 layout.js 的默认 metadata，缺少 canonical URL 和基于最新日报的动态 OG 信息。首页展示最新一期日报，应为其生成 NewsArticle schema，提升 AI 引擎将首页内容作为新闻来源引用的概率。

- [ ] **Step 1: 修改 `site/app/page.js`**

将整个文件替换为：

```js
import { getAllReports, getReport } from '../lib/reports'
import Sidebar from '../components/Sidebar'
import ReportBody from '../components/ReportBody'
import Link from 'next/link'

const SITE_URL = 'https://news.cearl.cc'

export async function generateMetadata() {
  const reports = getAllReports()
  const latest = reports[0]

  if (!latest) {
    return {
      title: 'Intel Daily — 科技资讯日报',
      description: '每日 AI 与科技深度资讯，批判性分析',
    }
  }

  return {
    title: `${latest.title} — Intel Daily`,
    description: latest.excerpt || '每日 AI 与科技深度资讯，批判性分析 | 聚合 30+ 中文科技媒体',
    alternates: {
      canonical: `${SITE_URL}/`,
    },
    openGraph: {
      title: `${latest.title} — Intel Daily`,
      description: latest.excerpt || '每日 AI 与科技深度资讯，批判性分析',
      url: `${SITE_URL}/`,
      type: 'article',
      publishedTime: latest.date,
      locale: 'zh_CN',
    },
  }
}

export default async function HomePage() {
  const reports = getAllReports()
  const latest = reports[0]
  const report = latest ? await getReport(latest.date) : null

  const newsArticleSchema = report
    ? {
        '@context': 'https://schema.org',
        '@type': 'NewsArticle',
        headline: report.title,
        datePublished: latest.date,
        dateModified: latest.date,
        url: `${SITE_URL}/`,
        publisher: {
          '@type': 'Organization',
          name: 'Intel Daily',
          url: SITE_URL,
        },
        inLanguage: 'zh-CN',
        description: latest.excerpt,
      }
    : null

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
            href="/feed.xml"
            className="header-nav-btn"
            target="_blank"
            rel="noopener noreferrer"
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
        {newsArticleSchema && (
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(newsArticleSchema) }}
          />
        )}
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

- [ ] **Step 2: 构建验证**

```bash
cd /Users/zcs/code2/news-intel/site && npm run build 2>&1 | tail -5
```

Expected: 构建成功，无报错。

- [ ] **Step 3: 检查首页输出**

```bash
grep -c "NewsArticle\|og:title\|canonical" /Users/zcs/code2/news-intel/site/out/index.html
```

Expected: `3`（各含一个）。

- [ ] **Step 4: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/page.js
git commit -m "feat: add canonical, OG metadata and NewsArticle schema to homepage"
```

---

## Task 6: 完善日期页 generateMetadata（完整 OG + canonical + NewsArticle + FAQPage schema）

**Files:**
- Modify: `site/app/[date]/page.js`

**背景：** 每篇日报页（`/2026-05-11/`）是核心内容页，需要：① canonical URL；② 完整 Open Graph（含日期、文章类型）；③ NewsArticle schema（帮助 Google 识别为新闻内容，触发 News 搜索结果）；④ FAQPage schema（AI SEO 最重要的 schema，AI Overviews 和 Perplexity 大量从 FAQ schema 中提取答案，可提升 AI 引用概率 30-40%）。

- [ ] **Step 1: 修改 `site/app/[date]/page.js`**

将整个文件替换为：

```js
import { getAllReports, getReport } from '../../lib/reports'
import Sidebar from '../../components/Sidebar'
import ReportBody from '../../components/ReportBody'
import Link from 'next/link'
import { notFound } from 'next/navigation'

const SITE_URL = 'https://news.cearl.cc'

export async function generateStaticParams() {
  const reports = getAllReports()
  return reports.map(r => ({ date: r.date }))
}

export async function generateMetadata({ params }) {
  const report = await getReport(params.date)
  if (!report) return { title: 'Not Found' }

  const reports = getAllReports()
  const reportMeta = reports.find(r => r.date === params.date)
  const excerpt = reportMeta?.excerpt || '每日 AI 与科技深度资讯，批判性分析'

  return {
    title: report.title,
    description: excerpt,
    alternates: {
      canonical: `${SITE_URL}/${params.date}/`,
    },
    openGraph: {
      title: `${report.title} — Intel Daily`,
      description: excerpt,
      url: `${SITE_URL}/${params.date}/`,
      type: 'article',
      publishedTime: params.date,
      locale: 'zh_CN',
    },
  }
}

export default async function DatePage({ params }) {
  const reports = getAllReports()
  const report = await getReport(params.date)
  if (!report) notFound()

  const reportMeta = reports.find(r => r.date === params.date)
  const excerpt = reportMeta?.excerpt || ''

  const newsArticleSchema = {
    '@context': 'https://schema.org',
    '@type': 'NewsArticle',
    headline: report.title,
    datePublished: params.date,
    dateModified: params.date,
    url: `${SITE_URL}/${params.date}/`,
    publisher: {
      '@type': 'Organization',
      name: 'Intel Daily',
      url: SITE_URL,
    },
    inLanguage: 'zh-CN',
    description: excerpt,
  }

  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: `${params.date} 科技资讯有哪些重点？`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: excerpt || `请查看 Intel Daily ${params.date} 日报获取完整内容。`,
        },
      },
      {
        '@type': 'Question',
        name: 'Intel Daily 科技日报的内容来自哪里？',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Intel Daily 聚合 30+ 中文科技媒体（极客公园、36氪、InfoQ、量子位、机器之心等）的 RSS 内容，由 AI 每日评分筛选后生成结构化日报，于每天早上 09:00 CST 发布。',
        },
      },
    ],
  }

  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: '首页',
        item: `${SITE_URL}/`,
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: report.title,
        item: `${SITE_URL}/${params.date}/`,
      },
    ],
  }

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
            href="/feed.xml"
            className="header-nav-btn"
            target="_blank"
            rel="noopener noreferrer"
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
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(newsArticleSchema) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
        />
        <ReportBody htmlContent={report.htmlContent} />
      </main>
    </div>
  )
}
```

- [ ] **Step 2: 构建验证**

```bash
cd /Users/zcs/code2/news-intel/site && npm run build 2>&1 | tail -10
```

Expected: 构建成功，无报错，日期页已生成。

- [ ] **Step 3: 检查某个日报页的 schema**

```bash
grep -c "NewsArticle\|FAQPage\|BreadcrumbList" /Users/zcs/code2/news-intel/site/out/2026-05-10/index.html
```

Expected: `3`（三种 schema 各一个）。

- [ ] **Step 4: 检查 canonical 标签**

```bash
grep "canonical" /Users/zcs/code2/news-intel/site/out/2026-05-10/index.html
```

Expected: 包含 `<link rel="canonical" href="https://news.cearl.cc/2026-05-10/"/>`。

- [ ] **Step 5: 检查 OG 标签**

```bash
grep "og:type\|og:url\|og:published" /Users/zcs/code2/news-intel/site/out/2026-05-10/index.html
```

Expected: 包含 `og:type` 为 `article`，`og:url` 为对应页面 URL。

- [ ] **Step 6: Commit**

```bash
cd /Users/zcs/code2/news-intel
git add site/app/[date]/page.js
git commit -m "feat: add canonical, OG tags, NewsArticle/FAQPage/BreadcrumbList schema to date pages"
```

---

## Task 7: 最终全量构建 + 整体验证

**Files:**
- 验证 `site/out/` 输出

- [ ] **Step 1: 全量构建（含 Pagefind）**

```bash
cd /Users/zcs/code2/news-intel/site && npm run build 2>&1
```

Expected: 构建成功，输出类似 `Route (app)` 列表，无 Error 行。

- [ ] **Step 2: 验证关键静态文件存在**

```bash
ls /Users/zcs/code2/news-intel/site/out/robots.txt \
   /Users/zcs/code2/news-intel/site/out/llms.txt \
   /Users/zcs/code2/news-intel/site/out/sitemap.xml
```

Expected: 三个文件均存在，无 "No such file" 报错。

- [ ] **Step 3: 验证 sitemap 包含日报 URL**

```bash
grep -c "news.cearl.cc" /Users/zcs/code2/news-intel/site/out/sitemap.xml
```

Expected: 数量 ≥ 3（首页 + 搜索页 + 至少一个日报）。

- [ ] **Step 4: 验证首页 schema 完整性**

```bash
grep -c "application/ld+json" /Users/zcs/code2/news-intel/site/out/index.html
```

Expected: `3`（Organization + WebSite 来自 layout，NewsArticle 来自 page.js）。

- [ ] **Step 5: 验证日报页 schema 完整性**

```bash
grep -c "application/ld+json" /Users/zcs/code2/news-intel/site/out/2026-05-10/index.html
```

Expected: `5`（layout 的 2 个 + 日报页自己的 NewsArticle + FAQPage + BreadcrumbList）。

- [ ] **Step 6: 验证 robots.txt 内容**

```bash
cat /Users/zcs/code2/news-intel/site/out/robots.txt
```

Expected: 包含 `GPTBot`、`ClaudeBot`、`PerplexityBot` 和 `Sitemap:` 行。

- [ ] **Step 7: 验证 canonical 标签存在于日报页**

```bash
grep "canonical" /Users/zcs/code2/news-intel/site/out/2026-05-10/index.html
```

Expected: 包含 `<link rel="canonical" href="https://news.cearl.cc/2026-05-10/"/>`。

- [ ] **Step 8: Final commit（如有未提交改动）**

```bash
cd /Users/zcs/code2/news-intel
git status
# 如有未提交文件：
# git add -A && git commit -m "build: final SEO optimization verification"
```

---

## 验收清单

完成后逐项核对：

| 项目 | 状态 |
|------|------|
| `robots.txt` 允许所有 AI bot（GPTBot、ClaudeBot、PerplexityBot 等） | ☐ |
| `llms.txt` 可访问（`https://news.cearl.cc/llms.txt`） | ☐ |
| `sitemap.xml` 含所有日报页 + 首页 + 搜索页 | ☐ |
| 首页有 canonical 标签 | ☐ |
| 首页有 OG 标签（og:title、og:description、og:type） | ☐ |
| 首页有 NewsArticle schema | ☐ |
| 首页有 Organization schema | ☐ |
| 首页有 WebSite schema（含 SearchAction） | ☐ |
| 日报页有 canonical 标签（指向自身绝对 URL） | ☐ |
| 日报页有完整 OG 标签（含 publishedTime） | ☐ |
| 日报页有 NewsArticle schema | ☐ |
| 日报页有 FAQPage schema（AI SEO 核心） | ☐ |
| 日报页有 BreadcrumbList schema | ☐ |
| HTML `lang` 属性为 `zh-CN`（之前是 `zh`） | ☐ |
| 构建无报错 | ☐ |

---

## 部署后行动

1. **Push 代码触发 GitHub Actions 自动部署**：
   ```bash
   git push origin main
   ```

2. **提交 sitemap 到 Google Search Console**：
   打开 https://search.google.com/search-console → Sitemaps → 输入 `https://news.cearl.cc/sitemap.xml`

3. **Rich Results Test 验证**：
   打开 https://search.google.com/test/rich-results → 测试 `https://news.cearl.cc/2026-05-10/`，确认 NewsArticle、FAQPage、BreadcrumbList 出现。

4. **检查 AI 引用**（一周后）：
   在 ChatGPT、Perplexity 搜索"每日科技资讯 AI"，查看是否出现引用。

---

## 注意事项

- **`site/public/` 目录**：Next.js 静态导出时，`public/` 目录的文件会被原样复制到 `out/`。robots.txt 和 llms.txt 放这里即可。
- **sitemap.js 路径**：`app/sitemap.js` 是 Next.js 14 的约定路径，不需要额外配置，构建时自动生成 `/sitemap.xml`。
- **dangerouslySetInnerHTML 安全性**：schema 内容是我们自己生成的结构化 JSON，无用户输入，使用 `dangerouslySetInnerHTML` 是安全的。
- **`NEXT_PUBLIC_BASE_PATH` 环境变量**：已从 page.js 中移除对该变量的依赖（`href="/feed.xml"` 替代），因为该变量值为空字符串，直接写 `/feed.xml` 更清晰。
