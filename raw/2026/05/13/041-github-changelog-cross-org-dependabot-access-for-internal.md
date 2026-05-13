---
title: "Cross-org Dependabot access for internal repositories"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-11-cross-org-dependabot-access-for-internal-repositories
published: 2026-05-11T21:52:50+08:00
lang: en
category: platform
fetched_at: 2026-05-13T00:30:12.486371+08:00
---

# Cross-org Dependabot access for internal repositories

**来源**: GitHub Changelog | **发布**: 2026-05-11 | **链接**: https://github.blog/changelog/2026-05-11-cross-org-dependabot-access-for-internal-repositories

## RSS 摘要

Dependabot can now access internal repositories hosted in other organizations within your enterprise. Consider the situation where you have a dependency hosted in an internal GitHub repository. This repository is&#8230; The post Cross-org Dependabot access for internal repositories appeared first on The GitHub Blog .

## 正文

Back to changelog Improvement May 11, 2026 • 1 minute read Cross-org Dependabot access for internal repositories Dependabot can now access internal repositories hosted in other organizations within your enterprise. Consider the situation where you have a dependency hosted in an internal GitHub repository. This repository is in the same enterprise as the project that uses the dependency, but it&rsquo;s in a different organization. In this situation, you can now grant Dependabot the ability to access all internal repositories, and you can do this from your enterprise&rsquo;s Advanced Security Policies page. Previously, Dependabot could only access repositories within the same organization, which meant cross-organization dependencies in internal repositories couldn&rsquo;t receive automatic updates. With this change, enterprise and organization administrators can grant Dependabot access to all internal repositories across their enterprise, so Dependabot can open pull requests for dependencies regardless of which organization hosts them. Get started For internal and public repositories : Enable Dependabot access permanently at the enterprise level. Once enabled, all current and future internal repositories will automatically have Dependabot access. This improvement is available today on github.com and will come to enterprise server in GHES 3.22. To enable Dependabot for all internal repositories in your organization: Navigate to your enterprise&rsquo;s &ldquo;Policies&rdquo; page. Select Advanced Security from the left-side pane. Scroll to the end of the page to the &ldquo;Grant Dependabot access to repositories&rdquo; section. Select the policy for repositories you&rsquo;d like to use for updates with Dependabot. Learn more Public, private, and internal repository types Managing Dependabot in your enterprise About Dependabot security updates Have feedback about this feature? We&rsquo;d love to hear from you in GitHub Community Discussions . supply chain security Share Copied Shared Back to changelog
