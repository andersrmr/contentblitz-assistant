from app.models import ContentBrief, ResearchPacket
from app.state import AppState
from app.config import Settings


def strategist_node(state: AppState) -> dict:
    research = ResearchPacket.model_validate(state["research"])
    settings = Settings()
    topic = state.get("topic") or research.user_query
    audience = state.get("audience", "B2B marketers")
    brief_data = {
        "topic": topic,
        "audience": audience,
        "objective": "Drive demo interest with a practical educational post.",
        "channel": settings.DEFAULT_PLATFORM,
        "angle": (
            f"Show how {topic} creates repeatable content operations using "
            f"{research.key_findings[0].lower()}."
        ),
        "outline": [
            "Lead with the pain of inconsistent content production.",
            "Show how a structured AI workflow improves output quality.",
            "Close with a direct invitation to talk.",
        ],
        "cta": "Book a short strategy call to map your next content sprint.",
    }
    brief = ContentBrief.model_validate(brief_data)
    return {"content_brief": brief.model_dump()}
