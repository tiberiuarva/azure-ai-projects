import os
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.core.exceptions import HttpResponseError
from openai import AzureOpenAI

app = FastAPI(title="Azure OpenAI RAG Demo")

# CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r".*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment
AZURE_SEARCH_ENDPOINT = (os.getenv("AZURE_SEARCH_ENDPOINT") or "").strip()
AZURE_SEARCH_API_KEY = (os.getenv("AZURE_SEARCH_API_KEY") or "").strip()
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME", "rag-demo-index")
AZURE_OPENAI_ENDPOINT = (os.getenv("AZURE_OPENAI_ENDPOINT") or "").strip()
AZURE_OPENAI_API_KEY = (os.getenv("AZURE_OPENAI_API_KEY") or "").strip()
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
AZURE_OPENAI_DEPLOYMENT = (os.getenv("AZURE_OPENAI_DEPLOYMENT") or "").strip()
SEMANTIC_SUPPORTED = os.getenv("AZURE_SEARCH_SEMANTIC", "true").lower() == "true"

class AskRequest(BaseModel):
    question: str
    top_k: int = 4

def get_search_client():
    if not AZURE_SEARCH_ENDPOINT or not AZURE_SEARCH_API_KEY:
        raise RuntimeError("AZURE_SEARCH_ENDPOINT/AZURE_SEARCH_API_KEY missing.")
    return SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
    )

def get_oai_client():
    if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_DEPLOYMENT:
        raise RuntimeError("AZURE_OPENAI_* environment variables missing.")
    return AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

@app.get("/healthz")
def healthz():
    return {"ok": True}

def _search_documents(sc: SearchClient, question: str, top_k: int) -> List[Dict]:
    global SEMANTIC_SUPPORTED

    use_semantic = SEMANTIC_SUPPORTED

    for attempt in range(2):
        search_kwargs = {
            "search_text": question,
            "top": top_k,
        }

        if use_semantic:
            search_kwargs.update({
                "query_type": "semantic",
                "semantic_configuration_name": "default",
            })

        try:
            results = sc.search(**search_kwargs)
            passages: List[Dict] = []
            for r in results:
                passages.append({
                    "title": r.get("title") or "",
                    "content": r.get("content") or "",
                    "url": r.get("url") or ""
                })
            return passages
        except HttpResponseError as ex:
            message = getattr(ex, "message", str(ex)).lower()
            if use_semantic and ("semantic" in message or ex.status_code in (400, 404)):
                SEMANTIC_SUPPORTED = False
                use_semantic = False
                continue
            raise

    return []


@app.post("/ask")
def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty.")

    sc = get_search_client()
    passages = _search_documents(sc, req.question, req.top_k)

    sources_text = "\n\n".join([
        f"[{i+1}] {p['title']} — {p['url']}\n{p['content']}" for i, p in enumerate(passages)
    ]) or "No matching documents were retrieved from the search index."

    system_prompt = (
        "You are a helpful assistant that answers strictly using the provided sources.\n"
        "Rules:\n"
        "- If the answer is not in sources, say you don't know.\n"
        "- Always cite sources as [1], [2], ... at the end of each relevant sentence.\n"
        "- Be concise and avoid speculation."
    )
    user_prompt = f"Question: {req.question}\n\nSources:\n{sources_text}\n\nAnswer:"

    client = get_oai_client()
    try:
        chat = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
        )
        answer = chat.choices[0].message.content if chat.choices else ""
    except Exception as exc:  # pragma: no cover - runtime failure path
        raise HTTPException(status_code=502, detail=f"Azure OpenAI error: {exc}") from exc
    return {
        "answer": answer,
        "sources": [
            {"title": p.get("title"), "url": p.get("url")}
            for p in passages if p
        ],
    }
