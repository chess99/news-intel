---
title: "Removal of code_scanning_upload field from rate_limit API endpoint"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-19-removal-of-code_scanning_upload-field-from-rate_limit-api-endpoint
published: 2026-05-19T18:40:26+08:00
lang: en
category: platform
fetched_at: 2026-05-20T00:30:20.241360+08:00
---

# Removal of code_scanning_upload field from rate_limit API endpoint

**来源**: GitHub Changelog | **发布**: 2026-05-19 | **链接**: https://github.blog/changelog/2026-05-19-removal-of-code_scanning_upload-field-from-rate_limit-api-endpoint

## RSS 摘要

As of May 19, 2026, we have removed the code_scanning_upload field from the rate limit REST API endpoint response. What changed The code_scanning_upload field no longer appears in the resources&#8230; The post Removal of code_scanning_upload field from rate_limit API endpoint appeared first on The GitHub Blog .

## 正文

Back to changelog Retired May 19, 2026 • 1 minute read Removal of code_scanning_upload field from rate_limit API endpoint Table of Contents What changed If your integrations are affected Menu. Currently selected: What changed What changed If your integrations are affected As of May 19, 2026 , we have removed the code_scanning_upload field from the rate limit REST API endpoint response. What changed The code_scanning_upload field no longer appears in the resources object of the rate_limit API response. This field was removed because it displayed a separate rate limit category that was actually joined with the core limit pool, causing confusion about actual rate limit status. Rate limits for code scanning uploads continue to be governed by the standard core rate limit. If your integrations are affected If you have scripts or tools that parse the /rate_limit endpoint and reference code_scanning_upload , update them to remove that reference. No alternative field replacement is needed&mdash;use the core rate limit values instead. For more information, see Rate limits for the REST API . Table of Contents What changed If your integrations are affected Menu. Currently selected: What changed What changed If your integrations are affected application security Share Copied Shared Back to changelog
