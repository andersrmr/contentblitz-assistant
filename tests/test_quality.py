from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.quality import quality_node


def test_quality_passes_stub_draft():
    result = quality_node(
        {
            "draft": {
                "channel": "linkedin",
                "headline": "Stable post",
                "body": "This draft is deliberately long enough to satisfy the minimum length check for the test suite.",
                "cta": "Book a short strategy call today.",
                "citations": [],
            }
        }
    )
    assert result["quality_report"]["passed"] is True
    assert result["quality_report"]["checks"]["min_length"] is True
    assert result["quality_report"]["checks"]["cta_present"] is True


def test_quality_fails_without_cta():
    result = quality_node(
        {
            "draft": {
                "channel": "linkedin",
                "headline": "Stable post",
                "body": "This draft is deliberately long enough to satisfy the minimum length check for the test suite.",
                "cta": "Reach out sometime.",
                "citations": [],
            }
        }
    )
    assert result["quality_report"]["passed"] is False
    assert result["quality_report"]["checks"]["cta_present"] is False
