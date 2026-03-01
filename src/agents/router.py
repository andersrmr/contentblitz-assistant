from app.state import AppState


def router_node(state: AppState) -> dict:
    intent = state.get("intent", "").lower()
    route = "revise" if intent == "revise" else "linkedin_post"
    return {"route": route, "rewrite_count": state.get("rewrite_count", 0)}
