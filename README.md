# AI Content Marketing Assistant (ContentBlitz)

A LangGraph-powered, multi-step assistant that generates high-quality, citation-backed marketing content (optimized for LinkedIn) using:

- **Research** (SerpAPI)
- **Strategy / Brief** (OpenAI, schema-validated)
- **Draft writing** (OpenAI, schema-validated)
- **Deterministic quality gate** + **rewrite loop** (OpenAI-backed rewrite + guardrails)
- **Streamlit UI** to run “Create” and “Revise” workflows

This project is designed as a capstone-style implementation emphasizing:
- structured state + schema validation (Pydantic)
- deterministic tests (offline)
- safe fallbacks when LLM calls fail
- citation hygiene (no invented URLs)

---

## Features

### ✅ Research (SerpAPI)
- Generates multiple queries from the topic
- Fetches SERP results via SerpAPI
- Normalizes and deduplicates sources
- Produces a schema-validated `ResearchPacket`

### ✅ Strategist (OpenAI JSON → ContentBrief)
- Uses research signals to produce a structured content brief:
  - topic, audience, objective, channel, angle, outline, CTA
- JSON-only output with schema validation

### ✅ Writer (OpenAI JSON → Draft)
- Produces a LinkedIn-ready draft:
  - headline, body, CTA, citations
- Citations are filtered to **only URLs already present in research**

### ✅ Quality Gate (Deterministic)
Validates the draft with deterministic checks:
- citations present / used
- headline length
- max words (if provided)
- CTA presence in body
- LinkedIn skimmability (blank-line-separated paragraphs)

### ✅ Rewrite Loop (OpenAI + Guardrails)
- If quality fails, rewrite runs with targeted fixes
- Deterministic post-processing guarantees:
  - CTA appears in the body
  - at least 3 blank-line-separated paragraphs
- Loop continues until pass or `MAX_ITERATIONS`

### ✅ Create vs Revise (Streamlit)
- **Run new draft**: full pipeline (research → brief → draft → quality/rewrite)
- **Revise last draft**: rewrite + quality loop using revision instructions

---

## Tech Stack

- **Python 3.11**
- **uv** for env + dependency management
- **LangGraph** for orchestration + state
- **OpenAI** (new `OpenAI()` client) for strategist/writer/rewrite
- **SerpAPI** for web research
- **Pydantic** for schema validation
- **Streamlit** for UI
- **pytest** for deterministic tests (offline by default)

---

## Repo Structure

```text
.
├─ src/
│  ├─ agents/                 # research, strategist, writer, quality, rewrite, router
│  ├─ app/                    # config, models, prompts, typed state
│  ├─ integrations/           # serp + openai client wrappers
│  ├─ ui/                     # streamlit UI
│  └─ workflow/               # graph assembly + routing
├─ tests/                     # offline deterministic unit tests
├─ plans/                     # numbered implementation plans
└─ docs/                      # architecture diagram and docs