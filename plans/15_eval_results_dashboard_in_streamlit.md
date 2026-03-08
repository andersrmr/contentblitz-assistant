# Step 16 — Eval Results Dashboard in Streamlit

## 1) Goal
Add a lightweight Eval Results dashboard to the Streamlit UI so eval performance can be viewed directly in the app instead of opening `latest.json` or `latest.md` manually.

## 2) Scope
- Load eval data from `evals/results/latest.json`.
- Add an "Eval Results" section below the existing generation workflow.
- Display top-level KPI cards for:
  - `final_pass_rate`
  - `first_pass_pass_rate`
  - `rewrite_trigger_rate`
  - `rewrite_recovery_rate`
  - `avg_rewrite_count`
- Display category-level metrics from `aggregate.by_category`.
- Display a per-case results table.
- Add a simple case detail viewer using a selectbox + JSON view.
- Do not modify the existing generation workflow behavior.

## 3) Architectural Rationale
The eval framework now produces useful aggregate and per-case diagnostics, but they are inconvenient to inspect via raw JSON/Markdown files. A Streamlit dashboard provides a faster, more convenient daily workflow while keeping `latest.json` as the underlying source of truth.

## 4) UI Design
Sections:
- Eval Results
- KPI metric cards
- Metrics by Category
- Per-Case Results
- Inspect Case

KPI cards:
- Final Pass Rate
- First-Pass Pass Rate
- Rewrite Trigger Rate
- Rewrite Recovery Rate
- Avg Rewrite Count

Per-case table columns:
- category
- case_id
- passed
- rewrite_count
- quality_status

## 5) Acceptance Criteria
- Streamlit app loads `latest.json` when present.
- App shows a helpful message when no eval results exist.
- KPI cards render correctly.
- Category metrics table renders.
- Per-case results table renders.
- Selecting a case shows its JSON details.
- Existing content-generation workflow still runs as before.

## 6) Commands
- `uv run streamlit run src/ui/streamlit_app.py`
- `python -m py_compile src/ui/streamlit_app.py`
