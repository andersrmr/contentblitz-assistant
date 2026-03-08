# Step 19 — Single-Case Flag for Eval Harness

## 1) Goal
Add a simple `--case` flag to the eval harness so a developer can run one specific eval case directly instead of always running the full suite.

## 2) Scope
- Extend CLI parsing in `evals/harness.py` to accept an optional:
  - `--case <case_id>`
- Keep existing `--suite` behavior intact.
- When `--case` is provided:
  - load the suite manifest/case list as usual
  - select the matching case by `case_id`
  - run only that one case
  - still generate `latest.json` and `latest.md` output in the same output directory
- Preserve aggregate output shape for a single-case run.
- If the `case_id` is not found in the selected suite, raise a clear error message.
- Do not change case execution semantics, metrics logic, or report rendering in this step.

## 3) Architectural Rationale
During development, it is common to iterate on one failing or weak eval case repeatedly before rerunning the full suite. A single-case harness flag makes the local development loop faster and reduces friction while preserving the full-suite regression workflow.

## 4) CLI Design
Add optional flag:
- `--case`

Examples:
- `uv run python -m evals.harness --suite golden --case case_007_tone_violation_rewrite --outdir evals/results`
- `uv run python -m evals.harness --suite golden --outdir evals/results`

Behavior:
- Without `--case`: run all cases in the suite.
- With `--case`: run only the matching case in the chosen suite.

## 5) Acceptance Criteria
- Harness accepts optional `--case` flag.
- Matching case runs successfully by itself.
- Full suite behavior remains unchanged when `--case` is omitted.
- Invalid `case_id` produces a clear, actionable error.
- `latest.json` and `latest.md` are still written for single-case runs.
- `uv run pytest -q` passes offline.
- `uv run python -m evals.harness --suite golden --case case_007_tone_violation_rewrite --outdir evals/results` runs successfully.

## 6) Commands
- `uv run pytest -q`
- `uv run python -m evals.harness --suite golden --case case_007_tone_violation_rewrite --outdir evals/results`
- `uv run python -m evals.harness --suite golden --outdir evals/results`
