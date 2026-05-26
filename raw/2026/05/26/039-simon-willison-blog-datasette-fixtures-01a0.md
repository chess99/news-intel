---
title: "datasette-fixtures 0.1a0"
source: Simon Willison Blog
url: https://simonwillison.net/2026/May/24/datasette-fixtures/#atom-everything
published: 2026-05-25T05:38:32+08:00
lang: en
category: ai_practitioner
fetched_at: 2026-05-26T00:30:20.506024+08:00
---

# datasette-fixtures 0.1a0

**来源**: Simon Willison Blog | **发布**: 2026-05-25 | **链接**: https://simonwillison.net/2026/May/24/datasette-fixtures/#atom-everything

## RSS 摘要

Release: datasette-fixtures 0.1a0 One of the smaller features in Datasette 1.0a30 is this: New documented datasette.fixtures.populate_fixture_database(conn) helper for creating the fixture database tables used by Datasette's own tests, intended for plugin test suites. This new plugin takes advantage of that API. You can try it out using uvx without even installing Datasette like this: uvx --prerelease=allow \ --with datasette-fixtures datasette \ --get /fixtures/roadside_attractions.json Which o

## 正文

Release: datasette-fixtures 0.1a0 Simon Willison’s Weblog Subscribe Sponsored by: exe.dev &mdash; ssh, root, https. Real VMs, not sandboxes. Edge-injected secrets so you can yolo. 0→1? ½→1! 24th May 2026 Release datasette-fixtures 0.1a0 &mdash; Add a fixtures test database to Datasette One of the smaller features in Datasette 1.0a30 is this: New documented datasette.fixtures.populate_fixture_database(conn) helper for creating the fixture database tables used by Datasette's own tests, intended for plugin test suites. This new plugin takes advantage of that API. You can try it out using uvx without even installing Datasette like this: uvx --prerelease=allow \ --with datasette-fixtures datasette \ --get /fixtures/roadside_attractions.json Which outputs: { "ok" : true , "next" : null , "rows" : [ { "pk" : 1 , "name" : " The Mystery Spot " , "address" : " 465 Mystery Spot Road, Santa Cruz, CA 95065 " , "url" : " https://www.mysteryspot.com/ " , "latitude" : 37.0167 , "longitude" : -122.0024 }, { "pk" : 2 , "name" : " Winchester Mystery House " , "address" : " 525 South Winchester Boulevard, San Jose, CA 95128 " , "url" : " https://winchestermysteryhouse.com/ " , "latitude" : 37.3184 , "longitude" : -121.9511 }, { "pk" : 3 , "name" : " Burlingame Museum of PEZ Memorabilia " , "address" : " 214 California Drive, Burlingame, CA 94010 " , "url" : null , "latitude" : 37.5793 , "longitude" : -122.3442 }, { "pk" : 4 , "name" : " Bigfoot Discovery Museum " , "address" : " 5497 Highway 9, Felton, CA 95018 " , "url" : " https://www.bigfootdiscoveryproject.com/ " , "latitude" : 37.0414 , "longitude" : -122.0725 } ], "truncated" : false } Posted 24th May 2026 at 9:38 pm Recent articles Datasette Agent - 21st May 2026 Gemini 3.5 Flash: more expensive, but Google plan to use it for everything - 19th May 2026 The last six months in LLMs in five minutes - 19th May 2026 This is a beat by Simon Willison, posted on 24th May 2026 . datasette 1499 uv 95 Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments. Pay me to send you less! Sponsor &amp; subscribe Disclosures Colophon &copy; 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
