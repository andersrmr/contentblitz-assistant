from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from app.config import Settings, settings


def test_settings_load_from_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("SERPAPI_API_KEY", "test-serp-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-test")

    loaded = Settings()

    assert loaded.OPENAI_API_KEY == "test-openai-key"
    assert loaded.SERPAPI_API_KEY == "test-serp-key"
    assert loaded.OPENAI_MODEL == "gpt-test"


def test_settings_singleton_exposes_expected_fields():
    assert hasattr(settings, "OPENAI_API_KEY")
    assert hasattr(settings, "SERPAPI_API_KEY")
    assert hasattr(settings, "OPENAI_MODEL")
