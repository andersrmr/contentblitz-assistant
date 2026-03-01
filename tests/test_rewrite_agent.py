from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.rewrite import rewrite_node
from app.models import Draft
from integrations.llm_openai import OpenAIClient


def test_rewrite_node_returns_valid_draft(monkeypatch):
    def fake_complete_json(self, system: str, user: str, temperature: float = 0.0, max_retries: int = 1):
        return {
            "channel": "linkedin",
            "headline": "Refined workflow for better output",
            "body": (
                "A tighter process helps teams move faster.\n\n"
                "It also keeps messaging more consistent.\n\n"
                "Book a short strategy call today."
            ),
            "cta": "Book a short strategy call today.",
            "citations": [
                {
                    "url": "https://example.com/source-one",
                    "supporting_claim": "Claim one",
                    "source_title": "Source one",
                }
            ],
        }

    monkeypatch.setattr(OpenAIClient, "complete_json", fake_complete_json)

    result = rewrite_node(
        {
            "revision_request": "Make it tighter and more skimmable.",
            "research": {
                "user_query": "AI content marketing",
                "search_queries": [],
                "sources": [],
                "key_findings": [],
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
                "angle": "Operational angle",
                "outline": ["Point one", "Point two", "Point three"],
                "cta": "Book a short strategy call today.",
            },
            "draft": {
                "channel": "linkedin",
                "headline": "Original draft headline",
                "body": "Old paragraph.",
                "cta": "Book a short strategy call today.",
                "citations": [],
            },
            "quality_report": {
                "status": "fail",
                "reasons": ["Draft is not skimmable enough for LinkedIn."],
                "fixes": ["Use at least three short paragraphs separated by blank lines."],
                "checks": {"skim_ok": False},
            },
        }
    )

    draft = Draft.model_validate(result["draft"])
    allowed_urls = {"https://example.com/source-one"}
    assert all(citation.url in allowed_urls for citation in draft.citations)
    assert result["rewrite_count"] == 1
