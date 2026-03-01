# Step 3 — OpenAI Research Summarization (JSON Enforced)

## Goal

Add OpenAI-backed research summarization that returns strictly parsed JSON for the research agent, while preserving deterministic offline tests.

## Scope

- OpenAI is used only for research summarization
- Strategist and writer agents remain unchanged in this step

## Acceptance Criteria

- `complete_json` returns a valid `dict`, and invalid JSON triggers a repair retry
- The research node uses OpenAI output when available and falls back safely otherwise
- Unit tests pass offline, and any real-API integration test is marked and optional

## Commands

- `uv run pytest -q`
- `uv run pytest -q -m integration` (optional)
