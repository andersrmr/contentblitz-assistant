from app.models import ContentBrief, Draft
from app.state import AppState


def rewrite_node(state: AppState) -> dict:
    draft = Draft.model_validate(state["draft"])
    brief = ContentBrief.model_validate(state["content_brief"])
    body = draft.body
    if len(body) < 80:
        body = (
            f"{body} This revised version adds enough detail to explain the process clearly "
            "and make the next action obvious for the reader."
        )
    rewritten_data = {
        "channel": draft.channel,
        "headline": draft.headline,
        "body": body,
        "cta": brief.cta,
        "citations": [citation.model_dump() for citation in draft.citations],
    }
    rewritten = Draft.model_validate(rewritten_data)
    return {
        "draft": rewritten.model_dump(),
        "rewrite_count": state.get("rewrite_count", 0) + 1,
    }
