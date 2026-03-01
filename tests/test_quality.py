from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.quality import quality_node


def test_quality_passes_strong_checks():
    result = quality_node(
        {
            "research": {
                "user_query": "AI content marketing",
                "search_queries": ["AI content marketing", "AI content marketing best practices"],
                "sources": [],
                "key_findings": [],
                "angles": [],
                "stats_or_quotes": [],
                "citations": [
                    {
                        "url": "https://example.com/source-one",
                        "supporting_claim": "Claim one",
                        "source_title": "Source one",
                    }
                ],
            },
            "constraints": {"max_words": 40},
            "draft": {
                "channel": "linkedin",
                "headline": "Stable LinkedIn post",
                "body": (
                    "This draft uses a clear first paragraph.\n\n"
                    "It adds a second paragraph for better scanning.\n\n"
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
        }
    )
    assert result["quality_report"]["status"] == "pass"
    assert result["quality_report"]["checks"]["headline_len_ok"] is True
    assert result["quality_report"]["checks"]["cta_present"] is True


def test_quality_fails_for_missing_citation_use():
    result = quality_node(
        {
            "research": {
                "user_query": "AI content marketing",
                "search_queries": [],
                "sources": [],
                "key_findings": [],
                "angles": [],
                "stats_or_quotes": [],
                "citations": [
                    {
                        "url": "https://example.com/source-one",
                        "supporting_claim": "Claim one",
                        "source_title": "Source one",
                    }
                ],
            },
            "draft": {
                "channel": "linkedin",
                "headline": "Stable LinkedIn post",
                "body": "Paragraph one.\n\nParagraph two.\n\nBook a short strategy call today.",
                "cta": "Book a short strategy call today.",
                "citations": [],
            }
        }
    )
    assert result["quality_report"]["status"] == "fail"
    assert "Draft does not use any research citations." in result["quality_report"]["reasons"]
    assert "Reuse at least one citation from the research packet." in result["quality_report"]["fixes"]


def test_quality_fails_word_limit_headline_and_cta_checks():
    result = quality_node(
        {
            "research": {
                "user_query": "AI content marketing",
                "search_queries": [],
                "sources": [],
                "key_findings": [],
                "angles": [],
                "stats_or_quotes": [],
                "citations": [
                    {
                        "url": "https://example.com/source-one",
                        "supporting_claim": "Claim one",
                        "source_title": "Source one",
                    }
                ],
            },
            "constraints": {"max_words": 3},
            "draft": {
                "channel": "linkedin",
                "headline": "This headline is definitely much too long for LinkedIn content marketing posts today",
                "body": "Too many words live here without the call to action.",
                "cta": "Book a short strategy call today.",
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
    assert result["quality_report"]["status"] == "fail"
    assert "Draft exceeds the maximum word limit." in result["quality_report"]["reasons"]
    assert "Headline exceeds 12 words." in result["quality_report"]["reasons"]
    assert "CTA is missing from the draft body." in result["quality_report"]["reasons"]
    assert "Draft is not skimmable enough for LinkedIn." in result["quality_report"]["reasons"]
