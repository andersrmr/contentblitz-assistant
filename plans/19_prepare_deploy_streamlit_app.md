# Step 20 - Prepare a Deployment-Focused Streamlit App

## 1. Goal
Create a deployment-focused Streamlit app entrypoint that is separate from the internal/dev UI, so the deployed experience is clean, user-facing, and not tied to eval artifacts or developer analysis views.

## 2. Scope
- Add a new app entrypoint: `src/ui/streamlit_deploy_app.py`
- Keep the deployment app focused on the end-user workflow:
  - topic input
  - audience input
  - revision request
  - Run new draft
  - Revise last draft
  - final output display
- Reuse the existing LangGraph workflow and session-state behavior where reasonable
- Exclude eval dashboard, `latest.json` / `latest.md` readers, and other dev/eval-only UI elements
- Add friendly checks for required secrets/environment variables
- Keep artifacts/session results in memory only for now
- Do not add persistence, S3, database storage, or auth in this step

## 3. Architectural Rationale
The current Streamlit app mixes interactive generation with internal evaluation views. For deployment, the user-facing app should be simpler, cleaner, and independent of local eval artifacts. A separate deploy app entrypoint is the fastest safe way to prepare for hosting while preserving the richer internal UI for development.

## 4. UI Design
Page title:
- AI Content Marketing Assistant

Core sections:
- short intro/caption explaining the app
- topic input
- audience input
- optional revision request
- Run new draft button
- Revise last draft button
- result display

Result display:
- show final draft prominently
- optionally show research / brief / quality in expanders or tabs
- do not expose eval results

Error handling:
- if `OPENAI_API_KEY` or `SERPAPI_API_KEY` are missing, show a clear warning/error message and do not attempt a run

## 5. Deployment Preparation
- Add a root `requirements.txt` suitable for deployment
- Ensure `pandas` is included if any deployed app code depends on it
- Keep settings driven by environment variables rather than relying on a local `.env` file in production
- Do not add Dockerfile or App Runner config in this step

## 6. Acceptance Criteria
- `src/ui/streamlit_deploy_app.py` exists and runs locally
- deployed app entrypoint does not reference `evals/results/latest.json` or eval dashboard code
- app shows clear secret-missing message when required keys are absent
- app can run new draft and revise flows using existing graph logic
- `python -m py_compile src/ui/streamlit_deploy_app.py` passes
- `uv run streamlit run src/ui/streamlit_deploy_app.py` works locally

## 7. Commands
- `python -m py_compile src/ui/streamlit_deploy_app.py`
- `uv run streamlit run src/ui/streamlit_deploy_app.py`
