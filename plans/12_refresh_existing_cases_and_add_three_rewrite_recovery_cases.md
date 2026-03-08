# Step 13 — Refresh Existing Golden Cases + Add 3 Rewrite-Recovery Cases

## 1) Goal
Make the golden suite fully explicit and expand it with three deterministic rewrite-recovery cases for:
- tone drift
- brand voice mismatch
- generic content

## 2) Scope
- Update the first 6 golden YAML cases to include:
  - `require_quality_pass: true`
- Add 3 new golden cases that follow the deterministic pattern:
  - stub bad writer output
  - run real quality
  - stub corrected rewrite output
  - require final quality pass
- New cases:
  - `case_007_tone_violation_rewrite`
  - `case_008_brand_voice_mismatch`
  - `case_009_generic_content_detection`
- Update manifest ordering and version.
- Keep existing suite behavior unchanged otherwise.

## 3) Case Design Guidance
Tone recovery case:
- Initial writer output should fail `tone_ok`.
- Rewrite output should remove hype language and pass.

Brand voice recovery case:
- Initial writer output should fail `brand_voice_ok`.
- Rewrite output should shift to credible enterprise B2B voice and pass.

Generic content recovery case:
- Initial writer output should fail `specificity_ok`.
- Rewrite output should add concrete operational/governance insight and pass.

## 4) Acceptance Criteria
- First 6 cases explicitly include `require_quality_pass: true`.
- 3 new cases are schema-valid.
- New cases route through rewrite and pass final quality.
- Golden manifest includes all 9 cases in explicit order.
- `uv run pytest -q` passes offline.
- `uv run python -m evals.harness --suite golden --outdir evals/results` runs successfully.

## 5) Commands
- `uv run pytest -q`
- `uv run python -m evals.harness --suite golden --outdir evals/results`
