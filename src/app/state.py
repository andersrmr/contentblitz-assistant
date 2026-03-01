from typing import Any, TypedDict


class AppState(TypedDict, total=False):
    user_query: str
    topic: str
    audience: str
    platform: str
    route: str
    research: dict[str, Any]
    brief: dict[str, Any]
    content_brief: dict[str, Any]
    draft: dict[str, Any]
    quality_report: dict[str, Any]
    rewrite_count: int
    errors: list[str]
    meta: dict[str, Any]
