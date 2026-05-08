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
