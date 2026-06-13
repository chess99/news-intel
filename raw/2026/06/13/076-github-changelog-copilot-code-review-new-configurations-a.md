---
title: "Copilot code review: New configurations and controls"
source: GitHub Changelog
url: https://github.blog/changelog/2026-06-12-copilot-code-review-new-configurations-and-controls
published: 2026-06-13T05:37:14+08:00
lang: en
category: platform
fetched_at: 2026-06-13T17:49:42.573201+08:00
---

# Copilot code review: New configurations and controls

**来源**: GitHub Changelog | **发布**: 2026-06-13 | **链接**: https://github.blog/changelog/2026-06-12-copilot-code-review-new-configurations-and-controls

## RSS 摘要

With new organization runner controls, Copilot content exclusion support, and the removal of the character limit on repository custom instructions, Copilot code review is now easier to tailor to your&#8230; The post Copilot code review: New configurations and controls appeared first on The GitHub Blog .

## 正文

Back to changelog Improvement June 12, 2026 • 2 minute read Copilot code review: New configurations and controls Table of Contents ⚙️ Organization runner controls 🛡️ Content exclusion support 📝 Custom instructions character limits have been removed Menu. Currently selected: ⚙️ Organization runner controls ⚙️ Organization runner controls 🛡️ Content exclusion support 📝 Custom instructions character limits have been removed With new organization runner controls, Copilot content exclusion support, and the removal of the character limit on repository custom instructions, Copilot code review is now easier to tailor to your needs within your repository and organization. &#9881;&#65039; Organization runner controls With the release of Copilot code review&rsquo;s agentic architecture , we announced that Copilot code review is powered by GitHub Actions. By default, Copilot code review runs on the standard GitHub-hosted runner, but teams can configure self-hosted or large runners for more control over the runner type. To support ease of setup of custom runners, Copilot code review&rsquo;s runner type can now be configured at the organization-level, meaning that one configuration can apply to all repositories within the organization. Organization admins can now: Set Copilot code review&rsquo;s default runner to be automatically used across all repositories, without requiring each repository to be individually configured. Lock the runner setting so the organization default overrides any individual repository configurations. To set this up, navigate to your organization, then go to Copilot -&gt; Runner type -&gt; Runner type configuration . Your configuration will apply to both Copilot code review and Copilot cloud agent if both are enabled. &#128737;&#65039; Content exclusion support Copilot code review now respects repository, organization, and enterprise-level Copilot content exclusion settings, so you can prevent Copilot from utilizing specified files or directories during its review. Repository administrators can configure excluded paths in repository settings using path-based rules. This gives you control over which repository content is available to Copilot code review, helping you align reviews with your team, organization, or enterprise&rsquo;s boundaries, or prevent Copilot from utilizing context that isn&rsquo;t relevant to the review. For more information, check out our docs about configuring content exclusions for Copilot. &#128221; Custom instructions character limits have been removed Previously, Copilot code review would stop reading copilot-instructions.md and *.instructions.md files located under the .github directory once the file reached 4000 characters in size. That limit has now been removed, allowing additional customization and flexibility in your custom instructions. Join the discussion within GitHub Community . Table of Contents ⚙️ Organization runner controls 🛡️ Content exclusion support 📝 Custom instructions character limits have been removed Menu. Currently selected: ⚙️ Organization runner controls ⚙️ Organization runner controls 🛡️ Content exclusion support 📝 Custom instructions character limits have been removed copilot Share Copied Shared Back to changelog
