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
          <ReportBody htmlContent={report.htmlContent} />
        ) : (
          <div style={{ padding: '4rem', fontFamily: 'var(--mono)', color: 'var(--text-dim)', fontSize: '11px', letterSpacing: '0.1em' }}>
            暂无日报数据
          </div>
        )}
      </main>
    </div>
  )
}
