# Risk Log — Project 01

| Risk | Description | Mitigation | Status | Owner |
| --- | --- | --- | --- | --- |
| Retrieval hallucination | RAG answers may cite outdated or short snippets. | Evaluate doc quality, expand context window, monitor groundedness metric in eval/run_eval.py. | In progress | Tiberiu |
| Credential exposure | Keys stored in app/.env locally. | Move secrets to Azure Key Vault + managed identity. | Open | Tiberiu |
| Prompt injection | Uploaded docs could contain malicious instructions. | System prompt enforces citation-only responses; add content validation pipeline. | Mitigated (monitor) | Tiberiu |
| Latency spikes | Azure OpenAI requests may exceed 3s under load. | Baseline latency via eval; add Azure Monitor alert (see policies.md). | Open | Tiberiu |
| Content safety gaps | No automated toxicity/PII filter yet. | Integrate Azure Content Safety API prior to public release. | Open | Tiberiu |
