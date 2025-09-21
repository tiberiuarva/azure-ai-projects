# 03 Copilot Studio Internal Qa

**Goal:** Copilot Studio bot for internal policy/knowledge with Dataverse + approvals.

## Architecture
- Ingestion / Index: Azure Blob + Azure AI Search (RAG) or Dataverse for Copilot.
- Reasoning: Azure OpenAI (gpt-4o family) or OpenAI Assistants with tools.
- Orchestration: Prompt flow / Semantic Kernel / function calling.
- App: FastAPI web app + simple UI.

## Setup (TL;DR)
- `az login` and set subscription.
- Deploy `infra/main.bicep`.
- Create `.env` (see `.env.example`).
- `pip install -r ../../shared/requirements.txt`
- `uvicorn app.main:app --reload`

## Demo
- Record a <3 min screencast showing the value, not the config.
- Include 2–3 screenshots in this README.

## Evaluation
- Add Prompt flow/offline evals in `/eval`.
- Track latency/cost and groundedness.

## Governance
- Fill in the checklist in `/governance/checklist.md` before publishing.

# Copilot Studio — Internal Q&A
- Connector plan (SharePoint, Dataverse, Azure AI Search)
- Topics & Orchestration: handoff rules + escalation
- Telemetry: transcript export & evaluation hooks
- DLP & compliance notes
