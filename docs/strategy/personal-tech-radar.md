# Personal Tech Radar Strategy

**Date:** 2026-06-01
**Status:** Core direction for future iteration

## Core Thesis

News Intel should be a personal technology intelligence system, not a public news site and not a generic daily digest.

The original motivation remains sound: the user's default technology news environment is dominated by WeChat and other second-hand Chinese media, where headlines often exaggerate, omit source context, and package marketing narratives as industry insight. The useful product is therefore not "more news." The useful product is a system that:

- Watches first-hand and high-quality sources the user would not manually check every day.
- Removes low-value repetition, PR framing, and headline inflation.
- Preserves evidence, source type, and caveats so the user can trust or reject the summary quickly.
- Maintains history across events, entities, and claims so daily fragments can become long-term judgment.
- Pushes a small number of useful items into an existing daily reading surface instead of expecting the user to open a website.

The website is an archive and research surface. It is not the primary reading interface.

## Product Principles

1. **Push, not pull.**
   The daily output should arrive where the user already reads: Feishu, email, Telegram, WeChat-compatible relay, or another chosen inbox. GitHub Pages exists for search, timelines, and historical reference.

2. **Evidence before prose.**
   Every important item must expose its original URL, source tier, key quote or evidence snippet, missing context, and confidence. A polished paragraph without evidence is not enough.

3. **First-hand sources are preferred, but source health is explicit.**
   Many first-hand sources are outside the firewall and depend on mihomo or other proxy paths. The system must expect partial failure, record source health, and show stale or failed first-hand coverage instead of silently falling back to second-hand media.

4. **AI is routed, not trusted wholesale.**
   Cheap deterministic rules and lightweight model calls handle extraction, categorization, deduplication, and rough ranking. Strong models or agentic investigation are reserved for a small number of high-value events, weekly synthesis, and cases that require evidence checking across multiple sources.

5. **History is structured, not pasted into a prompt.**
   Long-term value comes from maintaining durable records for events, entities, and claims. The system should not ask a weak model to read all past briefs and invent trends. It should update structured history and let stronger synthesis operate on curated context.

6. **The daily brief should be small.**
   A good daily brief has roughly five to eight items. It should make skipped information visible through counts and source health, but it should not recreate an information stream.

7. **The user should be able to correct the radar.**
   Feedback such as useful, not useful, track this, mute this source, and mute this topic should affect future ranking and topic surfaces.

## Source Strategy

Sources are tiered by their evidentiary role.

| Tier | Role | Examples | How to Use |
|---|---|---|---|
| T0 First-hand | Primary evidence | Official company blogs, product changelogs, GitHub releases, papers, regulators, standards bodies | Prefer for factual claims. If unavailable, mark coverage as stale or failed. |
| T1 High-quality secondary | Reporting and context | Ars Technica, MIT Technology Review, Wired, The Verge, TechCrunch, Simon Willison, Latent Space | Use for discovery, analysis, and context. Cross-check important claims against T0 when possible. |
| T2 Community discovery | Early signal and anomaly detection | Hacker News, Product Hunt, GitHub Trending, selected Reddit feeds | Use for leads and attention shifts. Do not treat as proof. |
| T3 Chinese secondary | Local narrative and user-context signal | 36氪, 机器之心, 量子位, 爱范儿, 极客公园, 钛媒体 | Use to understand Chinese-language framing and discover domestic items. Treat marketing-heavy claims with extra skepticism. |

The pipeline should record per-source health: last successful fetch, last attempted fetch, status, failure reason, consecutive failures, fetched item count, and proxy path. This health information belongs in both machine state and the human daily brief.

## AI Strategy

The system uses three levels of intelligence.

**Level 1: Deterministic and cheap processing**

- Fetch articles.
- Parse frontmatter and body.
- Normalize URLs, titles, dates, entities, and source metadata.
- Filter obvious ads, duplicates, deals, and non-technology items using rules.
- Maintain source health.

**Level 2: Lightweight LLM extraction**

- Extract structured facts from each candidate article.
- Classify source intent: official announcement, reporting, commentary, PR, community discussion, deal, tutorial, research, regulatory document.
- Produce short summaries, entity mentions, proposed event keys, and score candidates.
- Output JSON only, validated before persistence.

**Level 3: Strong model or agentic investigation**

- Investigate the top three to five daily events.
- Check first-hand evidence when secondary sources make important claims.
- Compare the event against prior events and claims.
- Decide whether a claim is supported, weakened, contradicted, or unchanged.
- Generate weekly and monthly synthesis.

Agentic work should be rare and intentional. The agent is for evidence gathering and judgment, not for rewriting every article.

## History Model

History is maintained through three durable objects.

**Event**

A concrete dated occurrence. Examples: a model release, a product launch, a funding event, a regulation update, a security incident, or a research result.

Events store evidence, involved entities, source tier, confidence, importance, and links to related claims.

**Entity**

A durable subject such as OpenAI, Anthropic, Cursor, Vite, MCP, a startup, a technology path, or a regulator.

Entities accumulate timelines and make it possible to answer "what changed about this thing over time?"

**Claim**

A testable long-running hypothesis or judgment. Examples:

- AI coding agents are moving from chat-style assistance into autonomous engineering environments.
- Rust-based tooling is taking over performance-critical JavaScript infrastructure.
- Consumer AI subscription willingness is fragmenting by use case and distribution channel.
- Chinese AI media headlines overstate product maturity more often than official sources.

Claims are updated by events using explicit relationship labels: supports, weakens, contradicts, or neutral. The system should keep claim status conservative. It is better to say "not enough evidence" than to synthesize a weak trend.

## Output Surfaces

**Daily Brief**

Primary surface. Five to eight items. Each item includes:

- What happened.
- Why it matters.
- Source tier and original URL.
- Key evidence quote or snippet.
- Confidence and caveats.
- Historical link, if meaningful.
- Whether it enters a tracked topic or claim.

**Weekly Review**

Three to five themes, generated from tracked events and claims. It should answer:

- Which narratives were strengthened?
- Which narratives were weakened?
- Which events changed the user's mental model?
- Which topics should be tracked, muted, or downgraded?

**Topic, Entity, and Claim Pages**

The website should evolve away from "daily markdown archive" and toward:

- Latest daily brief.
- Source health dashboard.
- Topic pages.
- Entity timelines.
- Claim pages with evidence history.
- Search across events, briefs, entities, and claims.

## Full End-State Direction

The ideal version is a Personal Tech Radar:

1. The fetch layer watches tiered sources through RSS, direct HTTP, page extraction, and optional browser-assisted fallbacks.
2. The ingestion layer normalizes articles and records source health.
3. The extraction layer turns articles into structured candidates.
4. The clustering layer merges candidates into events.
5. The knowledge layer updates entities, claims, and timelines.
6. The investigation layer uses stronger AI only for high-value or uncertain events.
7. The briefing layer produces a small daily push and richer weekly/monthly synthesis.
8. The site layer provides historical exploration rather than competing with the push surface.

The success test is behavioral: the user should be willing to read the daily push without opening the site, and the weekly review should create at least one durable judgment or correction that the user would not have reached from scattered articles alone.
