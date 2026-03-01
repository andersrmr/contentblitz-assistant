from app.config import settings
from app.models import QualityReport
from app.state import AppState


def route_after_router(state: AppState) -> str:
    if state.get("route") == "revise":
        return "rewrite"
    return "research"


def route_after_quality(state: AppState) -> str:
    report = QualityReport.model_validate(state["quality_report"])
    if report.status == "pass":
        return "end"
    if state.get("rewrite_count", 0) >= settings.MAX_ITERATIONS:
        return "end"
    return "rewrite"
