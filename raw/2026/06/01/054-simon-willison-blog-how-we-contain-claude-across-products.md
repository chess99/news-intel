---
title: "How we contain Claude across products"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/30/how-we-contain-claude/#atom-everything
published: 2026-05-31T05:36:24+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-06-01T17:14:16.414801+08:00
---

# How we contain Claude across products

**来源**: Simon Willison Blog | **发布**: 2026-05-31 | **链接**: https://simonwillison.net/2026/May/30/how-we-contain-claude/#atom-everything

## RSS 摘要

How we contain Claude across products A complaint I often have about sandboxing products is that they are rarely thoroughly documented , and in the absence of detailed documentation it's hard to know how much I can trust them. Anthropic just published a fantastic overview of how their various sandbox techniques work across Claude.ai , Claude Code, and Cowork. We constrain where and how an agent can act with process sandboxes, VMs, filesystem boundaries, and egress controls. The goal is to set a 

## 正文

How we contain Claude across products Simon Willison’s Weblog Subscribe Sponsored by: The AI App and Agent Factory &mdash; Microsoft Foundry is the enterprise Al platform where intelligence and trust ship with every agent. Try Foundry 30th May 2026 - Link Blog How we contain Claude across products . A complaint I often have about sandboxing products is that they are rarely thoroughly documented , and in the absence of detailed documentation it's hard to know how much I can trust them. Anthropic just published a fantastic overview of how their various sandbox techniques work across Claude.ai , Claude Code, and Cowork. We constrain where and how an agent can act with process sandboxes, VMs, filesystem boundaries, and egress controls. The goal is to set a hard boundary on what an agent can reach. For example, if credentials never enter the sandbox, they can't be exfiltrated, regardless of whether the cause is a user, a model finding a “creative” path, or an attacker. Claude.ai uses gVisor. Claude Code, run locally, uses Seatbelt on macOS and Bubblewrap on Linux. Claude Cowork runs a full VM (Apple's Virtualization framework on macOS, HCS on Windows). There's a lot in here, including some interesting stories of risks they missed such as the api.anthropic.com/v1/files exfiltration vector covered here previously . This reminded me it's time I took another look at Anthropic's open source srt (Anthropic Sandbox Runtime) tool - it's mature enough know that I'm ready to give it a proper go. Posted 30th May 2026 at 9:36 pm Recent articles Claude Opus 4.8: &quot;a modest but tangible improvement&quot; - 28th May 2026 I think Anthropic and OpenAI have found product-market fit - 27th May 2026 Notes on Pope Leo XIV&#x27;s encyclical on AI - 25th May 2026 This is a link post by Simon Willison, posted on 30th May 2026 . sandboxing 40 security 607 ai 2,047 generative-ai 1,808 llms 1,775 anthropic 289 claude 277 claude-code 115 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
