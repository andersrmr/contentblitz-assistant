from typing import Any, TypedDict


class AppState(TypedDict, total=False):
    topic: str
    audience: str
    route: str
    research_packet: dict[str, Any]
    content_brief: dict[str, Any]
    draft: dict[str, Any]
    quality_report: dict[str, Any]
    rewrite_count: int
