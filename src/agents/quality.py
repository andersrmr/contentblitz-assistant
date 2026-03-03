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

    citations_present = len(research.citations) > 0
    citations_used = bool(draft_citation_urls & research_citation_urls)
    max_words_ok = True if max_words is None else len(body_words) <= int(max_words)
    headline_len_ok = len(draft.headline.split()) <= 12
    cta_text = draft.cta.strip()
    cta_present = bool(cta_text) and (
        cta_text in draft.body or draft.body.strip().endswith(cta_text)
    )
    skim_ok = len(paragraphs) >= 3

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

    report_data = {
        "status": "pass" if not reasons else "fail",
        "reasons": reasons,
        "fixes": fixes,
        "checks": checks,
    }
    report = QualityReport.model_validate(report_data)
    return {"quality_report": report.model_dump()}
