import json
from typing import Any

from app.models import Citation, ContentBrief, Draft, ResearchPacket
from app.prompts import WRITER_SYSTEM, WRITER_USER_TEMPLATE
from app.state import AppState
from integrations.llm_openai import LLMError, OpenAIClient


def writer_linkedin_node(state: AppState) -> dict:
    research = ResearchPacket.model_validate(state["research"])
    brief = ContentBrief.model_validate(state["brief"])
    platform = state.get("platform", brief.channel)
    constraints = state.get("constraints", {})
    max_words = constraints.get("max_words") if isinstance(constraints, dict) else None
    fallback_data = {
        "channel": platform,
        "headline": brief.angle or "Content brief",
        "body": "\n".join(brief.outline) + "\n\n" + brief.cta,
        "cta": brief.cta,
        "citations": [
            Citation.model_validate(citation).model_dump()
            for citation in research.citations[:3]
        ],
    }
    errors = list(state.get("errors", []))
    meta = dict(state.get("meta", {}))

    try:
        llm_data = OpenAIClient().complete_json(
            system=WRITER_SYSTEM,
            user=WRITER_USER_TEMPLATE.format(
                platform=platform,
                max_words=max_words if max_words is not None else "not specified",
                brief=json.dumps(brief.model_dump(), indent=2),
                citations=json.dumps(
                    [citation.model_dump() for citation in research.citations],
                    indent=2,
                ),
            ),
        )
        if isinstance(llm_data, dict):
            fallback_data = {**fallback_data, **llm_data, "channel": platform}
    except LLMError as exc:
        errors.append(f"Writer fallback used: {exc}")
        meta["writer_fallback"] = "deterministic_draft"

    allowed_urls = {citation.url for citation in research.citations}
    valid_citations = [
        Citation.model_validate(citation).model_dump()
        for citation in fallback_data.get("citations", [])
        if citation.get("url", "") in allowed_urls
    ]
    draft_data = {
        "channel": fallback_data.get("channel", platform),
        "headline": fallback_data.get("headline", brief.angle or "Content brief"),
        "body": fallback_data.get("body", ""),
        "cta": fallback_data.get("cta", brief.cta),
        "citations": valid_citations,
    }
    draft = Draft.model_validate(draft_data)
    result: dict[str, Any] = {"draft": draft.model_dump()}
    if errors:
        result["errors"] = errors
    if meta:
        result["meta"] = meta
    return result
