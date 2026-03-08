from app.models import Draft, QualityReport, ResearchPacket
from app.state import AppState


def quality_node(state: AppState) -> dict:
    draft_data = state.get("draft")
    if draft_data is None:
        raise ValueError("quality_node requires 'draft' in state")
    research_data = state.get("research")
    if research_data is None:
        raise ValueError("quality_node requires 'research' in state")

    draft = Draft.model_validate(draft_data)
    research = ResearchPacket.model_validate(research_data)
    constraints = state.get("constraints", {})
    max_words = constraints.get("max_words") if isinstance(constraints, dict) else None

    body_words = draft.body.split()
    draft_citation_urls = {citation.url for citation in draft.citations}
    research_citation_urls = {citation.url for citation in research.citations}
    paragraphs = [segment for segment in draft.body.split("\n\n") if segment.strip()]
    combined_text_lower = f"{draft.headline}\n{draft.body}\n{draft.cta}".lower()
    body_lower = draft.body.lower()

    citations_present = len(research.citations) > 0
    citations_used = bool(draft_citation_urls & research_citation_urls)
    max_words_ok = True if max_words is None else len(body_words) <= int(max_words)
    headline_len_ok = len(draft.headline.split()) <= 12
    cta_text = draft.cta.strip()
    cta_present = bool(cta_text) and (
        cta_text in draft.body or draft.body.strip().endswith(cta_text)
    )
    skim_ok = len(paragraphs) >= 3
    tone_blocklist = [
        "secret weapon",
        "ultimate game changer",
        "transform your entire marketing organization",
        "transform your entire organization",
        "sign up today",
        "already behind the competition",
        "game changer",
    ]
    tone_ok = not any(phrase in combined_text_lower for phrase in tone_blocklist)
    brand_blocklist = [
        "hacks",
        "follow for more tips",
        "move fast",
        "just experiment",
        "worry about governance later",
        "every marketer should know",
        "try this now",
    ]
    brand_voice_ok = not any(phrase in combined_text_lower for phrase in brand_blocklist)
    generic_phrases = [
        "ai is becoming more important",
        "many organizations are thinking about",
        "companies should consider",
        "it is important to think about",
        "teams should think about",
        "businesses should think about",
    ]
    generic_phrase_hits = sum(1 for phrase in generic_phrases if phrase in body_lower)
    specificity_keywords = [
        "workflow",
        "review",
        "governance",
        "policy",
        "approval",
        "audit",
        "risk",
        "compliance",
        "reusable",
        "publish",
        "confidence",
        "consistency",
    ]
    specificity_signals = any(keyword in body_lower for keyword in specificity_keywords) or any(
        char.isdigit() for char in draft.body
    )
    specificity_ok = not (generic_phrase_hits >= 1 and not specificity_signals)

    checks = {
        "citations_present": citations_present,
        "citations_used": citations_used,
        "max_words": {
            "ok": max_words_ok,
            "limit": max_words,
            "actual": len(body_words),
        },
        "headline_len_ok": headline_len_ok,
        "cta_present": cta_present,
        "skim_ok": skim_ok,
        "tone_ok": tone_ok,
        "brand_voice_ok": brand_voice_ok,
        "specificity_ok": specificity_ok,
    }
    reasons: list[str] = []
    fixes: list[str] = []
    if not citations_present:
        reasons.append("Research has no citations to support the draft.")
        fixes.append("Include at least one citation in the research packet.")
    if not citations_used:
        reasons.append("Draft does not use any research citations.")
        fixes.append("Reuse at least one citation from the research packet.")
    if not max_words_ok:
        reasons.append("Draft exceeds the maximum word limit.")
        fixes.append("Shorten the draft body to fit the max_words constraint.")
    if not headline_len_ok:
        reasons.append("Headline exceeds 12 words.")
        fixes.append("Reduce the headline to 12 words or fewer.")
    if not cta_present:
        reasons.append("CTA is missing from the draft body.")
        fixes.append("Add the CTA sentence at the end of the draft body.")
    if not skim_ok:
        reasons.append("Draft is not skimmable enough for LinkedIn.")
        fixes.append("Use at least three short paragraphs separated by blank lines.")
    if not tone_ok:
        reasons.append("Draft tone is too promotional for professional B2B LinkedIn content.")
        fixes.append("Rewrite in a professional, analytical tone and remove hype or urgency-driven phrasing.")
    if not brand_voice_ok:
        reasons.append("Draft voice does not match a credible enterprise B2B brand voice.")
        fixes.append(
            "Rewrite in a credible, professional, enterprise-oriented voice and avoid casual influencer-style phrasing."
        )
    if not specificity_ok:
        reasons.append("Draft is too generic and lacks concrete operational insight.")
        fixes.append("Add at least one concrete, research-grounded operational insight relevant to the audience.")

    report_data = {
        "status": "pass" if not reasons else "fail",
        "reasons": reasons,
        "fixes": fixes,
        "checks": checks,
    }
    report = QualityReport.model_validate(report_data)
    report_dict = report.model_dump()
    result = {"quality_report": report_dict}
    if state.get("first_quality_report") is None:
        result["first_quality_report"] = report_dict
    return result
