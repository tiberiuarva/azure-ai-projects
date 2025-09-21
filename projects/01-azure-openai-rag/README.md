# Project 01 - Azure OpenAI RAG

End-to-end example that provisions Azure AI Search + Azure OpenAI, deploys a model, and runs a FastAPI backend with a lightweight web UI for retrieval-augmented generation.

## Repository Walkthrough
- `infra/` - Bicep templates and reusable modules (`infra/modules/`).
- `deploy.sh` / `cleanup.sh` - automation scripts that validate/deploy or tear down the infrastructure and manage local secrets (configure values directly in the scripts or export environment overrides).
- `app/` - FastAPI service (`main.py`) and ingestion script (`ingest.py`).
- `web/` - Static HTML client that talks to the FastAPI API.
- `eval/` - Evaluation harness (`run_eval.py`) and metrics documentation.
- `governance/` - Responsible AI evidence (checklist, data flow, risk log, policies, sign-off).

- `deploy.sh` validates the Bicep template, deploys it, then retrieves service keys with the Azure CLI and writes `app/.env`. Edit the variable section near the top (subscription ID, location, resource group, prefixes, model details) or export overrides before running the script.
- `cleanup.sh` deletes the resource group (async) and removes the local deployment artifacts using the same inline configuration block.

## Deployment Workflow
1. **Deploy infrastructure and capture secrets**
    ```bash
    bash deploy.sh
    ```
   (Ensure you have already authenticated with `az login` or enable auto-login as noted above.)
    - Runs `az deployment group validate` first.
   - Deploys the Bicep template using the variables defined near the top of `deploy.sh` (environment overrides respected).
    - Fetches service keys via `az cognitiveservices account keys list` and `az search admin-key show`.
    - Writes `app/.env` (git-ignored) with the credentials.

2. **Install Python dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Load environment variables & ingest sample docs**
    ```bash
    set -a; source app/.env; set +a
    python app/ingest.py
    ```
    - The ingestion script strips whitespace from secrets and falls back gracefully when semantic/vector features are unavailable in older SDKs.

4. **Run the FastAPI backend**
    ```bash
    uvicorn app.main:app --reload
    ```
    - `main.py` scrubs env vars, exposes `/healthz`, retries search without semantic configuration when the index doesn't support it, and honours `AZURE_SEARCH_SEMANTIC=false` to skip semantic search outright.
    - CORS is configured for localhost and `file://` origins, so the static page can be served from disk or a simple web server.

5. **Serve the web client**
    ```bash
    python -m http.server --directory web 5500
    ```
    Browse to `http://localhost:5500/`. The page calls the API at the same origin when served over HTTP, and falls back to `http://localhost:8000` when opened via `file://`, surfacing errors inline if the request fails.

### Dev Container Support
- `shared/.devcontainer/devcontainer.json` starts from the Python 3.11 devcontainer image, adds Azure CLI + jq, forwards ports 8000/5500, and runs `shared/.devcontainer/postCreate.sh` to install `requirements.txt`, `projects/01-azure-openai-rag/requirements.txt`, and `az bicep install`. Open the repo with “Dev Containers: Reopen in Container” for a reproducible Project 01 environment.

## Evaluation
- `eval/run_eval.py` measures citation presence, a groundedness proxy, substring accuracy, per-request latency (p50/p95), and source counts using `eval/queries.jsonl`.
- `eval/metrics.md` documents the covered metrics and lists potential future checks for quality, safety, and operations (e.g., toxicity detection, hallucination judging, throughput/cost tracking, red-team suites).

## Governance Artifacts
- `governance/checklist.md` tracks implemented controls with evidence links.
- `governance/data-flow.md` summarizes how data and secrets move through the system.
- `governance/risk-log.md` captures known risks and mitigations; `policies.md` stores planned Content Safety, monitoring, and RBAC snapshots.
- `governance/signoff.md` records stakeholder approvals so the portfolio shows responsible AI practices alongside code.

## Cleanup
```bash
bash cleanup.sh
```
- Uses the hard-coded configuration block and issues `az group delete --no-wait` for the project resource group.
- Removes `.deploy-output.json` and `app/.env` locally.

## Troubleshooting Notes
- Set `AZURE_SEARCH_SEMANTIC=false` before running the API if your search index lacks semantic settings to skip the first semantic attempt.
- Update the variable block in `deploy.sh`/`cleanup.sh` (or export overrides) when changing model details, capacity, or naming.
- Re-running `deploy.sh` is idempotent: it validates, redeploys, and refreshes keys each time.
