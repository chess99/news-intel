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
      type: 'website',
      locale: 'zh_CN',
    },
  }
}

export default async function HomePage() {
  const reports = getAllReports()
  const latest = reports[0]
  const report = latest ? await getReport(latest.date) : null

  // NewsArticle schema points to the stable date page, not the homepage URL
  const newsArticleSchema = report
    ? {
        '@context': 'https://schema.org',
        '@type': 'NewsArticle',
        headline: report.title,
        datePublished: `${latest.date}T09:00:00+08:00`,
        dateModified: `${latest.date}T09:00:00+08:00`,
        url: `${SITE_URL}/${latest.date}/`,
        author: {
          '@type': 'Organization',
          name: 'Intel Daily',
          url: SITE_URL,
        },
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
