---
title: "Using Claude Code: The Unreasonable Effectiveness of HTML"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/#atom-everything
published: 2026-05-09T05:00:11+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-11T00:30:17.995172+08:00
---

# Using Claude Code: The Unreasonable Effectiveness of HTML

**来源**: Simon Willison Blog | **发布**: 2026-05-09 | **链接**: https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/#atom-everything

## RSS 摘要

Using Claude Code: The Unreasonable Effectiveness of HTML Thought-provoking piece by Thariq Shihipar (on the Claude Code team at Anthropic) advocating for HTML over Markdown as an output format to request from Claude. The article is crammed with interesting examples (collected on this site ) and prompt suggestions like this one: Help me review this PR by creating an HTML artifact that describes it. I'm not very familiar with the streaming/backpressure logic so focus on that. Render the actual di

## 正文

Using Claude Code: The Unreasonable Effectiveness of HTML Simon Willison’s Weblog Subscribe Sponsored by: WorkOS &mdash; Make your app Enterprise Ready with SSO, SCIM, RBAC, and more. 8th May 2026 - Link Blog Using Claude Code: The Unreasonable Effectiveness of HTML . Thought-provoking piece by Thariq Shihipar (on the Claude Code team at Anthropic) advocating for HTML over Markdown as an output format to request from Claude. The article is crammed with interesting examples (collected on this site ) and prompt suggestions like this one: Help me review this PR by creating an HTML artifact that describes it. I'm not very familiar with the streaming/backpressure logic so focus on that. Render the actual diff with inline margin annotations, color-code findings by severity and whatever else might be needed to convey the concept well. I've been defaulting to asking for most things in Markdown since the GPT-4 days, when the 8,192 token limit meant that Markdown's token-efficiency over HTML was extremely worthwhile. Thariq's piece here has caused me to reconsider that, especially for output. Asking Claude for an explanation in HTML means it can drop in SVG diagrams, interactive widgets, in-page navigation and all sorts of other neat ways of making the information more pleasant to navigate. I wrote about Useful patterns for building HTML tools last December, but that was focused very much on interactive utilities like the ones on my tools.simonwillison.net site. I'm excited to start experimenting more with rich HTML explanations in response to ad-hoc prompts. Trying this out on copy.fail copy.fail describes a recently discovered Linux security exploit, including a proof of concept distributed as obfuscated Python. I tried having GPT-5.5 create an HTML explanation of the exploit like this: curl https://copy.fail/exp | llm -m gpt-5.5 -s 'Explain this code in detail. Reformat it, expand out any confusing bits and go deep into what it does and how it works. Output HTML, neatly styled and using capabilities of HTML and CSS and JavaScript to make the explanation rich and interactive and as clear as possible' Here's the resulting HTML page . It's pretty good, though I should have emphasized explaining the exploit over the Python harness around it. Posted 8th May 2026 at 9 pm Recent articles Notes on the xAI/Anthropic data center deal - 7th May 2026 Live blog: Code w/ Claude 2026 - 6th May 2026 Vibe coding and agentic engineering are getting closer than I&#x27;d like - 6th May 2026 This is a link post by Simon Willison, posted on 8th May 2026 . html 96 security 602 markdown 32 ai 2009 prompt-engineering 190 generative-ai 1780 llms 1746 llm 597 claude-code 112 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
