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
      publishedTime: `${params.date}T09:00:00+08:00`,
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
    datePublished: `${params.date}T09:00:00+08:00`,
    dateModified: `${params.date}T09:00:00+08:00`,
    url: `${SITE_URL}/${params.date}/`,
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
          text: `Intel Daily ${params.date} 日报从 30+ 中文科技媒体中精选当日重点资讯，经 AI 评分筛选后按"本日焦点"、"AI & 大模型"、"科技创业"、"产品 & 硬件"等分类整理，附带批判性分析和信源评级。完整内容见 ${SITE_URL}/${params.date}/`,
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
