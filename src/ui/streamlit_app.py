from pathlib import Path
import sys
from typing import Any, cast

import streamlit as st

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from app.state import AppState
from workflow.graph import content_marketing_graph


def _init_session() -> None:
    if "last_state" not in st.session_state:
        st.session_state.last_state = None


def _render_result(result: dict[str, Any]) -> None:
    tabs = st.tabs(["Research", "Brief", "Draft", "Quality"])
    with tabs[0]:
        st.json(result.get("research", {}))
    with tabs[1]:
        st.json(result.get("brief", {}))
    with tabs[2]:
        st.json(result.get("draft", {}))
    with tabs[3]:
        # your graph currently returns quality_report (and maybe quality too)
        st.json(result.get("quality", result.get("quality_report", {})))


def run() -> None:
    st.set_page_config(page_title="AI Content Marketing Assistant", layout="wide")
    st.title("AI Content Marketing Assistant")
    _init_session()

    # Inputs
    topic = st.text_input("Topic", value="AI content marketing")
    audience = st.text_input("Audience", value="B2B marketers")
    revision_request = st.text_area(
        "Revision request (for revising an existing draft)",
        value="",
        placeholder="e.g., Make it shorter, more technical, stronger hook and CTA...",
    )

    col1, col2 = st.columns(2)

    run_new = col1.button("Run new draft", type="primary")
    revise = col2.button("Revise last draft", type="secondary")

    # CREATE: start fresh for this run (don’t carry last draft unless you want to)
    if run_new:
        state: AppState = {
            "topic": topic,
            "audience": audience,
            "intent": "create",
            "revision_request": "",
            "rewrite_count": 0,
            "errors": [],
            "meta": {},
        }
        result = content_marketing_graph.invoke(cast(AppState, state))
        st.session_state.last_state = result
        _render_result(result)

    # REVISE: requires last_state with a draft; carry it forward
    if revise:
        prev = st.session_state.last_state
        if not prev or not prev.get("draft"):
            st.error("No existing draft found to revise. Click 'Run new draft' first.")
            return

        # Carry forward prior artifacts so rewrite has context
        state = cast(
            AppState,
            {
                **dict(cast(dict[str, Any], prev)),
                "topic": topic,
                "audience": audience,
                "intent": "revise",
                "revision_request": revision_request.strip()
                or "Make it clearer and tighter.",
                "rewrite_count": 0,
            },
        )

        result = content_marketing_graph.invoke(cast(AppState, state))
        st.session_state.last_state = result
        _render_result(result)

    # If we already have a result, show it (useful after reruns)
    if (not run_new and not revise) and st.session_state.last_state:
        st.divider()
        st.caption("Last run output")
        _render_result(st.session_state.last_state)


if __name__ == "__main__":
    run()
