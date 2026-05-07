---
title: "Secret scanning with GitHub MCP Server is now generally available"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-05-secret-scanning-with-github-mcp-server-is-now-generally-available
published: 2026-05-06T06:04:32+08:00
lang: en
category: platform
fetched_at: 2026-05-07T00:30:29.312420+08:00
---

# Secret scanning with GitHub MCP Server is now generally available

**来源**: GitHub Changelog | **发布**: 2026-05-06 | **链接**: https://github.blog/changelog/2026-05-05-secret-scanning-with-github-mcp-server-is-now-generally-available

## RSS 摘要

GitHub secret scanning in the GitHub MCP (Model Context Protocol) server is now generally available. When you use an MCP-compatible AI coding agent or IDE (like GitHub Copilot CLI or&#8230; The post Secret scanning with GitHub MCP Server is now generally available appeared first on The GitHub Blog .

## 正文

Back to changelog Release May 5, 2026 • 1 minute read Secret scanning with GitHub MCP Server is now generally available Table of Contents What's new Get started Learn more Menu. Currently selected: What's new What's new Get started Learn more GitHub secret scanning in the GitHub MCP (Model Context Protocol) server is now generally available. When you use an MCP-compatible AI coding agent or IDE (like GitHub Copilot CLI or Visual Studio Code), you can scan your code for exposed secrets before you commit or open a pull request, so leaked credentials don&rsquo;t make it into your repository in the first place. It&rsquo;s been in public preview since March 2026 , and it&rsquo;s available for repositories with GitHub Secret Protection enabled. What&rsquo;s new Secret scanning tools in the MCP server now honor your existing push protection customization , so detections and bypass behavior stay consistent with what you&rsquo;ve already set up at the repository or organization level. Get started Set up the GitHub MCP server in your developer environment. (Optional) Install the GitHub Advanced Security plugin for a more tailored secret scanning experience. In GitHub Copilot CLI, run /plugin install advanced-security@copilot-plugins . In Visual Studio Code, install the advanced-security agent plugin, then use /secret-scanning in Copilot Chat to start your prompt. Ask your agent to scan your current changes for exposed secrets before you commit. For example: &gt; Scan my current changes for exposed secrets and show me the files and lines I should update before I commit. For the full set of setup options and configurations, see documentation for GitHub MCP server secret scanning setup options and configurations . Learn more Learn more about GitHub secret scanning and how to set up the GitHub MCP server . Join the discussion in the GitHub Community . Table of Contents What's new Get started Learn more Menu. Currently selected: What's new What's new Get started Learn more application security Share Copied Shared Back to changelog
