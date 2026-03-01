from datetime import datetime, timezone

from app.models import Citation, ResearchPacket, Source
from app.state import AppState
from integrations.serp import SerpClient


def _build_search_queries(user_query: str) -> list[str]:
    base = user_query.strip() or "AI content marketing"
    return [
        base,
        f"{base} best practices",
        f"{base} case studies",
    ]


def _retrieved_at() -> str:
    return datetime.now(timezone.utc).isoformat()


def research_node(state: AppState) -> dict:
    user_query = state.get("user_query") or state.get("topic", "AI content marketing")
    search_queries = _build_search_queries(user_query)
    client = SerpClient()
    raw_results: list[dict[str, str]] = []
    for query in search_queries[:2]:
        raw_results.extend(client.search(query=query, num_results=5))

    deduped_sources: list[Source] = []
    seen_urls: set[str] = set()
    for result in raw_results:
        url = result.get("url", "")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        deduped_sources.append(
            Source.model_validate(
                {
                    "title": result.get("title", ""),
                    "url": url,
                    "snippet": result.get("snippet", ""),
                    "retrieved_at": _retrieved_at(),
                    "source_type": "serp",
                }
            )
        )
        if len(deduped_sources) >= 12:
            break

    sources = deduped_sources[:12]
    citations = [
        Citation.model_validate(
            {
                "source_title": source.title,
                "source_url": source.url,
                "supporting_claim": f"Supporting claim {index + 1} from source review.",
            }
        )
        for index, source in enumerate(sources[:3])
    ]
    packet_data = {
        "user_query": user_query,
        "search_queries": search_queries,
        "sources": [source.model_dump() for source in sources],
        "key_findings": [
            "Finding 1 (from sources)",
            "Finding 2 (from sources)",
            "Finding 3 (from sources)",
        ],
        "angles": [
            "Operational efficiency angle",
            "Content consistency angle",
        ],
        "stats_or_quotes": [],
        "citations": [citation.model_dump() for citation in citations],
    }
    packet = ResearchPacket.model_validate(packet_data)
    return {"research": packet.model_dump()}
