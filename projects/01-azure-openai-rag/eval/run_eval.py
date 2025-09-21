import json, time, re, requests, statistics, sys
from pathlib import Path

API = "http://localhost:8000/ask"
QFILE = Path("eval/queries.jsonl")

def has_citation(ans: str) -> bool:
    return bool(re.search(r"\[\d+\]", ans))

def groundedness_ratio(ans: str) -> float:
    # naive: % of sentences ending with [n]
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', ans) if s.strip()]
    if not sents:
        return 0.0
    cited = sum(1 for s in sents if re.search(r"\[\d+\]\s*$", s))
    return cited / len(sents)

rows = []
latencies = []
with open(QFILE) as f:
    for line in f:
        q = json.loads(line)
        prompt = q["question"]
        expected = q.get("expected_contains", "").lower()

        t0 = time.time()
        r = requests.post(API, json={"question": prompt, "top_k": 4}, timeout=60)
        dt = (time.time() - t0) * 1000
        latencies.append(dt)

        r.raise_for_status()
        payload = r.json()
        ans = payload.get("answer","")
        sources = payload.get("sources", [])

        accuracy_contains = (expected in ans.lower()) if expected else None
        citation_presence = has_citation(ans)
        grounded = groundedness_ratio(ans)

        rows.append({
            "question": prompt,
            "expected_contains": expected or "",
            "answer_head": ans[:200].replace("\n"," "),
            "citation_presence": citation_presence,
            "groundedness_sent_ratio": round(grounded, 2),
            "accuracy_contains": accuracy_contains,
            "latency_ms": round(dt, 1),
            "num_sources": len(sources),
        })

# Aggregate
agg = {
    "n": len(rows),
    "latency_ms_p50": round(statistics.median(latencies),1) if rows else None,
    "latency_ms_p95": round(sorted(latencies)[int(0.95*len(latencies))-1],1) if rows else None,
    "citation_presence_rate": round(sum(1 for r in rows if r["citation_presence"]) / len(rows), 2) if rows else 0,
    "groundedness_sent_avg": round(sum(r["groundedness_sent_ratio"] for r in rows)/len(rows), 2) if rows else 0,
    "accuracy_contains_rate": round(sum(1 for r in rows if r["accuracy_contains"] is True) / sum(1 for r in rows if r["accuracy_contains"] is not None), 2) if any(r["accuracy_contains"] is not None for r in rows) else None,
}

print("=== Aggregate ===")
print(json.dumps(agg, indent=2))
print("\n=== Per-question ===")
for r in rows:
    print(json.dumps(r, indent=2))
