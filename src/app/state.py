from typing import Any, TypedDict


class AppState(TypedDict, total=False):
    intent: str
    user_query: str
    topic: str
    audience: str
    platform: str
    constraints: dict[str, Any]
    route: str
    research: dict[str, Any]
    brief: dict[str, Any]
    draft: dict[str, Any]
    first_quality_report: dict[str, Any]
    quality_report: dict[str, Any]
    rewrite_count: int
    revision_request: str
    errors: list[str]
    meta: dict[str, Any]
