---
title: "Dependency scanning with GitHub MCP Server is in public preview"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-05-dependency-scanning-with-github-mcp-server-is-in-public-preview
published: 2026-05-06T04:45:38+08:00
lang: en
category: platform
fetched_at: 2026-05-07T00:30:30.326231+08:00
---

# Dependency scanning with GitHub MCP Server is in public preview

**来源**: GitHub Changelog | **发布**: 2026-05-06 | **链接**: https://github.blog/changelog/2026-05-05-dependency-scanning-with-github-mcp-server-is-in-public-preview

## RSS 摘要

The GitHub MCP Server can now scan your code changes for vulnerable dependencies before you commit or open a pull request. You&#8217;ll catch known vulnerabilities while you write code with&#8230; The post Dependency scanning with GitHub MCP Server is in public preview appeared first on The GitHub Blog .

## 正文

Back to changelog Release May 5, 2026 • 2 minute read Dependency scanning with GitHub MCP Server is in public preview Table of Contents How it works Get started Learn more Menu. Currently selected: How it works How it works Get started Learn more The GitHub MCP Server can now scan your code changes for vulnerable dependencies before you commit or open a pull request. You&rsquo;ll catch known vulnerabilities while you write code with MCP-compatible IDEs and AI coding agents. It&rsquo;s now in public preview for repositories with Dependabot alerts enabled. How it works The dependency vulnerability scanning tools ship as part of the GitHub MCP Server&rsquo;s dependabot toolset. Once enabled, your AI coding agent can run dependency vulnerability scanning based on your prompts. When you ask the agent to check for vulnerable dependencies, it invokes the toolset, sends dependency information to the GitHub Advisory Database, and returns structured results with affected packages, severity, and recommended fixed versions. For more thorough post-commit checks, the toolset can also run the Dependabot CLI locally to diff dependency graphs before and after your changes. Get started Set up the GitHub MCP Server in your developer environment and enable the dependabot toolset: In GitHub Copilot CLI, the GitHub MCP Server is preinstalled. Run copilot --add-github-mcp-toolset dependabot to enable the dependabot toolset for your session. In Visual Studio Code, add "X-MCP-Toolsets": "dependabot" to your GitHub MCP Server headers, or pick Dependabot from the toolset selector in Copilot Chat. Install the advanced-security plugin for GitHub Copilot for a more tailored dependency vulnerability scanning experience. For example: In GitHub Copilot CLI , run /plugin install advanced-security@copilot-plugins . In Visual Studio Code, install the advanced-security agent plugin , then use /dependency-scanning in Copilot Chat to start your prompt. Ask your agent to scan your current changes for vulnerable dependencies before you commit. Here&rsquo;s an example prompt you can use: Scan the dependencies I added on this branch for known vulnerabilities and tell me which versions to upgrade to before I commit. Learn more Dependabot . GitHub Advisory Database . GitHub MCP Server . Join the discussion within GitHub Community . Table of Contents How it works Get started Learn more Menu. Currently selected: How it works How it works Get started Learn more supply chain security Share Copied Shared Back to changelog
