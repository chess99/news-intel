const SITE_URL = 'https://news.cearl.cc'

export const metadata = {
  title: '搜索',
  description: '搜索 Intel Daily 历史日报',
  alternates: {
    canonical: `${SITE_URL}/search/`,
  },
}

export default function SearchLayout({ children }) {
  return children
}
