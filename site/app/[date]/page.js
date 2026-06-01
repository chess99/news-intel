import { getAllBriefs, getBrief } from '../../lib/briefs'
import Sidebar from '../../components/Sidebar'
import BriefBody from '../../components/BriefBody'
import Link from 'next/link'
import { notFound } from 'next/navigation'

const SITE_URL = 'https://news.cearl.cc'

export const dynamicParams = false
export const dynamic = 'force-static'

export async function generateStaticParams() {
  const briefs = getAllBriefs()
  return briefs.length ? briefs.map(brief => ({ date: brief.date })) : [{ date: '_empty' }]
}

export async function generateMetadata({ params }) {
  if (params.date === '_empty') return { title: 'No Briefs Yet' }
  const brief = await getBrief(params.date)
  if (!brief) return { title: 'Not Found' }

  const meta = getAllBriefs().find(item => item.date === params.date)
  const excerpt = meta?.excerpt || 'Evidence-first personal technology intelligence radar.'

  return {
    title: brief.title,
    description: excerpt,
    alternates: {
      canonical: `${SITE_URL}/${params.date}/`,
    },
    openGraph: {
      title: `${brief.title} — Personal Tech Radar`,
      description: excerpt,
      url: `${SITE_URL}/${params.date}/`,
      type: 'article',
      publishedTime: `${params.date}T09:00:00+08:00`,
      locale: 'zh_CN',
    },
  }
}

export default async function DatePage({ params }) {
  const briefs = getAllBriefs()
  const brief = await getBrief(params.date)
  if (!brief && params.date === '_empty') {
    return (
      <div className="site-wrapper">
        <header className="site-header">
          <Link href="/" className="site-logo">Personal Tech Radar</Link>
          <span className="site-header-sep" />
          <span className="site-tagline">Evidence · Events · Claims</span>
        </header>
        <Sidebar briefs={briefs} latestDate={briefs[0]?.date} />
        <main className="main-content">
          <div style={{ padding: '4rem', fontFamily: 'var(--mono)', color: 'var(--text-muted)', fontSize: '12px', letterSpacing: '0.1em' }}>
            暂无雷达简报
          </div>
        </main>
      </div>
    )
  }
  if (!brief) notFound()

  const meta = briefs.find(item => item.date === params.date)
  const excerpt = meta?.excerpt || ''

  const newsArticleSchema = {
    '@context': 'https://schema.org',
    '@type': 'NewsArticle',
    headline: brief.title,
    datePublished: `${params.date}T09:00:00+08:00`,
    dateModified: `${params.date}T09:00:00+08:00`,
    url: `${SITE_URL}/${params.date}/`,
    author: {
      '@type': 'Organization',
      name: 'Personal Tech Radar',
      url: SITE_URL,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Personal Tech Radar',
      url: SITE_URL,
    },
    inLanguage: 'zh-CN',
    description: excerpt,
  }

  return (
    <div className="site-wrapper">
      <header className="site-header">
        <Link href="/" className="site-logo">Personal Tech Radar</Link>
        <span className="site-header-sep" />
        <span className="site-tagline">Evidence · Events · Claims</span>
        <div className="site-header-right">
          <Link href="/search/" className="header-nav-btn" aria-label="搜索">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <span>搜索</span>
          </Link>
          <Link href="/topics/" className="header-nav-btn" aria-label="主题">
            <span>主题</span>
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

      <Sidebar briefs={briefs} latestDate={briefs[0]?.date} />

      <main className="main-content">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(newsArticleSchema) }}
        />
        <BriefBody htmlContent={brief.htmlContent} />
      </main>
    </div>
  )
}
