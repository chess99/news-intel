---
title: "Behind the Scenes Hardening Firefox with Claude Mythos Preview"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/7/firefox-claude-mythos/#atom-everything
published: 2026-05-08T01:56:25+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-09T00:30:19.817681+08:00
---

# Behind the Scenes Hardening Firefox with Claude Mythos Preview

**来源**: Simon Willison Blog | **发布**: 2026-05-08 | **链接**: https://simonwillison.net/2026/May/7/firefox-claude-mythos/#atom-everything

## RSS 摘要

Behind the Scenes Hardening Firefox with Claude Mythos Preview Fascinating, in-depth details on how Mozilla used their access to the Claude Mythos preview to locate and then fix hundreds of vulnerabilities in Firefox: Suddenly, the bugs are very good Just a few months ago, AI-generated security bug reports to open source projects were mostly known for being unwanted slop. Dealing with reports that look plausibly correct but are wrong imposes an asymmetric cost on project maintainers: it’s cheap 

## 正文

Behind the Scenes Hardening Firefox with Claude Mythos Preview Simon Willison’s Weblog Subscribe 7th May 2026 - Link Blog Behind the Scenes Hardening Firefox with Claude Mythos Preview ( via ) Fascinating, in-depth details on how Mozilla used their access to the Claude Mythos preview to locate and then fix hundreds of vulnerabilities in Firefox: Suddenly, the bugs are very good Just a few months ago, AI-generated security bug reports to open source projects were mostly known for being unwanted slop. Dealing with reports that look plausibly correct but are wrong imposes an asymmetric cost on project maintainers: it’s cheap and easy to prompt an LLM to find a “problem” in code, but slow and expensive to respond to it. It is difficult to overstate how much this dynamic changed for us over a few short months. This was due to a combination of two main factors. First, the models got a lot more capable. Second, we dramatically improved our techniques for harnessing these models — steering them, scaling them, and stacking them to generate large amounts of signal and filter out the noise. They include some detailed bug descriptions too, including a 20-year old XSLT bug and a 15-year-old bug in the &lt;legend&gt; element. A lot of the attempts made by the harness were blocked by Firefox's existing defense-in-depth measures, which is reassuring. Mozilla were fixing around 20-30 security bugs in Firefox per month through 2025. That jumped to 423 in April. Posted 7th May 2026 at 5:56 pm Recent articles Notes on the xAI/Anthropic data center deal - 7th May 2026 Live blog: Code w/ Claude 2026 - 6th May 2026 Vibe coding and agentic engineering are getting closer than I&#x27;d like - 6th May 2026 This is a link post by Simon Willison, posted on 7th May 2026 . firefox 101 mozilla 116 security 601 ai 2008 generative-ai 1779 llms 1745 anthropic 282 claude 275 ai-security-research 17 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
