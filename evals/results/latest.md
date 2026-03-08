# Eval Run Summary

- Suite: `golden`
- Golden set version: `v1.2.0`
- Cases: `9`

## Aggregate Metrics

- final_pass_rate: `1.000`
- first_pass_pass_rate: `0.444`
- rewrite_trigger_rate: `0.667`
- rewrite_recovery_rate: `0.833`
- avg_rewrite_count: `0.667`
- first_pass_failure_reason_counts: `{'CTA is missing from the draft body.': 1, 'Draft is not skimmable enough for LinkedIn.': 1, 'Draft tone is too promotional for professional B2B LinkedIn content.': 1, 'Draft voice does not match a credible enterprise B2B brand voice.': 1, 'Draft is too generic and lacks concrete operational insight.': 1}`

## Case Results

| Category | Case | Status | Quality | Rewrites | Notes |
|---|---|---|---:|---:|---|
| happy_path | case_001_create_happy_path | PASS | 1 | 0 | - |
| citation | case_002_citation_filtering | PASS | 1 | 0 | - |
| formatting | case_003_cta_recovery | PASS | 1 | 1 | - |
| formatting | case_004_skim_recovery | PASS | 1 | 1 | - |
| formatting | case_005_headline_recovery | PASS | 1 | 0 | - |
| rewrite_flow | case_006_revise_path | PASS | 1 | 1 | - |
| tone | case_007_tone_violation_rewrite | PASS | 1 | 1 | - |
| brand_voice | case_008_brand_voice_mismatch | PASS | 1 | 1 | - |
| specificity | case_009_generic_content_detection | PASS | 1 | 1 | - |
