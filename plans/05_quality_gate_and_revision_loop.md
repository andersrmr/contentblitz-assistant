# Step 6 — Quality Gate + Revision Loop

## 1) Goal

Strengthen the quality gate and make the revision loop reliable, while keeping behavior deterministic in tests.

## 2) Scope

- `QualityReport` contract with `status`, `reasons`, `fixes`, and `checks`
- Deterministic heuristic quality checks
- OpenAI-backed rewrite with deterministic fallback
- `revise` intent routing
- Loop until `MAX_ITERATIONS`

## 3) Quality Checks Implemented

- citations present
- citations used
- max_words
- headline length
- CTA present in body
- LinkedIn skimmability

## 4) Acceptance Criteria

- Quality report validates with `status` / `reasons` / `fixes` / `checks`
- Rewrite returns schema-valid `Draft` JSON and does not invent citation URLs
- `revise` intent routes correctly
- The loop runs up to `MAX_ITERATIONS`
- `uv run pytest -q` passes offline

## 5) Notes

- Post-processing enforces CTA-in-body and LinkedIn skimmability deterministically after rewrite.

## 6) Commands

- `uv run pytest -q`
- `uv run streamlit run src/ui/streamlit_app.py`
