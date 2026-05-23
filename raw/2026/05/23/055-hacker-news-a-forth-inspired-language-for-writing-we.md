---
title: "A Forth-inspired language for writing websites"
source: Hacker News
url: https://robida.net/entries/2026/05/21/a-forth-inspired-language-for-writing-websites
published: 2026-05-22T23:00:50+08:00
lang: en
category: community
fetched_at: 2026-05-23T00:30:22.886709+08:00
---

# A Forth-inspired language for writing websites

**来源**: Hacker News | **发布**: 2026-05-22 | **链接**: https://robida.net/entries/2026/05/21/a-forth-inspired-language-for-writing-websites

## RSS 摘要

Comments

## 正文

A Forth-inspired language for writing websites Beto Dealmeida ( / bɛtto de aʊˈmeɪ da / ) they/he Musician and software engineer. Former climate scientist. Always a webmaster. https://robida.net/ contact@robida.net Key Biscayne, FL, 33149, USA I don't remember where the idea came from, but I decided that it would be cool if I could write websites using a stack-based language. Something like this: : h1 ( s -- ) "&lt;h1&gt;" emit . "&lt;/h1&gt;" emit ; "Hello, World!" h1 So I wrote Forge. I quickly built a library of word definitions that let me easily add microformats to the HTML: : post-content "Hello, world! This is my first post with Forge!" p ; : post-body h-entry-start "&lt;p class='byline'&gt;" emit "2026-05-21T14:00:00Z" "May 21, 2026" dt-published " · by " emit "Beto" "/about" p-author "&lt;/p&gt;" emit h-entry-end "On building a tiny stack-based web language." p-summary "post-content" e-content "/hello-world" "permalink" u-url ; "Hello, world!" "post-body" blog-post Each site is a collection of pages, a library of words, and a stylesheet: my-site ├── lib.forge ├── style.css └── pages ├── about.forge ├── hello.forge └── notes.forge A single binary runs the website: forge --log forge.log my-site/ The binary does a lot. It has a webassembly compiler that generates HTML from .forge files. When you visit a page the compiler runs on the backend, and you get the actual HTML in the source code, as well as the original .forge source. But when you navigate between pages, a service worker captures the network request to the page, say, /notes , fetches the source /notes.forge ), and builds the HTML on the fly by running the compiler on the browser. So we have server-side rendering for crawlers and WebMentions, and client-side rendering for a SPA experience. I love the limitations of the language. You can persiste things to state, localStorage, or to an append-only log on the server. For example example, I can add a "like" button to posts like this: : like-button ( -- ) "❤" "do-like" on-click ; : do-like "1" "likes:demo" log-append ; : body "I liked this!" p like-button ; When you click it, appends the value "1" to the topic "likes:demo" in the log. It's just JSONL (one JSON document per line). Forms can submit to other .forge pages, and they simply put the contents in the stack for them. It's up to the target to use log-append to store in the backend. I like how weird it is. I might use it for my site, who knows? For now I'm just exploring some ideas. 2026-05-21T22:40:27.988Z 2026-05-22T00:08:35.705Z programming mailto:michael@mgrinder.org Factor has an HTML library that seems similar: https://docs.factorcode.org/content/vocab-html.html https://robida.net/entries/2026/05/22/reply-1 https://robida.net/entries/2026/05/21/a-forth-inspired-language-for-writing-websites
