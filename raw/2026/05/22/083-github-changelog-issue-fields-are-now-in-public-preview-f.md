---
title: "Issue fields are now in public preview for all organizations"
source: GitHub Changelog
url: https://github.blog/changelog/2026-05-21-issue-fields-are-now-in-public-preview-for-all-organizations
published: 2026-05-21T22:30:03+08:00
lang: en
category: platform
fetched_at: 2026-05-22T00:30:33.092009+08:00
---

# Issue fields are now in public preview for all organizations

**来源**: GitHub Changelog | **发布**: 2026-05-21 | **链接**: https://github.blog/changelog/2026-05-21-issue-fields-are-now-in-public-preview-for-all-organizations

## RSS 摘要

Issue fields are now available in public preview to all GitHub organizations on github.com and GitHub Enterprise Cloud with data residency. When you define typed metadata like Priority, Effort, or&#8230; The post Issue fields are now in public preview for all organizations appeared first on The GitHub Blog .

## 正文

Back to changelog Release May 21, 2026 • 2 minute read Issue fields are now in public preview for all organizations Issue fields are now available in public preview to all GitHub organizations on github.com and GitHub Enterprise Cloud with data residency. When you define typed metadata like Priority , Effort , or any custom field at the org level, and it automatically shows up on every issue, in every repository. Fields support four types (i.e., single select, text, number, and date), can be pinned to specific issue types, and work across the platform. You can search and filter issues by field value, add fields as columns in project views, track changes in the timeline, and automate via REST and GraphQL APIs or webhook events. Since the initial preview in March , over 1,000 organizations have adopted issue fields, including some of the largest enterprises and open source projects on GitHub. Teams are building fields into their creation workflows and using bots, GitHub Actions, and integrations to keep field values consistent without manual effort. The most common themes from early adopters include: Replacing sprawling label systems with structured, queryable metadata unifying priority and effort tracking across hundreds of repositories without manual syncing. Giving automation a consistent schema to build on. Teams describe it as the missing link between issues and projects. Based on that usage, we shipped several improvements and will continue iterating based on feedback: Public repository visibility controls : Orgs can decide which fields are visible to nonmembers. REST API parity : Set field values when creating issues via the REST API, matching existing GraphQL support. Migration tool : A Copilot skill that bulk copies values from labels or project fields. Every organization automatically gets four default fields that work out of the box. Organization admins can customize fields, add new ones, and configure which fields appear on each issue type from Settings &gt; Planning &gt; Issue fields . To learn more, see the issue fields documentation . Share feedback in the community discussion &mdash;it directly shapes what we build next. projects &amp; issues Share Copied Shared Back to changelog
