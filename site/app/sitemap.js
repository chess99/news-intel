import { getAllBriefs } from '../lib/briefs'

const BASE_URL = 'https://news.cearl.cc'

export default function sitemap() {
  const briefs = getAllBriefs()

  const briefEntries = briefs.map(brief => ({
    url: `${BASE_URL}/${brief.date}/`,
    lastModified: new Date(brief.date),
    changeFrequency: 'never',
    priority: 0.8,
  }))

  return [
    {
      url: `${BASE_URL}/`,
      lastModified: briefs[0] ? new Date(briefs[0].date) : new Date(),
      changeFrequency: 'daily',
      priority: 1.0,
    },
    {
      url: `${BASE_URL}/search/`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.5,
    },
    ...briefEntries,
  ]
}
