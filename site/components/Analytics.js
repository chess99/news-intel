'use client'

import { useEffect } from 'react'
import { analyticsConfig } from '@/lib/analytics-config'

export default function Analytics() {
  useEffect(() => {
    const { baidu, google } = analyticsConfig

    if (baidu?.enabled && baidu.siteId) {
      window._hmt = window._hmt || []
      const hm = document.createElement('script')
      hm.src = `https://hm.baidu.com/hm.js?${baidu.siteId}`
      hm.async = true
      const s = document.getElementsByTagName('script')[0]
      s.parentNode.insertBefore(hm, s)
    }

    if (google?.enabled && google.measurementId) {
      const ga = document.createElement('script')
      ga.src = `https://www.googletagmanager.com/gtag/js?id=${google.measurementId}`
      ga.async = true
      document.head.appendChild(ga)

      window.dataLayer = window.dataLayer || []
      function gtag() { window.dataLayer.push(arguments) }
      window.gtag = gtag
      gtag('js', new Date())
      gtag('config', google.measurementId)
    }
  }, [])

  return null
}
