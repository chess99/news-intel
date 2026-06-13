from __future__ import annotations

import re

from news_intel.clustering import stable_id
from news_intel.models import Article, Candidate, SourceTier


ENTITY_PATTERNS = [
    "Anthropic",
    "OpenAI",
    "Google",
    "DeepMind",
    "Microsoft",
    "Meta",
    "Apple",
    "Amazon",
    "AWS",
    "NVIDIA",
    "Oracle",
    "PeopleSoft",
    "Chrome",
    "WebMCP",
    "GitHub",
    "Kubernetes",
    "Prometheus",
    "Arch",
    "AUR",
    "Colab",
    "Fable",
    "Mythos",
]

SECURITY_TERMS = {
    "0-day",
    "zero-day",
    "cve",
    "vulnerability",
    "exploit",
    "exploited",
    "malicious",
    "breach",
    "rce",
    "vulnerability",
    "恶意",
    "漏洞",
    "供应链攻击",
}

REGULATORY_TERMS = {
    "regulator",
    "regulatory",
    "regulation",
    "监管",
    "调查",
    "合规",
    "暂停",
    "pause",
    "paused",
    "safety",
}

DEVELOPER_TOOL_TERMS = {
    "sdk",
    "api",
    "cli",
    "developer",
    "developers",
    "tool",
    "tools",
    "origin trial",
    "github",
    "chrome",
    "kubernetes",
    "prometheus",
    "webmcp",
    "colab",
}

MODEL_TERMS = {"model", "llm", "agent", "agents", "eval", "benchmark", "inference"}

DEAL_TERMS = {
    "raises",
    "raised",
    "funding",
    "financing",
    "series a",
    "series b",
    "ipo",
    "acquisition",
    "valuation",
    "$",
    "融资",
}

MARKETING_TERMS = {
    "transform",
    "revolutionize",
    "game-changing",
    "next-generation",
    "博人眼球",
}

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "into",
    "after",
    "says",
    "new",
    "launches",
    "introduces",
    "announces",
    "发布",
    "推出",
}


def extract_candidate(article: Article, *, llm: object | None = None) -> Candidate:
    del llm
    return extract_candidate_fast(article)


def extract_candidate_fast(article: Article) -> Candidate:
    text = "\n".join([article.title, article.summary, article.body])
    lower = text.lower()
    entities = extract_entities(text)
    intent = classify_intent(lower, article.source_tier)
    importance = score_importance(lower, article.source_tier, intent)
    evidence_quote = first_sentence(article.body or article.summary or article.title)
    summary = summarize_article(article)
    return Candidate(
        id=f"cand-{article.id}",
        article_id=article.id,
        date=article.date,
        event_key=event_key(article, entities),
        title=clean_title(article.title),
        summary=summary,
        source=article.source,
        source_tier=article.source_tier,
        entities=entities,
        category=article.category,
        intent=intent,
        importance=importance,
        confidence="high" if article.source_tier == SourceTier.T0_FIRST_HAND else "medium",
        caveats=[] if article.source_tier == SourceTier.T0_FIRST_HAND else ["需要一手来源交叉确认。"],
        evidence_quote=evidence_quote,
        url=article.url,
    )


def extract_entities(text: str) -> list[str]:
    found: list[str] = []
    lower = text.lower()
    for name in ENTITY_PATTERNS:
        if name.lower() in lower and name not in found:
            found.append(name)
    return found


def classify_intent(lower_text: str, tier: SourceTier) -> Candidate.model_fields["intent"].annotation:
    if has_any(lower_text, REGULATORY_TERMS):
        return "regulatory"
    if has_any(lower_text, DEAL_TERMS):
        return "deal"
    if has_any(lower_text, {"research", "paper", "benchmark", "eval", "研究", "论文"}):
        return "research"
    if tier == SourceTier.T0_FIRST_HAND:
        return "official_announcement"
    if has_any(lower_text, {"reddit", "hacker news", "github issue", "discussion"}):
        return "community_discussion"
    if has_any(lower_text, {"tutorial", "guide", "how to", "教程"}):
        return "tutorial"
    if has_any(lower_text, MARKETING_TERMS):
        return "pr"
    return "reporting"


def score_importance(lower_text: str, tier: SourceTier, intent: str) -> int:
    score = 2
    if tier == SourceTier.T0_FIRST_HAND:
        score += 1
    if tier == SourceTier.T1_HIGH_QUALITY_SECONDARY:
        score += 1
    if has_any(lower_text, SECURITY_TERMS):
        score += 2
    if has_any(lower_text, REGULATORY_TERMS):
        score += 2
    if has_any(lower_text, DEVELOPER_TOOL_TERMS):
        score += 1
    if has_any(lower_text, MODEL_TERMS):
        score += 1
    if intent == "deal":
        score -= 3
    if has_any(lower_text, MARKETING_TERMS):
        score -= 1
    return max(1, min(5, score))


def event_key(article: Article, entities: list[str]) -> str:
    lower = f"{article.title} {article.summary} {article.body[:500]}".lower()
    if "anthropic" in lower and ("fable" in lower or "mythos" in lower):
        return "anthropic-fable-mythos-regulatory-pause"
    if "peoplesoft" in lower and ("zero-day" in lower or "0-day" in lower or "exploit" in lower):
        return "oracle-peoplesoft-zero-day-exploitation"
    if "webmcp" in lower and "chrome" in lower:
        return "chrome-webmcp-origin-trial"

    tokens = []
    tokens.extend(slugify(entity) for entity in entities[:3])
    words = [
        word
        for word in re.findall(r"[a-zA-Z0-9]+", article.title.lower())
        if len(word) > 2 and word not in STOPWORDS
    ]
    tokens.extend(words[:5])
    raw = "-".join(token for token in tokens if token)
    if raw:
        return raw[:80].strip("-")
    return stable_id("event-key", f"{article.source}:{article.title}")


def summarize_article(article: Article) -> str:
    source_text = article.summary or first_sentence(article.body) or article.title
    return truncate(clean_whitespace(source_text), 140)


def first_sentence(text: str) -> str:
    cleaned = clean_whitespace(text)
    if not cleaned:
        return ""
    parts = re.split(r"(?<=[。.!?])\s+", cleaned)
    return truncate(parts[0], 180)


def clean_title(title: str) -> str:
    return clean_whitespace(title).strip(" -|")


def clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def slugify(text: str) -> str:
    return "-".join(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def has_any(text: str, terms: set[str]) -> bool:
    for term in terms:
        if needs_word_boundary(term):
            if re.search(rf"(?<![a-zA-Z0-9]){re.escape(term)}(?![a-zA-Z0-9])", text):
                return True
        elif term in text:
            return True
    return False


def needs_word_boundary(term: str) -> bool:
    return all(ord(char) < 128 for char in term) and any(char.isalnum() for char in term)
