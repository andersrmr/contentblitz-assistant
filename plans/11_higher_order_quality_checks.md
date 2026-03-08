# Step 12 — Higher-Order Quality Checks for Tone, Brand Voice, and Specificity

## 1) Goal
Extend the quality gate so it can detect higher-order content defects that matter for LinkedIn B2B marketing output:
- overly promotional tone
- brand voice mismatch
- generic / low-specificity content

## 2) Scope
- Add deterministic checks in `agents/quality.py` for:
  - `tone_ok`
  - `brand_voice_ok`
  - `specificity_ok`
- Add corresponding reasons and fixes to `QualityReport` generation.
- Keep all existing deterministic checks unchanged:
  - citations present
  - citations used
  - max_words
  - headline length
  - CTA present in body
  - LinkedIn skimmability
- Ensure new checks are simple, deterministic, and offline-safe.
- Do not yet change `rewrite.py` prompt structure beyond consuming the new fixes already emitted by quality.
- Do not yet add the new golden cases in this step.

## 3) Check Design Guidance
Tone check:
- Fail on obviously hype/promotional phrasing such as:
  - secret weapon
  - ultimate game changer
  - transform your entire organization
  - sign up today
  - already behind the competition
- Intended target is professional, analytical B2B LinkedIn tone.

Brand voice check:
- Fail on casual/influencer-style phrasing such as:
  - hacks
  - move fast
  - follow for more tips
  - just experiment
  - worry about governance later
- Intended target is credible, professional, enterprise-oriented voice.

Specificity check:
- Fail when draft body is too generic / obvious and lacks concrete, research-grounded insight.
- Use a simple deterministic heuristic, not an LLM judge.
- Examples of generic patterns:
  - AI is becoming more important
  - many organizations are thinking about
  - companies should consider
- Encourage at least one concrete operational or governance-oriented point.

## 4) Acceptance Criteria
- Quality report validates with the expanded checks map.
- New checks add reasons/fixes when they fail.
- Existing tests pass or are minimally updated.
- `uv run pytest -q` passes offline.
- `uv run python -m evals.harness --suite golden --outdir evals/results` runs successfully.

## 5) Commands
- `uv run pytest -q`
- `uv run python -m evals.harness --suite golden --outdir evals/results`
