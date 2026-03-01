# Step 7 — Remove content_brief Alias

## Goal

Simplify the state schema and avoid duplicate brief keys.

## Changes

- Strategist returns only `brief`
- UI reads `brief` only
- State schema removes `content_brief`

## Acceptance Criteria

- `brief` appears in the UI
- Tests pass
- No references to `content_brief` remain

## Commands

- `uv run pytest -q`
- `uv run streamlit run src/ui/streamlit_app.py`
