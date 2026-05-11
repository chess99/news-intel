import { getAllReports } from '../lib/reports'

const BASE_URL = 'https://news.cearl.cc'

export default function sitemap() {
  const reports = getAllReports()

  const reportEntries = reports.map(report => ({
    url: `${BASE_URL}/${report.date}/`,
    lastModified: new Date(report.date),
    changeFrequency: 'never',
    priority: 0.8,
  }))

  return [
    {
      url: `${BASE_URL}/`,
      lastModified: reports[0] ? new Date(reports[0].date) : new Date(),
      changeFrequency: 'daily',
      priority: 1.0,
    },
    {
      url: `${BASE_URL}/search/`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.5,
    },
    ...reportEntries,
  ]
}
