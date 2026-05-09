---
title: "Enterprise Live Migrations is now in public preview"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-07-enterprise-live-migrations-is-now-in-public-preview
published: 2026-05-08T04:28:33+08:00
lang: en
category: platform
fetched_at: 2026-05-09T00:30:25.038265+08:00
---

# Enterprise Live Migrations is now in public preview

**来源**: GitHub Changelog | **发布**: 2026-05-08 | **链接**: https://github.blog/changelog/2026-05-07-enterprise-live-migrations-is-now-in-public-preview

## RSS 摘要

Enterprise Live Migrations (ELM) is now available in public preview. ELM gives enterprise administrators a new way to migrate repositories from GitHub Enterprise Server (GHES) to GitHub Enterprise Cloud with&#8230; The post Enterprise Live Migrations is now in public preview appeared first on The GitHub Blog .

## 正文

Back to changelog Release May 7, 2026 • 1 minute read Enterprise Live Migrations is now in public preview Enterprise Live Migrations (ELM) is now available in public preview. ELM gives enterprise administrators a new way to migrate repositories from GitHub Enterprise Server (GHES) to GitHub Enterprise Cloud with data residency, without the extended code freezes and business disruption that come with traditional migrations. Key features of ELM to consider when selecting a tool for your next repository migration are: Cutover in minutes, not days: ELM continuously syncs data from source to target, so developers keep working in their repositories throughout the migration. When you&rsquo;re ready, the cutover only requires the time to drain remaining in-flight changes. This is especially valuable for business-critical repositories contributed to by geographically dispersed teams where there is no convenient downtime window to fit a migration into. Built for the largest monorepos: ELM was purpose-built to handle the repositories that push existing tooling to its limits (i.e., massive monorepos with deep git history, large volumes of issues and pull requests, and constant activity around the clock). Resource-level progress tracking surfaces failures before cutover, so you can make an informed decision about when to proceed. Use ELM alongside GitHub Enterprise Importer: ELM complements GEI, giving you flexibility to choose the right tool for each repository based on its size, shape, and activity. Use GEI for straightforward migrations where brief downtime is acceptable, and ELM for the repositories that need a zero-disruption approach. Run them concurrently as part of the same migration strategy. ELM runs as a service on your GHES appliance, driven by the elm CLI. ELM is delivered as part of GHES versions 3.17.14+, 3.18.8+, 3.19.5+, and 3.20.2+. This release ships with the most recent GHES patch releases. To get started, check out the Enterprise Live Migrations documentation . Have feedback or questions? Join our community discussion . enterprise management tools Share Copied Shared Back to changelog
