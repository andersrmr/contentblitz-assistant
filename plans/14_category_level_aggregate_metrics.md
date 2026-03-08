# Step 15 — Category-Level Aggregate Metrics

## 1) Goal
Add category-level aggregate reporting so eval runs summarize performance by scenario type, not just overall totals.

## 2) Scope
- Keep the existing top-level aggregate metrics unchanged.
- Add category-level aggregates for:
  - `final_pass_rate`
  - `first_pass_pass_rate`
  - `rewrite_trigger_rate`
  - `rewrite_recovery_rate`
- Use each case's top-level category metadata already carried into harness results.
- Include category-level metrics in `latest.json`.
- Add a "Metrics by Category" section to `latest.md`.
- Do not yet add tags or multi-label grouping in this step.

## 3) Architectural Rationale
Now that each case has a structured category, the report should show grouped performance by scenario type. This makes it easier to understand where the system is strong or weak, such as formatting vs tone vs specificity, without changing the underlying test logic.

## 4) Reporting Design
JSON:
- Add `aggregate.by_category` shaped like:
  - `by_category:`
  - `<category_name>:`
  - `final_pass_rate: ...`
  - `first_pass_pass_rate: ...`
  - `rewrite_trigger_rate: ...`
  - `rewrite_recovery_rate: ...`

Markdown:
- Add a "Metrics by Category" section after the overall aggregate summary.
- Render a table with columns:
  - `Category | Final Pass | First-Pass Pass | Rewrite Trigger | Rewrite Recovery`
- Sort rows alphabetically by category name.

## 5) Metric Semantics
- `final_pass_rate`: percent of cases in category with `final_quality_pass = true`.
- `first_pass_pass_rate`: percent of cases in category with `first_quality_pass = true`.
- `rewrite_trigger_rate`: percent of cases in category with `rewrite_triggered = true`.
- `rewrite_recovery_rate`: among rewritten cases in the category, percent with `rewrite_recovered = true`.
- If a category has no rewritten cases, `rewrite_recovery_rate` should be `0.0`.

## 6) Acceptance Criteria
- Overall aggregate metrics remain available and unchanged.
- `aggregate.by_category` exists in `latest.json`.
- `latest.md` includes a "Metrics by Category" section.
- All 9 golden cases still pass.
- `uv run pytest -q` passes offline.
- `uv run python -m evals.harness --suite golden --outdir evals/results` runs successfully.

## 7) Commands
- `uv run pytest -q`
- `uv run python -m evals.harness --suite golden --outdir evals/results`
