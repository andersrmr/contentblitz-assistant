# Step 17 — First-Pass Failure Reason Analysis in Streamlit

## 1) Goal
Add a small diagnostic section to the Streamlit Eval Results dashboard showing first-pass failure reasons and their counts, so it is easier to see what the system gets wrong before rewrite.

## 2) Scope
- Reuse eval data already loaded from `evals/results/latest.json`.
- Add a "First-Pass Failure Reasons" section to the Eval Results dashboard.
- Read `aggregate.first_pass_failure_reason_counts`.
- Render a small table with columns:
  - reason
  - count
- Sort rows by count descending.
- Show a fallback message when no failure reasons are present.
- Do not modify KPI cards, category metrics, per-case table, or case detail viewer.

## 3) Architectural Rationale
The eval framework now captures first-pass failure reason counts, which are among the most useful diagnostic signals in the suite. Surfacing them in Streamlit makes it easier to identify the dominant weaknesses in the current system without opening `latest.json` manually.

## 4) UI Design
Placement:
- After "Metrics by Category"
- Before "Per-Case Results"

Behavior:
- If `first_pass_failure_reason_counts` exists and is non-empty, render a dataframe.
- Otherwise show a short caption such as:
  - "No first-pass failure reasons recorded."

Table columns:
- reason
- count

Sorting:
- Descending by count

## 5) Acceptance Criteria
- Streamlit dashboard shows a "First-Pass Failure Reasons" section.
- Rows are sorted by count descending.
- Empty-state message appears when no reasons are available.
- Existing dashboard sections continue to render correctly.
- `uv run streamlit run src/ui/streamlit_app.py` works.
- `python -m py_compile src/ui/streamlit_app.py` passes.

## 6) Commands
- `uv run streamlit run src/ui/streamlit_app.py`
- `python -m py_compile src/ui/streamlit_app.py`
