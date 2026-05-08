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
            const href = `/${r.date}/`
            const isActive =
              pathname === `/news-intel/${r.date}/` ||
              pathname === `/news-intel/${r.date}`
            const parts = r.date.split('-')
            const shortDate = parts.length === 3 ? `${parts[1]}/${parts[2]}` : r.date

            return (
              <li key={r.date} className="archive-item">
                <Link href={href} className={`archive-link${isActive ? ' active' : ''}`}>
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
