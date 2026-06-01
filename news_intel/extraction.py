from __future__ import annotations

from news_intel.models import Article, Candidate


EXTRACTION_PROMPT = """你是个人科技情报系统的信息抽取器。
只输出 JSON 对象，不输出 Markdown。

字段:
- event_key: kebab-case 事件键，优先使用公司/产品/动作
- title: 事实标题，不使用营销措辞
- summary: 80字以内事实摘要，保留限定词
- entities: 专有名词列表
- intent: one of official_announcement, reporting, commentary, pr, community_discussion, deal, tutorial, research, regulatory
- importance: 1-5
- confidence: low, medium, high
- caveats: 重要限制或缺失信息数组
- evidence_quote: 原文中最关键的一句证据

文章:
{article_text}
"""


def extract_candidate(article: Article, *, llm) -> Candidate:
    article_text = f"标题: {article.title}\n来源: {article.source}\n正文:\n{article.body[:5000]}"
    data = llm.complete_json(EXTRACTION_PROMPT.format(article_text=article_text))
    return Candidate(
        id=f"cand-{article.id}",
        article_id=article.id,
        date=article.date,
        event_key=data["event_key"],
        title=data["title"],
        summary=data["summary"],
        source=article.source,
        source_tier=article.source_tier,
        entities=data.get("entities", []),
        category=article.category,
        intent=data["intent"],
        importance=int(data["importance"]),
        confidence=data["confidence"],
        caveats=data.get("caveats", []),
        evidence_quote=data.get("evidence_quote", ""),
        url=article.url,
    )
