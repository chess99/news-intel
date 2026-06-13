# Newsletter Reference Patterns

This note records format lessons from the KM newsletters used as references. It does not archive their full text.

## Useful Patterns

### Frontline Newsletter

- Starts with a compact trend scan before individual items.
- Uses category sections to reduce cognitive load.
- Keeps each item multi-source when possible instead of treating every URL as a separate story.
- Works best for broad discovery, but can become long if every item is preserved.

### Frontend Newsletter

- Opens with a named `Signal` that connects multiple events into one judgment.
- Uses article cards: source tag, headline, one-line takeaway, then short context.
- Separates research, tools, and industry updates so readers can scan by intent.
- The strongest part is not the item list; it is the editorial thesis at the top.

## Migration Principles

- Feishu is the primary reading surface, so the daily brief must be complete and pleasant without opening the site.
- The first screen should answer: "What changed in my judgment today?"
- Daily reports should lead with a Signal, then 3 to 5 must-read cards, then a short scan list.
- Machine fields such as `event_id`, `claim_id`, confidence labels, raw evidence ids, and tier enums stay in JSON artifacts, not in reader-facing Markdown.
- Multiple reports about the same event should merge into one item with up to 3 representative sources.
- First-hand sources, security, regulation, developer tools, and model capability changes outrank funding, generic business commentary, and marketing launches.
- History is still valuable, but daily rendering should not pretend to produce deep longitudinal conclusions unless the evidence is explicit.

## Target Daily Shape

```text
今日 Signal
先看结论
必读
值得扫一眼
资料库
信源状态
```

`data/editorial/YYYY-MM-DD.json` is the handoff between structured events and the reader-facing brief. It can be produced by a batch LLM pass or deterministic rules, but the Markdown renderer should stay simple and predictable.
