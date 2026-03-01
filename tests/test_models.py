from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from app.models import ContentBrief, Draft, QualityReport, ResearchPacket


def test_research_packet_model_round_trip():
    packet = ResearchPacket.model_validate(
        {
            "user_query": "AI content marketing",
            "search_queries": ["AI content marketing", "AI content marketing best practices"],
            "sources": [
                {
                    "title": "Source one",
                    "url": "https://example.com/source-one",
                    "snippet": "Summary one",
                    "retrieved_at": "2025-01-01T00:00:00+00:00",
                    "source_type": "serp",
                }
            ],
            "key_findings": ["One", "Two"],
            "angles": ["Angle one"],
            "stats_or_quotes": [],
            "citations": [
                {
                    "source_title": "Source one",
                    "source_url": "https://example.com/source-one",
                    "supporting_claim": "Claim one",
                }
            ],
        }
    )
    dumped = packet.model_dump()
    assert dumped["user_query"] == "AI content marketing"
    assert dumped["sources"][0]["title"] == "Source one"


def test_draft_and_quality_models_validate():
    brief = ContentBrief.model_validate(
        {
            "topic": "AI content marketing",
            "audience": "B2B marketers",
            "objective": "Educate",
            "channel": "linkedin",
            "angle": "Use a repeatable workflow",
            "outline": ["Pain", "Process", "CTA"],
            "cta": "Book a call.",
        }
    )
    draft = Draft.model_validate(
        {
            "channel": "linkedin",
            "headline": "Repeatable content workflow",
            "body": "A stable body for the test.",
            "cta": brief.cta,
            "citations": [],
        }
    )
    report = QualityReport.model_validate(
        {
            "passed": True,
            "score": 100,
            "checks": {"min_length": True, "cta_present": True},
            "feedback": [],
        }
    )
    assert draft.cta == "Book a call."
    assert report.score == 100
