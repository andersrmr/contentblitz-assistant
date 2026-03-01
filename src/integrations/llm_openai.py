def render_stub_completion(prompt_name: str, topic: str, audience: str) -> str:
    return (
        f"{prompt_name} response for {topic} aimed at {audience}. "
        "This is deterministic stub content for local tests."
    )
