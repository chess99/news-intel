---
title: "Synchronous SBOM API deprecated"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-12-synchronous-sbom-api-deprecated
published: 2026-05-13T00:00:53+08:00
lang: en
category: platform
fetched_at: 2026-05-14T00:30:21.498122+08:00
---

# Synchronous SBOM API deprecated

**来源**: GitHub Changelog | **发布**: 2026-05-13 | **链接**: https://github.blog/changelog/2026-05-12-synchronous-sbom-api-deprecated

## RSS 摘要

Following the recent release of the new Asynchronous SBOM REST API, the older, synchronous API is deprecated and slated for removal in six months, on November 13, 2026. If your&#8230; The post Synchronous SBOM API deprecated appeared first on The GitHub Blog .

## 正文

Back to changelog Retired May 12, 2026 • 1 minute read Synchronous SBOM API deprecated Following the recent release of the new Asynchronous SBOM REST API , the older, synchronous API is deprecated and slated for removal in six months, on November 13, 2026. If your scripts or integrations are currently using the REST endpoint at /{owner}/{repo}/dependency-graph/sbom , please update them to use the new /{owner}/{repo}/dependency-graph/sbom/generate-report instead. This request will return a URL which you then poll for completion. Once the SBOM is computed, it will be cached and available for download, providing better performance and reliability than the previous method. Visit the API documentation for more details on the API usage. supply chain security Share Copied Shared Back to changelog
