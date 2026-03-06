# Step 9 - Expand Golden Eval Suite

## Goal

Expand the deterministic offline evaluation system by adding a meaningful **golden set** of benchmark cases.

This step strengthens Phase 2 by turning the initial eval scaffold into a more realistic regression suite that covers the most important behaviors of the AI Content Marketing Assistant.

The golden set should remain:

- deterministic
- stable
- versioned
- CI-friendly

This suite will become the primary regression gate for future prompt, agent, and workflow changes.

---

# Why This Step Matters

The current eval scaffold proves that the framework works, but one happy-path case is not enough to measure reliability.

A stronger golden set should verify that the system can consistently handle:

- correct citation behavior
- CTA enforcement
- skim-friendly formatting
- headline compliance
- revise-path routing
- rewrite loop convergence

These are the core quality guarantees of the current architecture.

---

# Scope

This step adds several new golden cases and updates the manifest accordingly.

The harness, metrics, and reporting framework already exist from Plan 07.

This step should **not** introduce major refactors to the production workflow.

It should focus on:

- expanding coverage
- keeping cases deterministic
- validating key system behaviors
- preserving fast execution

---

# Golden Cases to Add

## Case 002 — Citation Filtering

Purpose:

Verify that draft citations must come from the research packet.

Scenario:

The writer output includes at least one citation that does not exist in the available research citations.

Expected behavior:

- citation precision remains 1.0
- invalid citations are removed or corrected predictably
- case passes or fails deterministically according to current logic

---

## Case 003 — CTA Recovery

Purpose:

Verify the system can recover when the initial writer draft lacks a CTA.

Scenario:

The writer output omits a CTA.

Expected behavior:

- quality gate fails CTA presence initially
- rewrite loop or deterministic post-processing restores CTA
- final result passes CTA requirement

---

## Case 004 — Skimmability Recovery

Purpose:

Verify the system can improve readability for LinkedIn formatting.

Scenario:

The writer output is a dense block of text with insufficient paragraph breaks.

Expected behavior:

- initial draft fails skim-format expectations
- rewrite loop or deterministic post-processing converts output into 3 or more readable paragraphs
- final result passes skim-format requirement

---

## Case 005 — Headline Compliance Recovery

Purpose:

Verify the system can recover from an overly long headline.

Scenario:

The writer output contains a headline longer than 12 words.

Expected behavior:

- initial draft fails headline compliance
- rewrite loop shortens headline
- final result passes headline requirement

---

## Case 006 — Revise Path

Purpose:

Verify that revise intent follows the intended workflow behavior.

Scenario:

Intent is revise and the input includes a revision request such as:
"Keep the humor, add emoticons"

Expected behavior:

- revise route is used
- research and strategist stages are skipped if that is how current routing is designed
- rewrite/quality loop executes deterministically
- final output passes quality checks

---

## Optional Case 007 — Rewrite Convergence

Purpose:

Verify that repeated quality failures do not create unstable loop behavior.

Scenario:

The initial draft fails one or more checks and requires multiple rewrites.

Expected behavior:

- rewrite_count increases deterministically
- final pass occurs before max_iterations, or failure occurs predictably at the configured limit
- convergence behavior is observable in eval metrics

This case is optional if the first five cases are already a substantial implementation.

---

# Manifest Update

Update:

evals/cases/golden/manifest.yaml

Requirements:

- include the new case filenames
- preserve explicit case ordering
- keep golden_set_version visible
- optionally bump version only if you think the benchmark definition meaningfully changed

If version is bumped, document the rationale in comments or report output.

---

# Implementation Guidance

Each case should include:

- realistic inputs
- deterministic SERP fixtures
- deterministic stubbed node outputs where needed
- expectations aligned with the current quality system

Avoid exact-string style expectations.

Prefer invariant-based expectations such as:

- CTA present
- headline length <= 12 words
- skim format satisfied
- citations subset of research citations
- rewrite_count <= max_iterations

---

# Testing Expectations

Existing test suite must remain green:

uv run pytest -q

Golden harness must run successfully:

uv run python -m evals.harness --suite golden --outdir evals/results --fail-on-threshold

The updated reports should show multiple cases executed and aggregate metrics across the expanded golden set.

---

# Deliverable

A stronger golden benchmark suite that provides real regression protection for:

- create flow
- revise flow
- citation correctness
- CTA enforcement
- LinkedIn formatting quality
- rewrite-loop reliability

This completes the transition from a proof-of-concept eval scaffold to a genuinely useful production-style regression benchmark.
