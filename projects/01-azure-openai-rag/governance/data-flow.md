# Data Flow — Project 01

Azure data flow (high level):

Markdown docs (./data/*.md) → ingestion script (app/ingest.py) → Azure AI Search index (West Europe) → FastAPI backend (app/main.py) → Azure OpenAI deployment (gpt-4o-mini) → FastAPI response → web client (web/index.html).

Supporting notes:
- PII/Data residency: raw docs stay local; deployed services run in West Europe.
- Secrets: generated via deploy.sh and stored temporarily in app/.env (git-ignored); planned migration to Azure Key Vault.
- Public endpoints: Azure OpenAI and Search endpoints are public; FastAPI is local/private in this demo.
- Monitoring: evaluation scripts (eval/) collect latency and citation metrics; connect to Azure Monitor in future work.
