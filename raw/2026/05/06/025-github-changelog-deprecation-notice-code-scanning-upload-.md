---
title: "Deprecation notice: code_scanning_upload field will be removed from rate_limit API endpoint"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-05-deprecation-notice-code_scanning_upload-field-will-be-removed-from-rate_limit-api-endpoint
published: 2026-05-05T21:14:30+08:00
lang: en
category: platform
fetched_at: 2026-05-06T00:30:14.677840+08:00
---

# Deprecation notice: code_scanning_upload field will be removed from rate_limit API endpoint

**来源**: GitHub Changelog | **发布**: 2026-05-05 | **链接**: https://github.blog/changelog/2026-05-05-deprecation-notice-code_scanning_upload-field-will-be-removed-from-rate_limit-api-endpoint

## RSS 摘要

On May 19, 2026, we&#8217;ll remove the code_scanning_upload field from the rate_limit REST API endpoint response. Why did we make this change? The code_scanning_upload field in the rate_limit response has&#8230; The post Deprecation notice: code_scanning_upload field will be removed from rate_limit API endpoint appeared first on The GitHub Blog .

## 正文

Back to changelog Retired May 5, 2026 • 1 minute read Deprecation notice: code_scanning_upload field will be removed from rate_limit API endpoint Table of Contents Why did we make this change? What you need to do Menu. Currently selected: Why did we make this change? Why did we make this change? What you need to do On May 19, 2026 , we&rsquo;ll remove the code_scanning_upload field from the rate_limit REST API endpoint response. Why did we make this change? The code_scanning_upload field in the rate_limit response has been a source of confusion. While it appeared as a separate rate limit category, it shares the same limit pool as core . This led customers to incorrectly interpret their rate limit status. What you need to do If your code or scripts parse the /rate_limit endpoint and reference the code_scanning_upload field, update them before May 19, 2026 to avoid failures. Before: { "resources": { "core": { "limit": 5000, "used": 1, "remaining": 4999, "reset": 1372700873 }, "code_scanning_upload": { "limit": 5000, "used": 1, "remaining": 4999, "reset": 1372700873 } } } After May 19, 2026: { "resources": { "core": { "limit": 5000, "used": 1, "remaining": 4999, "reset": 1372700873 } } } The standard core rate limit continues to govern GitHub code scanning uploads. No replacement field is needed. For more information about rate limits, see Rate limits for the REST API . Table of Contents Why did we make this change? What you need to do Menu. Currently selected: Why did we make this change? Why did we make this change? What you need to do application security Share Copied Shared Back to changelog
