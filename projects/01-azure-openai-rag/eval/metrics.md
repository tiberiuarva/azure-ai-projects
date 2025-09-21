# Evaluation Plan

## Covered by `run_eval.py`
- **Quality**
  - Citation presence rate (detects `[n]` markers).
  - Groundedness proxy: proportion of sentences ending with a citation marker.
  - Exact-match heuristic: answer contains expected substring when provided.
- **Operations**
  - Per-request latency measurements with aggregate p50 / p95.
  - Source count recorded per answer (sanity signal for retrieval).

## Potential Future Checks
- **Quality**
  - Automated answer relevance scoring against ground-truth references.
  - Citation accuracy validation (ensure cited documents really contain the referenced facts).
- **Safety**
  - Toxicity / sensitive-topic detection using Azure Content Safety or OpenAI moderation.
  - Hallucination detection via human review loop or LLM-based judges.
  - Prompt-injection and jailbreak stress tests.
- **Operations**
  - Throughput calculations across test suites.
  - Token accounting to estimate cost per request.
  - Resource utilization / quota monitoring during load.
