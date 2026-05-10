---
title: "More flexible secrets and variables for Copilot cloud agent"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-08-more-flexible-secrets-and-variables-for-copilot-cloud-agent
published: 2026-05-08T20:52:23+08:00
lang: en
category: platform
fetched_at: 2026-05-10T00:30:22.858287+08:00
---

# More flexible secrets and variables for Copilot cloud agent

**来源**: GitHub Changelog | **发布**: 2026-05-08 | **链接**: https://github.blog/changelog/2026-05-08-more-flexible-secrets-and-variables-for-copilot-cloud-agent

## RSS 摘要

When you delegate a task to Copilot cloud agent, it works in the background in its own development environment powered by GitHub Actions. You can pass secrets and variables to&#8230; The post More flexible secrets and variables for Copilot cloud agent appeared first on The GitHub Blog .

## 正文

Back to changelog Release May 8, 2026 • 1 minute read More flexible secrets and variables for Copilot cloud agent When you delegate a task to Copilot cloud agent , it works in the background in its own development environment powered by GitHub Actions. You can pass secrets and variables to the agent to give it access to private resources or to configure MCP servers. Until now, these had to be configured one repository at a time, in a copilot environment under the repository&rsquo;s Actions settings. That made it painful to roll out shared configuration (e.g., an internal package registry token or a common MCP server) across many repositories. Today, Copilot cloud agent gets its own dedicated &ldquo;Agents&rdquo; secrets and variables, sitting alongside the existing &ldquo;Actions&rdquo;, &ldquo;Codespaces&rdquo;, and &ldquo;Dependabot&rdquo; types. This means you can: Configure secrets and variables at the organization level for the first time, and share them across any or all repositories in your organization. Manage repository-level secrets and variables in a dedicated &ldquo;Agents&rdquo; section in your repository settings, separate from your Actions configuration. Choose which repositories in an organization can access each secret or variable, just like with Actions. This makes it much easier to configure Copilot cloud agent at scale, without having to duplicate configurations across every repository. To learn more, see &ldquo;Configuring secrets and variables for Copilot cloud agent&rdquo; in the GitHub Docs. copilot Share Copied Shared Back to changelog
