from app.models import ContentBrief, ResearchPacket
from app.state import AppState


def strategist_node(state: AppState) -> dict:
    research = ResearchPacket.model_validate(state["research_packet"])
    brief_data = {
        "topic": research.topic,
        "audience": research.audience,
        "objective": "Drive demo interest with a practical educational post.",
        "channel": "linkedin",
        "angle": f"Show how {research.topic} creates repeatable content operations.",
        "outline": [
            "Lead with the pain of inconsistent content production.",
            "Show how a structured AI workflow improves output quality.",
            "Close with a direct invitation to talk.",
        ],
        "cta": "Book a short strategy call to map your next content sprint.",
    }
    brief = ContentBrief.model_validate(brief_data)
    return {"content_brief": brief.model_dump()}
