from typing import Any

from app.config import settings
from app.models import ContentBrief, ResearchPacket
from app.prompts import STRATEGIST_SYSTEM, STRATEGIST_USER_TEMPLATE
from app.state import AppState
from integrations.llm_openai import LLMError, OpenAIClient


def strategist_node(state: AppState) -> dict:
    research = ResearchPacket.model_validate(state["research"])
    topic = state.get("user_query") or state.get("topic", research.user_query)
    platform = state.get("platform", settings.DEFAULT_PLATFORM)
    fallback_data = {
        "topic": topic,
        "audience": "Professional audience",
        "objective": "Educate and engage",
        "channel": platform,
        "angle": research.angles[0] if research.angles else "Practical implementation angle",
        "outline": (research.key_findings[:5] or ["Lead with the problem", "Offer a practical takeaway", "Invite discussion"]),
        "cta": "What are your thoughts?",
    }
    errors = list(state.get("errors", []))
    meta = dict(state.get("meta", {}))

    try:
        llm_data = OpenAIClient().complete_json(
            system=STRATEGIST_SYSTEM,
            user=STRATEGIST_USER_TEMPLATE.format(
                user_query=topic,
                platform=platform,
                key_findings="\n".join(f"- {item}" for item in research.key_findings),
                angles="\n".join(f"- {item}" for item in research.angles),
            ),
        )
        if isinstance(llm_data, dict):
            fallback_data = {**fallback_data, **llm_data, "channel": platform}
    except LLMError as exc:
        errors.append(f"Strategist fallback used: {exc}")
        meta["strategist_fallback"] = "deterministic_brief"

    brief = ContentBrief.model_validate(fallback_data)
    result: dict[str, Any] = {
        "brief": brief.model_dump(),
        "content_brief": brief.model_dump(),
    }
    if errors:
        result["errors"] = errors
    if meta:
        result["meta"] = meta
    return result
