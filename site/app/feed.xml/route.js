import { getAllBriefs } from '../../lib/briefs'

export const dynamic = 'force-static'

const SITE_URL = 'https://news.cearl.cc'
const BASE_PATH = ''

export async function GET() {
  const briefs = getAllBriefs().slice(0, 20)

  const items = briefs.map(r => `
    <item>
      <title><![CDATA[${r.title}]]></title>
      <link>${SITE_URL}${BASE_PATH}/${r.date}/</link>
      <guid isPermaLink="true">${SITE_URL}${BASE_PATH}/${r.date}/</guid>
      <pubDate>${new Date(r.date).toUTCString()}</pubDate>
      <description><![CDATA[${r.excerpt}]]></description>
    </item>`).join('\n')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Personal Tech Radar</title>
    <link>${SITE_URL}${BASE_PATH}/</link>
    <description>Evidence-first personal technology intelligence briefs</description>
    <language>zh-CN</language>
    <atom:link href="${SITE_URL}${BASE_PATH}/feed.xml" rel="self" type="application/rss+xml"/>
    ${items}
  </channel>
</rss>`

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  })
}
