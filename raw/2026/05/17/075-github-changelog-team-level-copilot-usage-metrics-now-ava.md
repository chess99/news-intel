---
title: "Team-level Copilot usage metrics now available via API"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-14-team-level-copilot-usage-metrics-now-available-via-api
published: 2026-05-15T07:06:25+08:00
lang: en
category: platform
fetched_at: 2026-05-17T00:30:27.480807+08:00
---

# Team-level Copilot usage metrics now available via API

**来源**: GitHub Changelog | **发布**: 2026-05-15 | **链接**: https://github.blog/changelog/2026-05-14-team-level-copilot-usage-metrics-now-available-via-api

## RSS 摘要

The Copilot usage metrics API now exposes a new user-teams report that maps each Copilot-licensed user to the teams they belong to. By joining the user-teams report with the existing&#8230; The post Team-level Copilot usage metrics now available via API appeared first on The GitHub Blog .

## 正文

Back to changelog Release May 14, 2026 • 2 minute read Team-level Copilot usage metrics now available via API Table of Contents How it works Who can use this feature Key benefits Important notes Menu. Currently selected: How it works How it works Who can use this feature Key benefits Important notes The Copilot usage metrics API now exposes a new user-teams report that maps each Copilot-licensed user to the teams they belong to. By joining the user-teams report with the existing per-user usage report, enterprise administrators and organization owners can produce team-level Copilot usage metrics for any team in their organization or enterprise. This includes elements such as active users, completions, chats, as well as breakdowns by language, IDE, feature, and model. How it works Two new endpoints return signed download URLs to NDJSON reports: GET /enterprises/{enterprise}/copilot/metrics/reports/user-teams-1-day GET /orgs/{org}/copilot/metrics/reports/user-teams-1-day Each row in the user-teams report represents a team membership for a given day, including the team&rsquo;s enterprise or organization id, team slug, and the user&rsquo;s ID and login. To produce team-level metrics, join the user-teams report to the per-user usage report on user_id and day , then aggregate. This release also introduces step-by-step guidance in the docs covering the join, day-level aggregation, and a rolling-window pattern for multi-day reporting. Who can use this feature These metrics are available through the REST API to enterprise administrators, organization owners, billing managers, and people with an enterprise custom role with the View Enterprise Copilot Metrics permission. Key benefits Slice metrics by team : Pivot Copilot adoption, active users, and code generation activity from org/enterprise totals down to any organization or enterprise team without building external team attribution. Identify champions and gaps : See which teams are driving adoption and which need enablement, so you can target campaigns and rollout investments. Full feature coverage : Team-level breakdowns are available across IDE completions, chat, Copilot CLI, code review, and Copilot cloud agent activity. They can be cut by language, IDE, feature, or model. Important notes User-teams reports are available through the REST API only. There is no dashboard surface for team-level metrics in this release. Teams with fewer than five Copilot-seated users are excluded from the user-teams report, though their members&rsquo; individual activity remains visible in the per-user usage report. Users who belong to multiple teams will have their activity counted in each team&rsquo;s aggregate, so team totals cannot be summed to reproduce an organization or enterprise total. For step-by-step guidance, including the join recipe and rolling-window aggregation, see Team-level Copilot usage metrics . Join the discussion within GitHub Community . Table of Contents How it works Who can use this feature Key benefits Important notes Menu. Currently selected: How it works How it works Who can use this feature Key benefits Important notes account management copilot enterprise management tools Share Copied Shared Back to changelog
