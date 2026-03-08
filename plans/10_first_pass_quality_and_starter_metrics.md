# Step 11 — First-Pass Quality Snapshot + Starter Metrics

## 1) Goal
Add first-pass quality capture and a small high-value starter metric set so eval runs show not only final success, but also whether the first draft passed, whether rewrite was triggered, and what first-pass failures were most common.

## 2) Scope
- Preserve `first_quality_report` on the first execution of `quality_node`.
- Keep `quality_report` as the latest/final quality result.
- Extend `compute_case_metrics()` to include:
  - `first_quality_pass`
  - `final_quality_pass`
  - `rewrite_triggered`
  - `rewrite_recovered`
  - `rewrite_count`
  - `first_failure_reasons`
- Extend `compute_aggregate()` to include:
  - `final_pass_rate`
  - `first_pass_pass_rate`
  - `rewrite_trigger_rate`
  - `rewrite_recovery_rate`
  - `avg_rewrite_count`
  - `first_pass_failure_reason_counts`
- Keep existing final-state compliance metrics unless removal is necessary.
- Do not yet add tone / brand voice / genericity checks in this step.

## 3) Architectural Rationale
Current metrics are final-state only. That hides whether the writer passed on first attempt and what the rewrite loop actually contributed. Preserving `first_quality_report` creates a minimal trajectory-aware eval design without adding full history tracking.

## 4) Acceptance Criteria
- `quality_node` stores `first_quality_report` only on the first quality pass.
- Final/latest `quality_report` still behaves as before.
- Case metrics expose first-pass and rewrite-recovery fields.
- Aggregate report exposes the 6 starter metrics.
- Existing golden suite still runs successfully.
- `uv run pytest -q` passes offline.

## 5) Commands
- `uv run pytest -q`
- `uv run python -m evals.harness --suite golden --outdir evals/results`
