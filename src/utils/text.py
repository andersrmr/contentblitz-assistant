def contains_cta(text: str) -> bool:
    lowered = text.lower()
    return "book" in lowered or "call" in lowered
