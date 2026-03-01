from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from integrations.llm_openai import OpenAIClient


def test_complete_json_strips_fences(monkeypatch):
    responses = iter(['```json\n{"key":"value"}\n```'])

    def fake_request_text(self, system: str, user: str, temperature: float) -> str:
        return next(responses)

    monkeypatch.setattr(OpenAIClient, "_request_text", fake_request_text)
    client = OpenAIClient(api_key=None)

    payload = client.complete_json("system", "user")

    assert payload == {"key": "value"}


def test_complete_json_repairs_after_parse_failure(monkeypatch):
    responses = iter(["not json", '{"fixed": true}'])

    def fake_request_text(self, system: str, user: str, temperature: float) -> str:
        return next(responses)

    monkeypatch.setattr(OpenAIClient, "_request_text", fake_request_text)
    client = OpenAIClient(api_key=None)

    payload = client.complete_json("system", "user", max_retries=1)

    assert payload == {"fixed": True}
