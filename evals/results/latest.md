# Eval Run Summary

- Suite: `golden`
- Golden set version: `v1.1.0`
- Cases: `6`

## Aggregate Metrics

- final_pass_rate: `1.000`
- first_pass_pass_rate: `0.667`
- rewrite_trigger_rate: `0.500`
- rewrite_recovery_rate: `0.667`
- avg_rewrite_count: `0.500`
- first_pass_failure_reason_counts: `{'CTA is missing from the draft body.': 1, 'Draft is not skimmable enough for LinkedIn.': 1}`

## Case Results

| Case | Status | Quality | Rewrites | Notes |
|---|---|---:|---:|---|
| case_001_create_happy_path | PASS | 1 | 0 | - |
| case_002_citation_filtering | PASS | 1 | 0 | - |
| case_003_cta_recovery | PASS | 1 | 1 | - |
| case_004_skim_recovery | PASS | 1 | 1 | - |
| case_005_headline_recovery | PASS | 1 | 0 | - |
| case_006_revise_path | PASS | 1 | 1 | - |
