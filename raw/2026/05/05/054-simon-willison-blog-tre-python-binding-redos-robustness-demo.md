---
title: "TRE Python binding — ReDoS robustness demo"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/4/tre-python-binding/#atom-everything
published: 2026-05-05T01:52:00+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-05T13:39:21.826209+08:00
---

# TRE Python binding — ReDoS robustness demo

**来源**: Simon Willison Blog | **发布**: 2026-05-05 | **链接**: https://simonwillison.net/2026/May/4/tre-python-binding/#atom-everything

## RSS 摘要

Research: TRE Python binding — ReDoS robustness demo If it's good enough for antirez to add to Redis I figured Ville Laurikari's TRE regular expression engine was worth exploring in a little more detail. I had Claude Code build an experimental Python binding (it used ctypes ) and try some malicious regular expression attacks against the library. TRE handles those much better than Python's standard library implementation, thanks mainly to the lack of support for backtracking. Tags: security , pyt

## 正文

Research: TRE Python binding — ReDoS robustness demo Simon Willison’s Weblog Subscribe Sponsored by: MongoDB &mdash; Join MongoDB.local London 2026 on 7 May to learn how teams move AI from prototype to production. 4th May 2026 Research TRE Python binding — ReDoS robustness demo &mdash; Demonstrating robust regex performance, this project offers a minimal Python ctypes binding to the TRE regex library, highlighting TRE’s immunity to regular expression denial-of-service (ReDoS) attacks that cripple Python&#x27;s built-in `re` module. Key benchmarks show that TRE processes even notorious &quot;evil&quot; patterns on gigantic inputs (10 million characters) much faster than `re` on tiny ones, and scales linearly with input size instead of exponentially. If it's good enough for antirez to add to Redis I figured Ville Laurikari's TRE regular expression engine was worth exploring in a little more detail. I had Claude Code build an experimental Python binding (it used ctypes ) and try some malicious regular expression attacks against the library. TRE handles those much better than Python's standard library implementation, thanks mainly to the lack of support for backtracking. Posted 4th May 2026 at 5:52 pm Recent articles LLM 0.32a0 is a major backwards-compatible refactor - 29th April 2026 Tracking the history of the now-deceased OpenAI Microsoft AGI clause - 27th April 2026 DeepSeek V4 - almost on the frontier, a fraction of the price - 24th April 2026 This is a beat by Simon Willison, posted on 4th May 2026 . c 53 ctypes 9 python 1249 regular-expressions 37 security 600 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
