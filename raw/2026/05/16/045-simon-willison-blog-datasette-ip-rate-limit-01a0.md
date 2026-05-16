---
title: "datasette-ip-rate-limit 0.1a0"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/14/datasette-ip-rate-limit/#atom-everything
published: 2026-05-14T12:10:23+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-16T00:30:18.723708+08:00
---

# datasette-ip-rate-limit 0.1a0

**来源**: Simon Willison Blog | **发布**: 2026-05-14 | **链接**: https://simonwillison.net/2026/May/14/datasette-ip-rate-limit/#atom-everything

## RSS 摘要

Release: datasette-ip-rate-limit 0.1a0 The datasette.io site was being hammered by poorly-behaved crawlers, so I had Codex (GPT-5.5 xhigh) build a configurable rate limiting plugin to block IPs that were hammering specific areas of the site too quickly. Here's the production configuration I'm using on that site for the new plugin: datasette-ip-rate-limit : header : Fly-Client-IP max_keys : 10000 exempt_paths : - " /static/* " - " /-/turnstile* " rules : - name : demo-databases paths : - " /globa

## 正文

Release: datasette-ip-rate-limit 0.1a0 Simon Willison’s Weblog Subscribe Sponsored by: Datadog &mdash; Ship reliable AI faster with LLM Observability. Read the best practices guide 14th May 2026 Release datasette-ip-rate-limit 0.1a0 &mdash; Rate limit Datasette requests by client IP address The datasette.io site was being hammered by poorly-behaved crawlers, so I had Codex (GPT-5.5 xhigh) build a configurable rate limiting plugin to block IPs that were hammering specific areas of the site too quickly. Here's the production configuration I'm using on that site for the new plugin: datasette-ip-rate-limit : header : Fly-Client-IP max_keys : 10000 exempt_paths : - " /static/* " - " /-/turnstile* " rules : - name : demo-databases paths : - " /global-power-plants/* " - " /legislators/* " window_seconds : 60 max_requests : 60 block_seconds : 20 Posted 14th May 2026 at 4:10 am Recent articles Notes on the xAI/Anthropic data center deal - 7th May 2026 Live blog: Code w/ Claude 2026 - 6th May 2026 Vibe coding and agentic engineering are getting closer than I&#x27;d like - 6th May 2026 This is a beat by Simon Willison, posted on 14th May 2026 . rate-limiting 11 datasette 1484 codex 48 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
