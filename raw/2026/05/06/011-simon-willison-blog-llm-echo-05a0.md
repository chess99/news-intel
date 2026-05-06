---
title: "llm-echo 0.5a0"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/5/llm-echo/#atom-everything
published: 2026-05-05T09:31:54+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-06T00:30:12.466972+08:00
---

# llm-echo 0.5a0

**来源**: Simon Willison Blog | **发布**: 2026-05-05 | **链接**: https://simonwillison.net/2026/May/5/llm-echo/#atom-everything

## RSS 摘要

Release: llm-echo 0.5a0 New -o thinking 1 option to help test against LLM 0.32a0 and higher. This plugin provides a fake model called "echo" for LLM which doesn't run an LLM at all - it's useful for writing automated tests. You can now do this: uvx --with llm==0.32a1 --with llm-echo==0.5a0 llm -m echo hi -o thinking 1 This will fake a reasoning block to standard error before returning JSON echoing the prompt. Tags: llm

## 正文

Release: llm-echo 0.5a0 Simon Willison’s Weblog Subscribe Sponsored by: MongoDB &mdash; Join MongoDB.local London 2026 on 7 May to learn how teams move AI from prototype to production. 5th May 2026 Release llm-echo 0.5a0 &mdash; Debug plugin for LLM providing an echo model New -o thinking 1 option to help test against LLM 0.32a0 and higher. This plugin provides a fake model called "echo" for LLM which doesn't run an LLM at all - it's useful for writing automated tests. You can now do this: uvx --with llm==0.32a1 --with llm-echo==0.5a0 llm -m echo hi -o thinking 1 This will fake a reasoning block to standard error before returning JSON echoing the prompt. Posted 5th May 2026 at 1:31 am Recent articles LLM 0.32a0 is a major backwards-compatible refactor - 29th April 2026 Tracking the history of the now-deceased OpenAI Microsoft AGI clause - 27th April 2026 DeepSeek V4 - almost on the frontier, a fraction of the price - 24th April 2026 This is a beat by Simon Willison, posted on 5th May 2026 . llm 595 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
