import requests


from app.config import Settings


class SerpApiError(RuntimeError):
    pass


def dedupe_urls(results: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    deduped: list[dict[str, str]] = []
    for result in results:
        url = result.get("url", "")
        if not url or url in seen:
            continue
        seen.add(url)
        deduped.append(result)
    return deduped


class SerpClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key if api_key is not None else Settings().SERPAPI_API_KEY
        self.base_url = "https://serpapi.com/search.json"

    def search(
        self,
        query: str,
        num_results: int = 10,
        timeout_s: int = 20,
        hl: str = "en",
        gl: str = "us",
    ) -> list[dict[str, str]]:
        params = {
            "q": query,
            "engine": "google",
            "api_key": self.api_key,
            "num": num_results,
            "hl": hl,
            "gl": gl,
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=timeout_s)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise SerpApiError(f"SerpAPI request failed: {exc}") from exc

        payload = response.json()
        if payload.get("error"):
            raise SerpApiError(str(payload["error"]))

        organic_results = payload.get("organic_results", [])
        normalized = [
            {
                "title": item.get("title", "") or "",
                "url": item.get("link", "") or "",
                "snippet": item.get("snippet", "") or "",
            }
            for item in organic_results
        ]
        return dedupe_urls(normalized)
