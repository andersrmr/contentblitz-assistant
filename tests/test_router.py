from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.router import router_node
from integrations.llm_openai import OpenAIClient
from integrations.serp import SerpClient
from workflow.graph import content_marketing_graph


def test_router_sets_linkedin_route():
    result = router_node({"topic": "AI content marketing"})
    assert result["route"] == "linkedin_post"
    assert result["rewrite_count"] == 0


def test_graph_runs_through_quality_pass(monkeypatch):
    def fake_search(self, query: str, num_results: int = 10, timeout_s: int = 20, hl: str = "en", gl: str = "us"):
        return [
            {
                "title": f"{query} source 1",
                "url": "https://example.com/source-1",
                "snippet": "Snippet 1",
            },
            {
                "title": f"{query} source 2",
                "url": "https://example.com/source-2",
                "snippet": "Snippet 2",
            },
        ]

    def fake_complete_json(self, system: str, user: str, temperature: float = 0.0, max_retries: int = 1):
        if "content strategist" in system.lower():
            return {
                "topic": "AI content marketing",
                "audience": "B2B marketers",
                "objective": "Educate",
                "channel": "linkedin",
                "angle": "Show how a structured workflow improves execution",
                "outline": [
                    "Open with the operational problem",
                    "Explain how research reduces ambiguity",
                    "Show how strategy creates consistency",
                    "Connect the workflow to better publishing",
                    "Invite readers to compare approaches",
                ],
                "cta": "Book a short strategy call to compare approaches.",
            }
        return {
            "key_findings": ["LLM finding"],
            "angles": ["LLM angle"],
            "stats_or_quotes": [],
            "citations": [
                {
                    "url": "https://example.com/source-1",
                    "supporting_claim": "Claim from source 1",
                }
            ],
        }

    monkeypatch.setattr(SerpClient, "search", fake_search)
    monkeypatch.setattr(OpenAIClient, "complete_json", fake_complete_json)
    result = content_marketing_graph.invoke(
        {"topic": "AI content marketing", "audience": "B2B marketers"}
    )
    assert result["route"] == "linkedin_post"
    assert result["quality_report"]["passed"] is True
