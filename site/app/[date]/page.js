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
          <a href={`${process.env.NEXT_PUBLIC_BASE_PATH}/feed.xml`} className="header-search-link" target="_blank" rel="noopener">RSS</a>
        </div>
      </header>

      <Sidebar reports={reports} latestDate={reports[0]?.date} />

      <main className="main-content">
        <ReportBody htmlContent={report.htmlContent} />
      </main>
    </div>
  )
}
