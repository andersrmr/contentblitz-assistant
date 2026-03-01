from app.state import AppState


def router_node(state: AppState) -> dict:
    return {"route": "linkedin_post", "rewrite_count": state.get("rewrite_count", 0)}
