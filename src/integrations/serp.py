from app.models import Citation, Source


def fetch_stub_sources(topic: str) -> tuple[list[Source], list[Citation]]:
    sources = [
        Source(
            title=f"{topic} benchmark report",
            url=f"https://example.com/{topic.lower().replace(' ', '-')}-benchmark",
            summary=f"A stable benchmark summary for {topic}.",
        ),
        Source(
            title=f"{topic} implementation guide",
            url=f"https://example.com/{topic.lower().replace(' ', '-')}-guide",
            summary=f"A stable implementation guide for {topic}.",
        ),
    ]
    citations = [
        Citation(
            source_title=source.title,
            source_url=source.url,
            note=f"Referenced for {topic}.",
        )
        for source in sources
    ]
    return sources, citations
