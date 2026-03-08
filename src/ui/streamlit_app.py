from pathlib import Path
import json
import sys
from typing import Any, cast

import pandas as pd
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


def _load_eval_results() -> dict[str, Any] | None:
    path = Path("evals/results/latest.json")
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return cast(dict[str, Any], json.load(f))


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

    st.divider()
    st.header("Eval Results")

    results = _load_eval_results()
    if not results:
        st.info("No eval results found. Run the eval harness first.")
        return

    agg = cast(dict[str, Any], results.get("aggregate", {}))
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Final Pass Rate", f"{float(agg.get('final_pass_rate', 0.0)):.2%}")
    col2.metric("First-Pass Pass Rate", f"{float(agg.get('first_pass_pass_rate', 0.0)):.2%}")
    col3.metric("Rewrite Trigger Rate", f"{float(agg.get('rewrite_trigger_rate', 0.0)):.2%}")
    col4.metric("Rewrite Recovery Rate", f"{float(agg.get('rewrite_recovery_rate', 0.0)):.2%}")
    col5.metric("Avg Rewrite Count", f"{float(agg.get('avg_rewrite_count', 0.0)):.2f}")

    st.subheader("Metrics by Category")
    by_cat = agg.get("by_category", {})
    if isinstance(by_cat, dict) and by_cat:
        df = pd.DataFrame(by_cat).T.reset_index()
        df = df.rename(columns={"index": "category"})
        st.dataframe(df, use_container_width=True)

    st.subheader("First-Pass Failure Reasons")
    reason_counts = agg.get("first_pass_failure_reason_counts", {})
    if isinstance(reason_counts, dict) and reason_counts:
        df_reasons = (
            pd.DataFrame(
                [{"reason": k, "count": v} for k, v in reason_counts.items()]
            )
            .sort_values("count", ascending=False)
            .reset_index(drop=True)
        )
        st.dataframe(df_reasons, use_container_width=True)
    else:
        st.caption("No first-pass failure reasons recorded.")

    st.subheader("Per-Case Results")
    cases = results.get("cases", [])
    if isinstance(cases, list) and cases:
        df_cases = pd.DataFrame(cases)
        columns = [
            "category",
            "case_id",
            "passed",
            "rewrite_count",
            "quality_status",
        ]
        visible_cols = [c for c in columns if c in df_cases.columns]
        st.dataframe(df_cases[visible_cols], use_container_width=True)

        case_ids = [str(c.get("case_id", "")) for c in cases if isinstance(c, dict) and c.get("case_id")]
        selected = st.selectbox("Inspect Case", case_ids)
        if selected:
            case = next(
                (c for c in cases if isinstance(c, dict) and str(c.get("case_id", "")) == selected),
                None,
            )
            if case is not None:
                st.json(case)


if __name__ == "__main__":
    run()
