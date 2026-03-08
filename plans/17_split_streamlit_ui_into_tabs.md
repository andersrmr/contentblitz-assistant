# Step 18 — Split Streamlit UI into Generate Content and Eval Results Tabs

## 1) Goal
Reduce confusion in the Streamlit UI by separating the live content-generation workflow from the saved eval-suite dashboard. Users should clearly see that ad hoc draft runs and eval harness results are different contexts.

## 2) Scope
- Introduce two top-level tabs in the Streamlit app:
  - Generate Content
  - Eval Results
- Move the existing generation workflow into the Generate Content tab.
- Move the existing eval dashboard into the Eval Results tab.
- Keep all existing functionality intact:
  - content graph invocation
  - revision workflow
  - session state handling
  - eval dashboard rendering from latest.json
- Do not change the underlying generation or eval logic in this step.

## 3) Architectural Rationale
The current UI shows both a live draft run and a saved eval-suite report on the same page, which can imply that the dashboard reflects the ad hoc run above. Splitting the interface into two tabs clarifies the distinction between:
- running the content generation graph interactively
- viewing results from the offline eval harness.

## 4) UI Design
Tab 1: Generate Content
- Contains the current content-generation workflow:
  - topic input
  - audience input
  - revision request
  - Run new draft button
  - Revise last draft button
  - last run output display
- Add a caption at the top:
  - "Run the live content workflow on an ad hoc input."

Tab 2: Eval Results
- Contains the eval dashboard:
  - KPI metric cards
  - Metrics by Category
  - First-Pass Failure Reasons section (if implemented)
  - Per-Case Results table
  - Inspect Case selector
- Add a caption at the top:
  - "This tab shows the most recent saved eval harness results from evals/results/latest.json."

## 5) Acceptance Criteria
- Streamlit UI shows two tabs: Generate Content and Eval Results.
- Generate Content tab runs the content workflow exactly as before.
- Eval Results tab displays the dashboard based on latest.json.
- The dashboard does not change when running ad hoc drafts.
- The app compiles and runs successfully.
- `python -m py_compile src/ui/streamlit_app.py` passes.
- `uv run streamlit run src/ui/streamlit_app.py` works locally.

## 6) Commands
- `python -m py_compile src/ui/streamlit_app.py`
- `uv run streamlit run src/ui/streamlit_app.py`
