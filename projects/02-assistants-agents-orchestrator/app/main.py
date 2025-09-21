from fastapi import FastAPI
app = FastAPI(title="Assistants Orchestrator")

@app.get("/healthz")
def healthz():
    return {"ok": True}

# TODO: Add endpoints to kickoff multi-agent run and stream events
