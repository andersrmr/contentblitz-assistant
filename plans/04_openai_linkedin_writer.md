# Step 5 — OpenAI LinkedIn Writer (Schema-Aligned Draft)

## Goal

Implement an OpenAI-backed LinkedIn writer that returns a schema-valid `Draft` while preserving deterministic offline tests.

## Required Draft JSON Shape

The model must return JSON only with:

- `channel`
- `headline`
- `body`
- `cta`
- `citations`

## Acceptance Criteria

- `Draft` validates successfully
- Citation URLs are reused from research and not invented
- Offline tests pass with no real network calls
- Deterministic fallback works when the LLM fails

## Commands to Run

- `uv run pytest -q`
- `uv run streamlit run src/ui/streamlit_app.py`
