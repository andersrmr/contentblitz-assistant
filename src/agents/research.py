from app.models import ResearchPacket
from app.prompts import RESEARCH_PROMPT
from app.state import AppState
from integrations.llm_openai import render_stub_completion
from integrations.serp import fetch_stub_sources


def research_node(state: AppState) -> dict:
    topic = state.get("topic", "AI content marketing")
    audience = state.get("audience", "B2B marketers")
    sources, citations = fetch_stub_sources(topic)
    packet_data = {
        "topic": topic,
        "audience": audience,
        "summary": render_stub_completion("research", topic, audience),
        "key_points": [
            f"{topic} reduces content bottlenecks.",
            f"{topic} helps teams maintain message consistency.",
            RESEARCH_PROMPT,
        ],
        "sources": [source.model_dump() for source in sources],
        "citations": [citation.model_dump() for citation in citations],
    }
    packet = ResearchPacket.model_validate(packet_data)
    return {"research_packet": packet.model_dump()}
