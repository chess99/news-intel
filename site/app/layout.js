import './globals.css'

export const metadata = {
  title: 'Intel Daily — 科技资讯日报',
  description: '每日 AI 与科技深度资讯，批判性分析',
}

export default function RootLayout({ children }) {
  return (
    <html lang="zh">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="alternate"
          type="application/rss+xml"
          title="Intel Daily RSS"
          href="/news-intel/feed.xml"
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
