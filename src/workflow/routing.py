from app.models import QualityReport
from app.state import AppState


def route_after_quality(state: AppState) -> str:
    report = QualityReport.model_validate(state["quality_report"])
    if report.passed:
        return "end"
    if state.get("rewrite_count", 0) >= 1:
        return "end"
    return "rewrite"
