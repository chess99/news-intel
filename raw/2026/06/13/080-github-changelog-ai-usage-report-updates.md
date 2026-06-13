---
title: "AI usage report updates"
source: GitHub Changelog
url: https://github.blog/changelog/2026-06-11-ai-usage-report-updates
published: 2026-06-12T02:27:05+08:00
lang: en
category: platform
fetched_at: 2026-06-13T17:49:42.956526+08:00
---

# AI usage report updates

**来源**: GitHub Changelog | **发布**: 2026-06-12 | **链接**: https://github.blog/changelog/2026-06-11-ai-usage-report-updates

## RSS 摘要

Your AI usage reports now reflect GitHub AI Credits usage in the standard report fields. To monitor AI credit usage going forward, use quantity for AI credit quantity and gross_amount&#8230; The post AI usage report updates appeared first on The GitHub Blog .

## 正文

Back to changelog Improvement June 11, 2026 • 1 minute read AI usage report updates Your AI usage reports now reflect GitHub AI Credits usage in the standard report fields. To monitor AI credit usage going forward, use quantity for AI credit quantity and gross_amount for the dollar amount. These fields now provide the same signal that aic_quantity and aic_gross_amount previously provided during the preview period. We added aic_quantity and aic_gross_amount as a preview before AI credits became the native billing model on June 1. After that change, those preview fields were no longer meaningful for AI credit usage and should have been zeroed. A bug caused those values to persist until a fix was deployed. That fix retroactively zeroed those columns for AI credit usage from June 1 forward. Reports from before June 1 are unchanged, so your historical analysis will continue to work as expected. This fix is already available for GitHub Enterprise Cloud customers. enterprise management tools Share Copied Shared Back to changelog
