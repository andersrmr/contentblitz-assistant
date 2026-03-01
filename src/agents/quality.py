from app.config import Settings
from app.models import Draft, QualityReport
from app.state import AppState


def quality_node(state: AppState) -> dict:
    settings = Settings()
    draft = Draft.model_validate(state["draft"])
    body_text = f"{draft.headline} {draft.body} {draft.cta}".strip()
    has_min_length = len(body_text) >= settings.min_draft_length
    has_cta = "call" in draft.cta.lower() or "book" in draft.cta.lower()
    checks = {"min_length": has_min_length, "cta_present": has_cta}
    feedback = []
    if not has_min_length:
        feedback.append("Draft is too short.")
    if not has_cta:
        feedback.append("CTA is missing.")
    report_data = {
        "passed": all(checks.values()),
        "score": sum(50 for passed in checks.values() if passed),
        "checks": checks,
        "feedback": feedback,
    }
    report = QualityReport.model_validate(report_data)
    return {"quality_report": report.model_dump()}
