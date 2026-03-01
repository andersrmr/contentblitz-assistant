from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.research import research_node
from app.models import ResearchPacket
from integrations.llm_openai import LLMError, OpenAIClient
from integrations.serp import SerpClient


def test_research_node_builds_valid_deduped_packet(monkeypatch):
    def fake_search(self, query: str, num_results: int = 10, timeout_s: int = 20, hl: str = "en", gl: str = "us"):
        return [
            {
                "title": f"{query} source 1",
                "url": "https://example.com/shared",
                "snippet": "Shared source",
            },
            {
                "title": f"{query} source 2",
                "url": f"https://example.com/{query.replace(' ', '-')}",
                "snippet": "Unique source",
            },
        ]

    def fake_complete_json(self, system: str, user: str, temperature: float = 0.0, max_retries: int = 1):
        raise LLMError("forced fallback")

    monkeypatch.setattr(SerpClient, "search", fake_search)
    monkeypatch.setattr(OpenAIClient, "complete_json", fake_complete_json)

    result = research_node({"user_query": "AI content marketing"})

    assert "research" in result
    packet = ResearchPacket.model_validate(result["research"])
    assert len(packet.search_queries) >= 2
    assert len(packet.sources) == 3
    assert len({source.url for source in packet.sources}) == len(packet.sources)
    assert result["meta"]["research_fallback"] == "deterministic_placeholders"
    assert result["errors"]
