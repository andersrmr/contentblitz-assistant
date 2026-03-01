# Step 4 — OpenAI Strategist Brief (Schema-Aligned)

## Goal

Implement an OpenAI-backed strategist agent that returns a schema-valid content brief aligned with the existing `ContentBrief` model.

## Scope

- Strategist only
- Writer remains unchanged in this step

## Required JSON Shape

The model must return JSON only with keys matching `ContentBrief`:

- `topic`
- `audience`
- `objective`
- `channel`
- `angle`
- `outline`
- `cta`

## Acceptance Criteria

- `brief` validates against `ContentBrief`
- Deterministic fallback works when the LLM fails
- Tests pass offline with no real OpenAI calls

## Commands to Run

- `uv run pytest -q`
- `uv run streamlit run src/ui/streamlit_app.py`
