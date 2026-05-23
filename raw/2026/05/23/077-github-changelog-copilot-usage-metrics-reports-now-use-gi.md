---
title: "Copilot usage metrics reports now use GitHub-owned download URLs"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-20-copilot-usage-metrics-reports-now-use-github-owned-download-urls
published: 2026-05-21T07:58:35+08:00
lang: en
category: platform
fetched_at: 2026-05-23T00:30:27.784483+08:00
---

# Copilot usage metrics reports now use GitHub-owned download URLs

**来源**: GitHub Changelog | **发布**: 2026-05-21 | **链接**: https://github.blog/changelog/2026-05-20-copilot-usage-metrics-reports-now-use-github-owned-download-urls

## RSS 摘要

As previously announced, the download URLs for Copilot usage metrics reports have migrated from Azure Front Door domains to a stable, GitHub-owned custom domain. This change improves URL stability and&#8230; The post Copilot usage metrics reports now use GitHub-owned download URLs appeared first on The GitHub Blog .

## 正文

Back to changelog Improvement May 20, 2026 • 2 minute read Copilot usage metrics reports now use GitHub-owned download URLs Table of Contents What's changed What you need to do Why we made this change Menu. Currently selected: What's changed What's changed What you need to do Why we made this change As previously announced , the download URLs for Copilot usage metrics reports have migrated from Azure Front Door domains to a stable, GitHub-owned custom domain. This change improves URL stability and makes firewall and proxy allowlist management easier for enterprise customers. What&rsquo;s changed Starting today, Copilot usage metrics report download links, which are returned by the Copilot Usage Metrics API , use the new domain copilot-reports.github.com instead of the previous copilot-reports-*.b01.azurefd.net pattern. github.com (GHEC) customers: Previous New Report download URL pattern https://copilot-reports-*.b01.azurefd.net/... https://copilot-reports.github.com/... ghe.com customers: Previous New Report download URL pattern https://copilot-reports-*.b01.azurefd.net/... https://copilot-reports.*.ghe.com/... What you need to do If your organization uses a firewall or proxy allowlist, add the following domain: github.com: https://copilot-reports.github.com ghe.com: https://copilot-reports.SUBDOMAIN.ghe.com , where SUBDOMAIN is your enterprise&rsquo;s dedicated subdomain on GHE.com The legacy copilot-reports-*.b01.azurefd.net pattern will continue to work during a transition period, but will eventually be deprecated. We recommend updating your allowlists as soon as possible. Note: In rare cases where Azure Front Door is unavailable, report downloads may fall back to direct Azure Blob Storage URLs ( *.blob.core.windows.net ). If your organization requires uninterrupted access to reports during such events, you should also ensure *.blob.core.windows.net is in your allowlist. Why we made this change The previous Azure Front Door domains were infrastructure-specific and could change when services were redeployed or reconfigured. Moving to a stable, GitHub-owned domain ensures that: Report download URLs remain constant regardless of infrastructure changes. Enterprise security teams have a predictable, trustworthy domain to allowlist. Automation scripts and integrations are not disrupted by domain changes. For more information, see the Copilot allowlist reference . Join the discussion within GitHub Community . Table of Contents What's changed What you need to do Why we made this change Menu. Currently selected: What's changed What's changed What you need to do Why we made this change account management copilot Share Copied Shared Back to changelog
