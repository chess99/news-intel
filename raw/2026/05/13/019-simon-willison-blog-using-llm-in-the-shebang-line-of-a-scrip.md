---
title: "Using LLM in the shebang line of a script"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/11/llm-shebang/#atom-everything
published: 2026-05-12T02:48:57+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-13T00:30:09.871660+08:00
---

# Using LLM in the shebang line of a script

**来源**: Simon Willison Blog | **发布**: 2026-05-12 | **链接**: https://simonwillison.net/2026/May/11/llm-shebang/#atom-everything

## RSS 摘要

TIL: Using LLM in the shebang line of a script Kim_Bruning on Hacker News : But seriously, you can put a shebang on an english text file now (if you're sufficiently brave) [...] This inspired me to look at patterns for doing exactly that with LLM . Here's the simplest, which takes advantage of LLM fragments : #!/usr/bin/env -S llm -f Generate an SVG of a pelican riding a bicycle But you can also incorporate tool calls using the -T name_of_tool option: #!/usr/bin/env -S llm -T llm_time -f Write a

## 正文

TIL: Using LLM in the shebang line of a script Simon Willison’s Weblog Subscribe Sponsored by: WorkOS &mdash; Make your app Enterprise Ready with SSO, SCIM, RBAC, and more. 11th May 2026 TIL Using LLM in the shebang line of a script &mdash; This comment on Hacker News inspired me to investigate patterns for using my LLM CLI tool in a shebang line: Kim_Bruning on Hacker News : But seriously, you can put a shebang on an english text file now (if you're sufficiently brave) [...] This inspired me to look at patterns for doing exactly that with LLM . Here's the simplest, which takes advantage of LLM fragments : #!/usr/bin/env -S llm -f Generate an SVG of a pelican riding a bicycle But you can also incorporate tool calls using the -T name_of_tool option: #!/usr/bin/env -S llm -T llm_time -f Write a haiku that mentions the exact current time Or even execute YAML templates directly that define extra tools as Python functions: # !/usr/bin/env -S llm -t model : gpt-5.4-mini system : | Use tools to run calculations functions : | def add(a: int, b: int) -&gt; int: return a + b def multiply(a: int, b: int) -&gt; int: return a * b Then: ./calc.sh 'what is 2344 * 5252 + 134' --td Which outputs (thanks to that --td tools debug option): Tool call: multiply({'a': 2344, 'b': 5252}) 12310688 Tool call: add({'a': 12310688, 'b': 134}) 12310822 2344 × 5252 + 134 = **12,310,822** Read the full TIL for a more complex example that uses the Datasette SQL API to answer questions about content on my blog. Posted 11th May 2026 at 6:48 pm Recent articles Notes on the xAI/Anthropic data center deal - 7th May 2026 Live blog: Code w/ Claude 2026 - 6th May 2026 Vibe coding and agentic engineering are getting closer than I&#x27;d like - 6th May 2026 This is a beat by Simon Willison, posted on 11th May 2026 . ai 2016 generative-ai 1785 llms 1751 llm 598 llm-tool-use 68 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
