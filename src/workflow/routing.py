from app.config import settings
from app.models import QualityReport
from app.state import AppState


def route_after_router(state: AppState) -> str:
    if state.get("route") == "revise":
        return "rewrite"
    return "research"


def route_after_quality(state: AppState) -> str:
    quality_report_data = state.get("quality_report")
    if quality_report_data is None:
        raise ValueError("route_after_quality requires 'quality_report' in state")

    report = QualityReport.model_validate(quality_report_data)
    if report.status == "pass":
        return "end"
    if state.get("rewrite_count", 0) >= settings.MAX_ITERATIONS:
        return "end"
    return "rewrite"
