---
title: "datasette 1.0a29"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/12/datasette/#atom-everything
published: 2026-05-13T07:41:06+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-14T00:30:19.002786+08:00
---

# datasette 1.0a29

**来源**: Simon Willison Blog | **发布**: 2026-05-13 | **链接**: https://simonwillison.net/2026/May/12/datasette/#atom-everything

## RSS 摘要

Release: datasette 1.0a29 New TokenRestrictions.abbreviated(datasette) utility method for creating "_r" dictionaries. #2695 Table headers and column options are now visible even if a table contains zero rows. #2701 Fixed bug with display of column actions dialog on Mobile Safari. #2708 Fixed bug where tests could crash with a segfault due to a race condition between Datasette.close() and Database.close() . #2709 That segfault bug was gnarly . I added a mechanism to Datasette recently that would 

## 正文

Release: datasette 1.0a29 Simon Willison’s Weblog Subscribe Sponsored by: WorkOS &mdash; Make your app Enterprise Ready with SSO, SCIM, RBAC, and more. 12th May 2026 Release datasette 1.0a29 &mdash; An open source multi-tool for exploring and publishing data New TokenRestrictions.abbreviated(datasette) utility method for creating "_r" dictionaries. #2695 Table headers and column options are now visible even if a table contains zero rows. #2701 Fixed bug with display of column actions dialog on Mobile Safari. #2708 Fixed bug where tests could crash with a segfault due to a race condition between Datasette.close() and Database.close() . #2709 That segfault bug was gnarly . I added a mechanism to Datasette recently that would automatically close connections at the end of each test, but it turned out that introduced a race condition where an in-flight query could sometimes be executing in a thread against a connection while it was being closed. I ended up solving that by having Codex CLI (with GPT-5.5 xhigh) create a minimal Dockerfile that recreated the bug. Posted 12th May 2026 at 11:41 pm Recent articles Notes on the xAI/Anthropic data center deal - 7th May 2026 Live blog: Code w/ Claude 2026 - 6th May 2026 Vibe coding and agentic engineering are getting closer than I&#x27;d like - 6th May 2026 This is a beat by Simon Willison, posted on 12th May 2026 . projects 528 datasette 1481 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
