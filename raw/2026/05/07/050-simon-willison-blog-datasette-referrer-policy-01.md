---
title: "datasette-referrer-policy 0.1"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/5/datasette-referrer-policy/#atom-everything
published: 2026-05-06T07:44:27+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-07T00:30:24.103320+08:00
---

# datasette-referrer-policy 0.1

**来源**: Simon Willison Blog | **发布**: 2026-05-06 | **链接**: https://simonwillison.net/2026/May/5/datasette-referrer-policy/#atom-everything

## RSS 摘要

Release: datasette-referrer-policy 0.1 The OpenStreetMap tiles on the Datasette global-power-plants demo weren't displaying correctly. This turned out to be caused by two bugs. The first is that the CAPTCHA I added to that site a few weeks ago was triggering for the .json fetch requests used by the map plugin, and since those weren't HTML the user was not being asked to solve them. Here's the fix . The second was that OpenStreetMap quite reasonably block tile requests from sites that use a Refer

## 正文

Release: datasette-referrer-policy 0.1 Simon Willison’s Weblog Subscribe Sponsored by: MongoDB &mdash; Join MongoDB.local London 2026 on 7 May to learn how teams move AI from prototype to production. 5th May 2026 Release datasette-referrer-policy 0.1 &mdash; Set the Referrer-Policy header for a Datasette site The OpenStreetMap tiles on the Datasette global-power-plants demo weren't displaying correctly. This turned out to be caused by two bugs. The first is that the CAPTCHA I added to that site a few weeks ago was triggering for the .json fetch requests used by the map plugin, and since those weren't HTML the user was not being asked to solve them. Here's the fix . The second was that OpenStreetMap quite reasonably block tile requests from sites that use a Referrer-Policy: no-referrer header. Datasette does this by default, and I didn't want to change that default on people without warning - so I had Codex + GPT-5.5 build me a new plugin to help set that header to another value. Posted 5th May 2026 at 11:44 pm Recent articles Vibe coding and agentic engineering are getting closer than I&#x27;d like - 6th May 2026 LLM 0.32a0 is a major backwards-compatible refactor - 29th April 2026 Tracking the history of the now-deceased OpenAI Microsoft AGI clause - 27th April 2026 This is a beat by Simon Willison, posted on 5th May 2026 . http 124 openstreetmap 55 datasette 1480 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
