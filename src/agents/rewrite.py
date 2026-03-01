import json
from typing import Any

from app.models import ContentBrief, Citation, Draft, QualityReport, ResearchPacket
from app.prompts import REWRITE_SYSTEM, REWRITE_USER_TEMPLATE
from app.state import AppState
from integrations.llm_openai import LLMError, OpenAIClient


def _reflow_linkedin_paragraphs(body: str) -> str:
    normalized = body.replace("\n\n", " ").replace("\n", " ").strip()
    if not normalized:
        return body

    sentences = [segment.strip() for segment in normalized.split(". ") if segment.strip()]
    if len(sentences) >= 3:
        return "\n\n".join(sentences)

    paragraphs: list[str] = []
    current: list[str] = []
    for sentence in sentences:
        current.append(sentence)
        if len(current) == 2:
            paragraphs.append(". ".join(current).strip())
            current = []
    if current:
        paragraphs.append(". ".join(current).strip())

    if len(paragraphs) >= 3:
        return "\n\n".join(paragraphs)
    return body


def _post_process_draft_data(draft_data: dict[str, Any]) -> dict[str, Any]:
    body = str(draft_data.get("body", "")).strip()
    cta = str(draft_data.get("cta", "")).strip()

    if cta and cta not in body:
        body = f"{body}\n\n{cta}".strip()

    paragraphs = [segment for segment in body.split("\n\n") if segment.strip()]
    if len(paragraphs) < 3:
        body = _reflow_linkedin_paragraphs(body)

    draft_data["body"] = body
    return draft_data


def rewrite_node(state: AppState) -> dict:
    draft = Draft.model_validate(state["draft"])
    brief_data = state.get("brief")
    if brief_data is None:
        raise ValueError("rewrite_node requires 'brief' in state")
    brief = ContentBrief.model_validate(brief_data)
    research = ResearchPacket.model_validate(state["research"])
    report = QualityReport.model_validate(state["quality_report"])

    fallback_body = draft.body.strip()
    constraints = state.get("constraints", {})
    max_words = constraints.get("max_words") if isinstance(constraints, dict) else None
    if draft.cta and draft.cta not in fallback_body:
        fallback_body = f"{fallback_body}\n\n{draft.cta}".strip()
    if len(fallback_body.split("\n\n")) < 3:
        fallback_body = fallback_body.replace("\n\n", "\n").strip()
        fallback_body = f"{fallback_body}\n\n{brief.angle}\n\n{draft.cta}".strip()
    if max_words is not None:
        words = fallback_body.split()
        if len(words) > int(max_words):
            fallback_body = " ".join(words[: int(max_words)]).strip()
            if draft.cta and draft.cta not in fallback_body:
                fallback_body = f"{fallback_body}\n\n{draft.cta}".strip()

    fallback_data = {
        "channel": draft.channel,
        "headline": " ".join(draft.headline.split()[:12]),
        "body": fallback_body,
        "cta": draft.cta or brief.cta,
        "citations": [citation.model_dump() for citation in research.citations[:3]],
    }
    errors = list(state.get("errors", []))
    meta = dict(state.get("meta", {}))

    try:
        llm_data = OpenAIClient().complete_json(
            system=REWRITE_SYSTEM,
            user=REWRITE_USER_TEMPLATE.format(
                draft=json.dumps(draft.model_dump(), indent=2),
                fixes="\n".join(f"- {fix}" for fix in report.fixes),
                revision_request=state.get("revision_request", ""),
                citations=json.dumps(
                    [citation.model_dump() for citation in research.citations],
                    indent=2,
                ),
            ),
        )
        if isinstance(llm_data, dict):
            fallback_data = {**fallback_data, **llm_data}
    except LLMError as exc:
        errors.append(f"Rewrite fallback used: {exc}")
        meta["writer_fallback"] = "deterministic_rewrite"

    allowed_urls = {citation.url for citation in research.citations}
    valid_citations = [
        Citation.model_validate(citation).model_dump()
        for citation in fallback_data.get("citations", [])
        if citation.get("url", "") in allowed_urls
    ]
    draft_data = _post_process_draft_data(
        {
            "channel": fallback_data.get("channel", draft.channel),
            "headline": fallback_data.get("headline", draft.headline),
            "body": fallback_data.get("body", fallback_body),
            "cta": fallback_data.get("cta", draft.cta or brief.cta),
            "citations": valid_citations,
        }
    )
    rewritten = Draft.model_validate(draft_data)
    result: dict[str, Any] = {
        "draft": rewritten.model_dump(),
        "rewrite_count": state.get("rewrite_count", 0) + 1,
    }
    if errors:
        result["errors"] = errors
    if meta:
        result["meta"] = meta
    return result
