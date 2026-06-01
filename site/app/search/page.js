'use client'

import { useEffect, useRef } from 'react'
import Link from 'next/link'

export default function SearchPage() {
  const initialized = useRef(false)

  useEffect(() => {
    if (initialized.current) return
    initialized.current = true

    // Load pagefind-ui.css
    if (!document.querySelector('link[href*="pagefind-ui.css"]')) {
      const cssLink = document.createElement('link')
      cssLink.rel = 'stylesheet'
      cssLink.href = '/pagefind/pagefind-ui.css'
      document.head.appendChild(cssLink)
    }

    // Load pagefind-ui.js as regular script (NOT module) so PagefindUI lands on window
    const script = document.createElement('script')
    script.src = '/pagefind/pagefind-ui.js'
    script.onload = () => {
      // Poll until PagefindUI is available
      let attempts = 0
      const poll = setInterval(() => {
        attempts++
        if (typeof window.PagefindUI !== 'undefined') {
          clearInterval(poll)
          new window.PagefindUI({
            element: '#search-container',
            showImages: false,
            resetStyles: false,
            excerptLength: 35,
          })
        } else if (attempts > 30) {
          clearInterval(poll)
          console.warn('PagefindUI did not load in time')
        }
      }, 100)
    }
    script.onerror = () => console.info('Pagefind not available in this environment')
    document.head.appendChild(script)
  }, [])

  return (
    <div className="site-wrapper">
      <header className="site-header">
        <Link href="/" className="site-logo">Personal Tech Radar</Link>
        <span className="site-header-sep" />
        <span className="site-tagline">Evidence · Events · Claims</span>
        <div className="site-header-right">
          <Link href="/search/" className="header-nav-btn header-nav-btn--active" aria-label="搜索">
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

      <div className="search-page-wrapper">
        <div className="search-page-inner">
          <h1 className="search-page-title">搜索雷达简报</h1>
          <div id="search-container" className="search-container-wrap" />
        </div>
      </div>
    </div>
  )
}
