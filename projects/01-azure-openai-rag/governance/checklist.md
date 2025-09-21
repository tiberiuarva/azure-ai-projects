# AI Governance Checklist — Project 01

| Control | Status | Evidence / Notes |
| --- | --- | --- |
| Data classification & residency reviewed | ✅ | Region locked to West Europe. See variable block in `deploy.sh` for subscription/region defaults. No cross-region services created. |
| Prompt-injection / jailbreak mitigations | ✅ | System prompt in `projects/01-azure-openai-rag/app/main.py` enforces source citing & refusal. Retrieval scope limited to markdown docs via `app/ingest.py`. |
| PII handling & redaction | ⚠️ | Keys stored locally in `app/.env`. No automated redaction yet. Plan: integrate Azure Content Safety PII detection before production. |
| Content Safety policies configured | ⚠️ | Placeholder policy JSON in `projects/01-azure-openai-rag/governance/policies.md`. Service deployment pending. |
| Human-in-the-loop approvals | ⬜️ | Not defined. Requires business process before external launch. |
| Logging, traceability & incident playbook | ⬜️ | FastAPI/uvicorn logs only. Need centralized monitoring + incident response doc. |
| RBAC & least privilege | ✅ | Deployment executed with limited subscription access; see `governance/policies.md` for planned role assignments. |
| Secrets management | ⚠️ | Keys retrieved via Azure CLI and stored in `app/.env` (git-ignored). Plan to move to Azure Key Vault. |
| Eval coverage | ✅ | `eval/run_eval.py` & `eval/metrics.md` document groundedness, citation, latency checks. |

Legend: ✅ complete · ⚠️ needs improvement · ⬜️ not started
