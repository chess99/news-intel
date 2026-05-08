---
title: "Repository rulesets: User bypass and branch renaming"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-07-repository-rulesets-user-bypass-and-branch-renaming
published: 2026-05-07T22:13:48+08:00
lang: en
category: platform
fetched_at: 2026-05-08T00:30:23.347316+08:00
---

# Repository rulesets: User bypass and branch renaming

**来源**: GitHub Changelog | **发布**: 2026-05-07 | **链接**: https://github.blog/changelog/2026-05-07-repository-rulesets-user-bypass-and-branch-renaming

## RSS 摘要

GitHub repository rulesets now support two frequently requested features: adding individual users as bypass actors and renaming branches covered by organization rulesets. Add individual users as bypass actors You can&#8230; The post Repository rulesets: User bypass and branch renaming appeared first on The GitHub Blog .

## 正文

Back to changelog Improvement May 7, 2026 • 1 minute read Repository rulesets: User bypass and branch renaming Table of Contents Add individual users as bypass actors Rename branches covered by rulesets Menu. Currently selected: Add individual users as bypass actors Add individual users as bypass actors Rename branches covered by rulesets GitHub repository rulesets now support two frequently requested features: adding individual users as bypass actors and renaming branches covered by organization rulesets. Add individual users as bypass actors You can now add individual users as bypass actors on repository-level rulesets through the UI, REST API, and GraphQL. If you&rsquo;ve been creating dedicated teams or roles just to grant bypass access for a single person or service account, you can now skip that step and add accounts directly. Rename branches covered by rulesets Repository administrators can now rename a branch that&rsquo;s covered by an organization or enterprise ruleset, as long as the new branch name remains within the scope of every ruleset that applied to the original name. This removes the need to involve an organization or enterprise administrator for routine renames (e.g., migrating from master to main ) when the rename doesn&rsquo;t change which rules apply. Enterprise-level setting: Organization-level setting: The rename is allowed only when every organization-level and enterprise-level rule that applied to the original branch also applies to the new branch name. If the new name would fall outside the scope of any applicable ruleset, the rename is blocked and an administrator at that level must perform it. Organization and enterprise administrators can disable this capability in their settings. To learn more, see the rulesets documentation . Table of Contents Add individual users as bypass actors Rename branches covered by rulesets Menu. Currently selected: Add individual users as bypass actors Add individual users as bypass actors Rename branches covered by rulesets platform governance Share Copied Shared Back to changelog
