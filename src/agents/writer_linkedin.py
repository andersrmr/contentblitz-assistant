from app.models import Citation, ContentBrief, Draft, ResearchPacket
from app.state import AppState


def writer_linkedin_node(state: AppState) -> dict:
    research = ResearchPacket.model_validate(state["research_packet"])
    brief = ContentBrief.model_validate(state["content_brief"])
    draft_data = {
        "channel": "linkedin",
        "headline": f"{research.topic}: a cleaner way to ship consistent content",
        "body": (
            f"Most teams do not need more ideas. They need a repeatable process. "
            f"{research.topic} gives {research.audience} a stable workflow for research, "
            "planning, drafting, and review. That means fewer delays, clearer messaging, "
            "and content that is easier to approve across the team. "
            f"{brief.angle} Start with one clear workflow and iterate from there."
        ),
        "cta": brief.cta,
        "citations": [
            Citation.model_validate(citation).model_dump() for citation in research.citations
        ],
    }
    draft = Draft.model_validate(draft_data)
    return {"draft": draft.model_dump()}
