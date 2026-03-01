from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.strategist import strategist_node
from app.models import ContentBrief
from integrations.llm_openai import OpenAIClient


def test_strategist_node_returns_valid_brief(monkeypatch):
    def fake_complete_json(self, system: str, user: str, temperature: float = 0.0, max_retries: int = 1):
        return {
            "topic": "AI content marketing",
            "audience": "B2B marketing leaders",
            "objective": "Build authority",
            "channel": "linkedin",
            "angle": "Turn research into repeatable editorial decisions",
            "outline": [
                "Start with the market problem",
                "Explain the workflow gap",
                "Show where research improves decisions",
                "Describe the content planning benefit",
                "Invite teams to test a repeatable process",
            ],
            "cta": "What are your thoughts?",
        }

    monkeypatch.setattr(OpenAIClient, "complete_json", fake_complete_json)

    result = strategist_node(
        {
            "user_query": "AI content marketing",
            "platform": "linkedin",
            "research": {
                "user_query": "AI content marketing",
                "search_queries": ["AI content marketing", "AI content marketing best practices"],
                "sources": [
                    {
                        "title": "Source one",
                        "url": "https://example.com/source-one",
                        "snippet": "Snippet one",
                        "retrieved_at": "2025-01-01T00:00:00+00:00",
                        "source_type": "serp",
                    }
                ],
                "key_findings": [
                    "Finding one",
                    "Finding two",
                    "Finding three",
                ],
                "angles": [
                    "Operational angle",
                    "Authority angle",
                ],
                "stats_or_quotes": [],
                "citations": [
                    {
                        "url": "https://example.com/source-one",
                        "supporting_claim": "Claim one",
                        "source_title": "Source one",
                    }
                ],
            },
        }
    )

    assert "brief" in result
    brief = ContentBrief.model_validate(result["brief"])
    assert len(brief.outline) >= 3
    assert brief.channel == "linkedin"
