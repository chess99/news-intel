---
title: "datasette-llm-limits 0.1a0"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/15/datasette-llm-limits/#atom-everything
published: 2026-05-15T08:42:09+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-17T00:30:23.001728+08:00
---

# datasette-llm-limits 0.1a0

**来源**: Simon Willison Blog | **发布**: 2026-05-15 | **链接**: https://simonwillison.net/2026/May/15/datasette-llm-limits/#atom-everything

## RSS 摘要

Release: datasette-llm-limits 0.1a0 This plugin works in conjunction with datasette-llm and datasette-llm-accountant to let you configure a per-user (or global) spending limit for LLM usage inside of Datasette. Configuration looks something like this: plugins : datasette-llm-limits : limits : per-user-daily : scope : actor window : rolling-24h amount_usd : 1.00 Tags: llm , datasette

## 正文

Release: datasette-llm-limits 0.1a0 Simon Willison’s Weblog Subscribe Sponsored by: Datadog &mdash; Ship reliable AI faster with LLM Observability. Read the best practices guide 15th May 2026 Release datasette-llm-limits 0.1a0 &mdash; Plugin for configuring periodic limits on LLM usage in Datasette This plugin works in conjunction with datasette-llm and datasette-llm-accountant to let you configure a per-user (or global) spending limit for LLM usage inside of Datasette. Configuration looks something like this: plugins : datasette-llm-limits : limits : per-user-daily : scope : actor window : rolling-24h amount_usd : 1.00 Posted 15th May 2026 at 12:42 am Recent articles Notes on the xAI/Anthropic data center deal - 7th May 2026 Live blog: Code w/ Claude 2026 - 6th May 2026 Vibe coding and agentic engineering are getting closer than I&#x27;d like - 6th May 2026 This is a beat by Simon Willison, posted on 15th May 2026 . datasette 1485 llm 600 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
