from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from integrations.serp import SerpClient


class _FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self._payload


def test_serp_client_normalizes_results(monkeypatch):
    def fake_get(url: str, params: dict, timeout: int):
        assert url == "https://serpapi.com/search.json"
        assert params["q"] == "ai content"
        assert params["num"] == 5
        assert timeout == 7
        return _FakeResponse(
            {
                "organic_results": [
                    {
                        "title": "Result one",
                        "link": "https://example.com/one",
                        "snippet": "Snippet one",
                    },
                    {
                        "link": "https://example.com/two",
                    },
                    {
                        "title": "Duplicate",
                        "link": "https://example.com/one",
                        "snippet": "Ignored",
                    },
                ]
            }
        )

    monkeypatch.setattr("integrations.serp.requests.get", fake_get)
    client = SerpClient(api_key="test-key")

    results = client.search("ai content", num_results=5, timeout_s=7)

    assert results == [
        {
            "title": "Result one",
            "url": "https://example.com/one",
            "snippet": "Snippet one",
        },
        {
            "title": "",
            "url": "https://example.com/two",
            "snippet": "",
        },
    ]
