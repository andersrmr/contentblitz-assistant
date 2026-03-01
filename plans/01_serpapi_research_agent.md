# Step 2 — SerpAPI Integration + Research Agent (No LLM Yet)

## Goal

Implement real SerpAPI search integration and a research agent that builds a valid `ResearchPacket`, while keeping the system deterministic and testable without any LLM calls.

## Scope

- SerpAPI integration only
- No OpenAI or other LLM calls in this step
- Deterministic placeholder values for findings, angles, and citation claims

## Acceptance Criteria

- `uv run pytest -q` passes without any API keys set
- Unit tests mock `requests` and make no real network calls
- `ResearchPacket` validates successfully via Pydantic
- Research outputs are deterministic and schema-valid

## Commands to Run

- `uv run pytest -q`
- `uv run streamlit run src/ui/streamlit_app.py`

## Notes

- Deduplicate sources by URL and keep the first occurrence
- Every agent output must remain schema-valid JSON produced via Pydantic validation
