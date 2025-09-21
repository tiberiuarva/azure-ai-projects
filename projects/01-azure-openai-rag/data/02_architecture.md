# Architecture
- **Azure AI Search** holds indexed content with fields id, content, title, url.
- **FastAPI** exposes /ask and /healthz endpoints.
- **Azure OpenAI** generates answers using retrieved passages as context.
- The system should include semantic search and show citations for transparency.
