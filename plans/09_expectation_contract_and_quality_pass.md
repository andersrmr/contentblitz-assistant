# Step 10 — Expectation Contract + Explicit Quality Pass

## 1) Goal
Introduce an explicit expectation contract for eval cases by adding `require_quality_pass` to `EvalCaseExpectations`. This removes implicit behavior from the harness and makes success vs expected-failure cases explicit.

## 2) Scope
- Add `require_quality_pass: bool = True` to `EvalCaseExpectations` in `schema.py`.
- Move final-quality validation logic into `evaluate_expectations()`.
- Remove hardcoded final quality enforcement from `harness.py`.
- Ensure backward compatibility by defaulting `require_quality_pass=True`.
- Prepare the eval system for richer metrics and failure-mode cases.

## 3) Architectural Rationale
`harness.py` currently enforces final quality pass implicitly for every case. Moving this rule into expectations:
- Makes eval behavior explicit.
- Enables safe-failure test cases.
- Keeps harness orchestration logic simple.
- Aligns expectations with YAML configuration.

## 4) Acceptance Criteria
- `EvalCaseExpectations` includes `require_quality_pass` with default `True`.
- `evaluate_expectations()` enforces quality pass according to this field.
- `harness.py` no longer hardcodes quality pass validation.
- Existing golden cases still pass unchanged.
- `uv run pytest -q` passes offline.

## 5) Commands
- `uv run pytest -q`
- `uv run python -m evals.harness --suite golden --outdir evals/results`
