from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.writer_linkedin import writer_linkedin_node
from app.models import Draft
from integrations.llm_openai import OpenAIClient


def test_writer_linkedin_node_returns_valid_draft(monkeypatch):
    def fake_complete_json(self, system: str, user: str, temperature: float = 0.0, max_retries: int = 1):
        return {
            "channel": "linkedin",
            "headline": "A better way to ship content",
            "body": (
                "Most teams do not need more ideas.\n\n"
                "They need a repeatable system for research and production.\n\n"
                "Book a short strategy call to compare your current workflow."
            ),
            "cta": "Book a short strategy call to compare your current workflow.",
            "citations": [
                {
                    "url": "https://example.com/source-one",
                    "supporting_claim": "Claim one",
                    "source_title": "Source one",
                }
            ],
        }

    monkeypatch.setattr(OpenAIClient, "complete_json", fake_complete_json)

    result = writer_linkedin_node(
        {
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
                "key_findings": ["Finding one", "Finding two"],
                "angles": ["Operational angle"],
                "stats_or_quotes": [],
                "citations": [
                    {
                        "url": "https://example.com/source-one",
                        "supporting_claim": "Claim one",
                        "source_title": "Source one",
                    }
                ],
            },
            "brief": {
                "topic": "AI content marketing",
                "audience": "B2B marketers",
                "objective": "Educate",
                "channel": "linkedin",
                "angle": "Use a repeatable workflow",
                "outline": [
                    "Start with the core problem",
                    "Show the operational gap",
                    "Explain the workflow advantage",
                ],
                "cta": "Book a short strategy call to compare your current workflow.",
            },
        }
    )

    assert "draft" in result
    draft = Draft.model_validate(result["draft"])
    research_urls = {"https://example.com/source-one"}
    assert draft.body
    assert draft.cta in draft.body
    assert all(citation.url in research_urls for citation in draft.citations)
