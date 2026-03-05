# Plan 07 — Phase 2 Eval System Scaffold

## Goal

Begin Phase 2 of the AI Content Marketing Assistant by introducing a **deterministic offline evaluation system**.

This eval framework will allow the system to:

- Measure end-to-end behavior of the LangGraph pipeline
- Detect regressions as prompts, agents, or quality checks evolve
- Provide a stable benchmark ("golden set") for CI gating
- Support a growing "challenge set" of difficult scenarios

The eval harness must run **fully offline and deterministically**.

---

# Architecture Concept

The evaluation system introduces a new top-level package:

evals/

Containing:

evals/
  cases/
    golden/
    challenge/
  harness.py
  metrics.py
  report.py

Golden cases are **stable CI benchmarks**.

Challenge cases capture **real-world failures and edge scenarios**.

---

# Golden Set Concept

Golden cases are:

- deterministic
- stable
- versioned
- CI-blocking

Initial size:

10–20 cases (eventually 20–50)

The golden set includes a manifest file:

evals/cases/golden/manifest.yaml

Example:

golden_set_version: v1
description: Initial deterministic eval suite
cases:
  - case_001_create_happy_path.yaml

This ensures the benchmark can evolve without silent drift.

---

# Case Design

Cases are stored as YAML.

Each case defines:

Inputs
Fixtures
Expectations

Conceptual structure:

inputs:
  intent: create
  topic: sustainability in classical christian schools
  audience: educators
  platform: linkedin

fixtures:
  serp_fixture:
    - title: ...
      link: ...
      snippet: ...

expectations:
  max_iterations: 3
  require_cta_presence: true
  require_headline_compliance: true
  require_skim_format: true
  require_citation_precision: true

Fixtures allow **fully offline execution**.

---

# Metrics

The evaluation harness computes system-level metrics.

Initial metrics include:

quality_pass_rate  
rewrite_convergence_rate  
avg_rewrite_count  
headline_compliance_rate  
cta_presence_rate  
skim_format_rate  
citation_precision  

These metrics measure both:

- structural correctness
- rewrite loop stability

---

# Evaluation Harness

The runner will be implemented in:

evals/harness.py

CLI interface:

python -m evals.harness --suite golden

Supported suites:

golden  
challenge  

Outputs:

evals/results/latest.json  
evals/results/latest.md  

Reports include:

- per-case results
- aggregate metrics
- golden_set_version (when applicable)

---

# Deterministic Execution

To guarantee repeatability:

SerpAPI integration will be monkeypatched using fixtures.

OpenAI calls will be monkeypatched with deterministic stub outputs unless a case explicitly defines stubbed responses.

No network calls are allowed during eval execution.

---

# Initial Smoke Case

The scaffold will include one deterministic golden case:

case_001_create_happy_path.yaml

The case should:

- follow the full create pipeline
- include citations
- include CTA
- produce skimmable output
- pass quality checks without excessive rewrites

---

# Implementation Checklist

Create directory structure:

evals/
evals/cases/
evals/cases/golden/
evals/cases/challenge/

Create files:

evals/__init__.py
evals/harness.py
evals/metrics.py
evals/report.py

Create golden manifest:

evals/cases/golden/manifest.yaml

Create first case:

evals/cases/golden/case_001_create_happy_path.yaml

Add results output directory:

evals/results/

Add one pytest test verifying harness execution.

---

# Verification Steps

Run existing test suite:

uv run pytest -q

Run eval harness manually:

uv run python -m evals.harness --suite golden

Expected outputs:

evals/results/latest.json
evals/results/latest.md

Golden suite should execute deterministically.

---

# Deliverable

A working **evaluation scaffold** enabling future expansion of golden and challenge case libraries.

This forms the foundation for:

Phase 2 reliability engineering  
LLM regression detection  
production-style CI gating
