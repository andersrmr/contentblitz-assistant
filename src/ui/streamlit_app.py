from pathlib import Path
import sys

import streamlit as st

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from workflow.graph import content_marketing_graph


def run() -> None:
    st.set_page_config(page_title="AI Content Marketing Assistant", layout="wide")
    st.title("AI Content Marketing Assistant")

    topic = st.text_input("Topic", value="AI content marketing")
    audience = st.text_input("Audience", value="B2B marketers")

    if st.button("Run workflow", type="primary"):
        result = content_marketing_graph.invoke({"topic": topic, "audience": audience})
        tabs = st.tabs(["Research", "Brief", "Draft", "Quality"])
        with tabs[0]:
            st.json(result.get("research_packet", {}))
        with tabs[1]:
            st.json(result.get("content_brief", {}))
        with tabs[2]:
            st.json(result.get("draft", {}))
        with tabs[3]:
            st.json(result.get("quality_report", {}))


if __name__ == "__main__":
    run()
