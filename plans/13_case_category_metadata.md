# Step 14 — Case Category Metadata for Eval Reporting

## 1) Goal
Add a simple optional `category` field to eval cases so reports can label each case by scenario type (for example: happy_path, citation, formatting, tone, brand_voice, specificity).

## 2) Scope
- Add optional `category` to the `EvalCase` schema.
- Include category in per-case harness output.
- Show category in the markdown case table.
- Add top-level category metadata to all 9 golden YAML cases.
- Do not yet compute category-level aggregates in this step.

## 3) Architectural Rationale
Current reports show per-case results but do not label scenario type in a structured way. Adding `category` improves report readability now and prepares the framework for future category-level metrics and grouped analysis.

## 4) Category Mapping
Use these categories for the current golden suite:
- `case_001_create_happy_path` -> `happy_path`
- `case_002_citation_filtering` -> `citation`
- `case_003_cta_recovery` -> `formatting`
- `case_004_skim_recovery` -> `formatting`
- `case_005_headline_recovery` -> `formatting`
- `case_006_revise_path` -> `rewrite_flow`
- `case_007_tone_violation_rewrite` -> `tone`
- `case_008_brand_voice_mismatch` -> `brand_voice`
- `case_009_generic_content_detection` -> `specificity`

## 5) Acceptance Criteria
- `EvalCase` supports optional category metadata.
- Harness output includes category for each case.
- Markdown report shows a category column.
- All 9 golden YAML cases include category at top level.
- `uv run pytest -q` passes offline.
- `uv run python -m evals.harness --suite golden --outdir evals/results` runs successfully.

## 6) Commands
- `uv run pytest -q`
- `uv run python -m evals.harness --suite golden --outdir evals/results`
