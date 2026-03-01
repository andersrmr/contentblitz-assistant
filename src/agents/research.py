import json
from datetime import datetime, timezone

from app.prompts import RESEARCH_SYSTEM, RESEARCH_USER_TEMPLATE
from app.models import Citation, ResearchPacket, Source
from app.state import AppState
from integrations.llm_openai import LLMError, OpenAIClient
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


def _fallback_payload(sources: list[Source]) -> dict:
    citations = [
        {
            "url": source.url,
            "supporting_claim": f"Supporting claim {index + 1} from source review.",
        }
        for index, source in enumerate(sources[:3])
    ]
    return {
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
        "citations": citations,
    }


def _render_source_context(sources: list[Source]) -> str:
    return json.dumps(
        [
            {
                "title": source.title,
                "url": source.url,
                "snippet": source.snippet,
            }
            for source in sources
        ],
        indent=2,
    )


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
    payload = _fallback_payload(sources)
    errors = list(state.get("errors", []))
    meta = dict(state.get("meta", {}))

    try:
        llm_payload = OpenAIClient().complete_json(
            system=RESEARCH_SYSTEM,
            user=RESEARCH_USER_TEMPLATE.format(
                user_query=user_query,
                search_queries="\n".join(f"- {query}" for query in search_queries),
                sources=_render_source_context(sources),
            ),
        )
        if isinstance(llm_payload, dict):
            payload = {**payload, **llm_payload}
    except LLMError as exc:
        errors.append(f"Research summarization fallback used: {exc}")
        meta["research_fallback"] = "deterministic_placeholders"

    source_index = {source.url: source for source in sources}
    citations: list[Citation] = []
    for citation_data in payload.get("citations", []):
        url = citation_data.get("url", "")
        if url not in source_index:
            continue
        citations.append(
            Citation.model_validate(
                {
                    "url": url,
                    "supporting_claim": citation_data.get("supporting_claim", ""),
                    "source_title": source_index[url].title,
                }
            )
        )

    packet_data = {
        "user_query": user_query,
        "search_queries": search_queries,
        "sources": [source.model_dump() for source in sources],
        "key_findings": payload.get("key_findings", []),
        "angles": payload.get("angles", []),
        "stats_or_quotes": payload.get("stats_or_quotes", []),
        "citations": [citation.model_dump() for citation in citations],
    }
    packet = ResearchPacket.model_validate(packet_data)
    result = {"research": packet.model_dump()}
    if errors:
        result["errors"] = errors
    if meta:
        result["meta"] = meta
    return result
