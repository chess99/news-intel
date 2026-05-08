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
