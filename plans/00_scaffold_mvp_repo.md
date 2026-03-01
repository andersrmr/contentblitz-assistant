# Step 1 — Scaffold MVP Repo

## 1) Goal

Scaffold a minimal runnable MVP structure for the AI Content Marketing Assistant using LangGraph, with stub agents that return schema-valid JSON and passing unit tests.

## 2) File Structure

Expected directories and files:

- `src/app`: `config.py`, `state.py`, `models.py`
- `src/app/prompts/*`
- `src/integrations`: `llm_openai.py`, `serp.py`
- `src/agents`: `router.py`, `research.py`, `strategist.py`, `writer_linkedin.py`, `quality.py`, `rewrite.py`
- `src/workflow`: `graph.py`, `routing.py`
- `src/ui`: `streamlit_app.py`
- `src/utils/*`
- `tests/*`
- `plans/`

## 3) Acceptance Criteria

- LangGraph graph compiles successfully.
- Stub agents return deterministic outputs.
- All agent outputs validate against Pydantic models.
- `uv run pytest -q` passes.
- `streamlit run src/ui/streamlit_app.py` launches without error.
- State is passed cleanly between nodes.
- No real API calls yet (OpenAI and SerpAPI are stubbed).

## 4) Commands to Run

- `uv run pytest -q`
- `uv run streamlit run src/ui/streamlit_app.py`

## 5) Notes

- Every agent must return schema-valid JSON via Pydantic validation.
- No extra agents or features beyond the defined MVP scaffold.
- Keep implementation minimal and deterministic.
