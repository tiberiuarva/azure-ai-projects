# Azure AI Portfolio — Starter Kit

Curated portfolio scaffolding focused on **Azure AI Foundry, Azure OpenAI, OpenAI Assistants, and Copilot Studio**.

## What's inside
- Opinionated project templates (RAG, agents, Copilot Studio, vision, safety).
- IaC with Bicep modules, devcontainer, CI seed, and governance checklists.
- Evaluation-first mindset (Prompt flow hooks, offline evals, red-teaming notes).

> Tip: Start with `01-azure-openai-rag`, then move to agents (`02`), Copilot Studio (`03`), and safety (`06`).

## Quickstart
1. Pick a project under `projects/`.
2. Open in Dev Containers (or VS Code) for reproducible environment.
3. Deploy shared baseline with Bicep, then per-project resources.
4. Run the app, capture demos (gif/video), and document measurable outcomes.

### Project 01 – Azure OpenAI RAG (Complete)
**Goal:** build a retrieval-augmented generation pipeline that stays grounded, emits cited answers, and demonstrates responsible AI controls end-to-end.

**Azure Resources Provisioned**
- Azure AI Search (index + semantic configuration) for document retrieval.
- Azure OpenAI (deployment of `gpt-4o-mini` with configurable capacity/SKU).
- Infrastructure modules live in `projects/01-azure-openai-rag/infra/modules/`, and deployment scripts define their own configuration block (edit the variables in `deploy.sh`/`cleanup.sh` or export overrides before running).

**What We Exercise**
- Infrastructure-as-code validation (`az deployment group validate`) before every deploy.
- Secure key handling in automation: `deploy.sh` provisions infra, fetches keys via CLI, and drops them into a git-ignored `app/.env`.
- RAG backend: FastAPI (`app/main.py`) handles semantic fallback when the index lacks semantic settings, enforces source-based prompting, and exposes `/healthz`.
- Document ingestion: `app/ingest.py` reads markdown, creates the search index (with optional vector/semantic settings when the SDK supports it), and uploads docs.
- Lightweight web client (`web/index.html`) that talks to `/ask` and shows answers + sources.
- Offline evaluation: `eval/run_eval.py` measures citation presence, groundedness proxy, substring accuracy, and latency percentiles defined in `eval/metrics.md`.
- Governance evidence: `governance/` contains checklist, risk log, data flow, policy snapshots, and sign-off to simulate enterprise readiness.
- Cleanup: `cleanup.sh` provides a matching inline config to delete the resource group and scrub local artifacts.

### Project 02 – Assistants Agents Orchestrator (Planned)
**What it is:** multi-agent orchestration sample powered by the OpenAI Assistants API with optional Semantic Kernel integration.

**Goal:** show how specialized agents (retrieval, summarization, ticketing) collaborate to solve workflows end-to-end.

**Deliverables**
- `app/` FastAPI endpoints to start and monitor agent conversations.
- Example tools (Azure DevOps API, search query helpers, custom actions).
- `eval/` scenarios such as “create a ticket from a log entry.”
- `governance/` guardrails documenting tool limits and approvals for risky actions.

### Project 03 – Copilot Studio Internal QA (Planned)
**What it is:** Copilot Studio solution for internal knowledge Q&A (IT policies, onboarding, SOPs).

**Goal:** demonstrate conversational design that unifies SharePoint/Dataverse data with Azure AI Search grounding.

**Deliverables**
- Copilot Studio topics and flows export assets.
- Connectors to SharePoint or Azure AI Search data sources.
- `governance/` package covering DLP considerations and escalation paths.
- Screenshots or short video of the Copilot in Microsoft Teams.

### Project 04 – Vision Document Intake (Planned)
**What it is:** document intelligence pipeline using Azure AI Vision/Form Recognizer paired with RAG.

**Goal:** extract structure from PDFs, index to Azure AI Search, and enable grounded Q&A over ingested documents.

**Deliverables**
- `app/ingest.py` pipeline for OCR, parsing, and indexing.
- `app/main.py` Q&A endpoint backed by Azure OpenAI.
- `data/` sample scanned documents for demos and tests.
- `eval/` metrics tracking OCR accuracy and grounding quality.
- `governance/` guidance on handling sensitive documents.

### Project 05 – DevOps Copilot Accelerator (Planned)
**What it is:** DevOps copilot that assists with Infrastructure-as-Code reviews and pipeline authoring.

**Goal:** automate compliant Bicep/Terraform suggestions with guardrails baked into the workflow.

**Deliverables**
- Prompt + completion gallery for generating Bicep snippets.
- `app/` API that lints IaC before proposing changes.
- Integrations with GitHub Actions and Azure DevOps pipelines.
- `eval/` corpus of IaC files with pass/fail compliance checks.
- `governance/` notes outlining policy enforcement.

### Project 06 – Content Safety Moderation (Planned)
**What it is:** reference implementation of Azure AI Content Safety wrapped around app experiences.

**Goal:** prove moderation across text/images, PII redaction, and safe-completion enforcement.

**Deliverables**
- `app/main.py` gateway that layers safety checks over Azure OpenAI calls.
- `data/` synthetic toxic and PII samples for testing.
- `eval/` red-team scripts measuring refusals and safe filtering rates.
- `governance/` with moderation policy, thresholds, and incident response.

## Portfolio Artifacts (per project)
- **README.md** with problem statement, architecture, diagrams, setup, and demo.
- **/infra** (Bicep) and CI seed.
- **/app** minimal runnable sample.
- **/eval** with metrics (groundedness, toxicity, latency, cost).
- **/governance** with AI risk checklist, data flows, and approvals.

---

© 2025 Tiberiu Arva — MIT License
