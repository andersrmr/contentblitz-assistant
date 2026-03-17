from pathlib import Path
import sys
from typing import Any, cast

import streamlit as st

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from app.config import Settings
from app.state import AppState
from workflow.graph import content_marketing_graph


def _init_session() -> None:
    if "last_state" not in st.session_state:
        st.session_state.last_state = None


def _missing_required_keys() -> bool:
    settings = Settings()
    return not (settings.OPENAI_API_KEY.strip() and settings.SERPAPI_API_KEY.strip())


def _render_final_draft(result: dict[str, Any]) -> None:
    draft = result.get("draft", {})
    if isinstance(draft, dict):
        headline = str(draft.get("headline", "")).strip()
        body = str(draft.get("body", "")).strip()
        if headline:
            st.subheader(headline)
        if body:
            st.text(body)
        if not headline and not body:
            st.info("No draft output is available yet.")
    else:
        st.info("No draft output is available yet.")


def _render_supporting_artifacts(result: dict[str, Any]) -> None:
    tabs = st.tabs(["Research", "Brief", "Quality"])
    with tabs[0]:
        st.json(result.get("research", {}))
    with tabs[1]:
        st.json(result.get("brief", {}))
    with tabs[2]:
        st.json(result.get("quality_report", result.get("quality", {})))


def _build_create_state(topic: str, audience: str) -> AppState:
    return {
        "topic": topic,
        "audience": audience,
        "intent": "create",
        "revision_request": "",
        "rewrite_count": 0,
        "errors": [],
        "meta": {},
    }


def _build_revise_state(
    previous: dict[str, Any], topic: str, audience: str, revision_request: str
) -> AppState:
    return cast(
        AppState,
        {
            **previous,
            "topic": topic,
            "audience": audience,
            "intent": "revise",
            "revision_request": revision_request.strip() or "Make it clearer and tighter.",
            "rewrite_count": 0,
        },
    )


def _invoke_graph(state: AppState) -> dict[str, Any] | None:
    if _missing_required_keys():
        st.error(
            "Missing required API keys. Set OPENAI_API_KEY and SERPAPI_API_KEY in your deployment secrets/environment."
        )
        return None

    with st.spinner("Generating content..."):
        result = content_marketing_graph.invoke(cast(AppState, state))
    st.session_state.last_state = result
    return cast(dict[str, Any], result)


def run() -> None:
    st.set_page_config(page_title="AI Content Marketing Assistant", layout="wide")
    st.title("AI Content Marketing Assistant")
    st.caption("Generate and revise LinkedIn-ready content using a structured AI workflow.")
    st.caption("To run this app in production, configure secrets in your deployment environment.")
    _init_session()

    topic = st.text_input("Topic", value="AI content marketing")
    audience = st.text_input("Audience", value="B2B marketers")
    revision_request = st.text_area(
        "Revision request",
        value="",
        placeholder="e.g., Make it shorter, more technical, and tighten the CTA.",
    )

    col1, col2 = st.columns(2)
    run_new = col1.button("Run new draft", type="primary")
    revise = col2.button("Revise last draft", type="secondary")

    result: dict[str, Any] | None = None

    if run_new:
        result = _invoke_graph(_build_create_state(topic, audience))

    if revise:
        previous = st.session_state.last_state
        if not previous or not previous.get("draft"):
            st.error("No existing draft found to revise. Click 'Run new draft' first.")
        else:
            result = _invoke_graph(
                _build_revise_state(cast(dict[str, Any], previous), topic, audience, revision_request)
            )

    if result is None and st.session_state.last_state:
        st.divider()
        st.caption("Last run output")
        result = cast(dict[str, Any], st.session_state.last_state)

    if result:
        st.divider()
        st.markdown("### Final Draft")
        _render_final_draft(result)
        _render_supporting_artifacts(result)


if __name__ == "__main__":
    run()
