'use client'

import { useEffect } from 'react'
import Link from 'next/link'

export default function SearchPage() {
  useEffect(() => {
    async function loadPagefind() {
      if (typeof window === 'undefined') return
      try {
        const pagefind = await import('/news-intel/pagefind/pagefind.js')
        await pagefind.init()
        const { PagefindUI } = await import('/news-intel/pagefind/pagefind-ui.js')
        new PagefindUI({
          element: '#search-container',
          showImages: false,
          resetStyles: false,
        })
      } catch {
        console.info('Pagefind not available in dev mode')
      }
    }
    loadPagefind()
  }, [])

  return (
    <div className="site-wrapper">
      <header className="site-header">
        <Link href="/" className="site-logo">Intel Daily</Link>
        <span className="site-header-sep" />
        <span className="site-tagline">科技资讯 · 批判性分析 · 每日更新</span>
        <div className="site-header-right">
          <Link href="/search/" className="header-search-link" style={{ color: 'var(--accent)' }}>搜索</Link>
          <a href="/news-intel/feed.xml" className="header-search-link" target="_blank" rel="noopener">RSS</a>
        </div>
      </header>

      <div style={{ gridColumn: '1 / -1', padding: '3rem 3rem 4rem', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        <h1 style={{ fontFamily: 'var(--serif)', fontSize: '1.5rem', marginBottom: '2rem', color: 'var(--text)' }}>
          搜索日报
        </h1>
        <link rel="stylesheet" href="/news-intel/pagefind/pagefind-ui.css" />
        <div id="search-container" />
        <p style={{ marginTop: '2rem', fontSize: '12px', color: 'var(--text-dim)', fontFamily: 'var(--mono)' }}>
          搜索功能在构建后可用。开发模式下请先运行 <code>npm run build</code>。
        </p>
      </div>
    </div>
  )
}
