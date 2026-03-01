from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.research import research_node
from app.models import ResearchPacket
from integrations.llm_openai import OpenAIClient
from integrations.serp import SerpClient


def test_research_node_uses_llm_payload(monkeypatch):
    def fake_search(self, query: str, num_results: int = 10, timeout_s: int = 20, hl: str = "en", gl: str = "us"):
        return [
            {
                "title": "Source one",
                "url": "https://example.com/one",
                "snippet": "Snippet one",
            },
            {
                "title": "Source two",
                "url": "https://example.com/two",
                "snippet": "Snippet two",
            },
        ]

    def fake_complete_json(self, system: str, user: str, temperature: float = 0.0, max_retries: int = 1):
        return {
            "key_findings": ["LLM finding 1", "LLM finding 2"],
            "angles": ["LLM angle 1"],
            "stats_or_quotes": ["LLM stat"],
            "citations": [
                {
                    "url": "https://example.com/one",
                    "supporting_claim": "Supported claim",
                },
                {
                    "url": "https://example.com/not-in-sources",
                    "supporting_claim": "Should be dropped",
                },
            ],
        }

    monkeypatch.setattr(SerpClient, "search", fake_search)
    monkeypatch.setattr(OpenAIClient, "complete_json", fake_complete_json)

    result = research_node({"user_query": "AI content marketing"})

    packet = ResearchPacket.model_validate(result["research"])
    source_urls = {source.url for source in packet.sources}

    assert packet.key_findings == ["LLM finding 1", "LLM finding 2"]
    assert packet.stats_or_quotes == ["LLM stat"]
    assert packet.citations
    assert all(citation.url in source_urls for citation in packet.citations)
