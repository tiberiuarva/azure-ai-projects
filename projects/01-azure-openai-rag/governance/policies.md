# Governance Policies & Config Snapshots — Project 01

## Azure Content Safety (Planned)
```json
{
  "category": "Hate",
  "severities": ["Medium", "High"],
  "action": "Block",
  "notes": "To be applied to all user prompts before invoking Azure OpenAI."
}
```
Status: **Pending** — capture real export once the Content Safety resource is deployed.

## Azure Monitor Alert (Draft)
```json
{
  "name": "aoai-latency-p95",
  "criteria": {
    "metricName": "Latency",
    "timeAggregation": "Percentile95",
    "threshold": 3000
  },
  "actions": ["email:tiberiu@example.com"]
}
```
Status: **Planned** — hook into FastAPI or Application Insights metrics after first load test.

## Bicep Hardening Snippet
```
// Add to infra/modules/search.bicep when Key Vault is in place
properties: {
  disableLocalAuth: true
  publicNetworkAccess: 'enabled'
}
```
> Current deployment keeps `disableLocalAuth: false` because admin keys are used via CLI. Track migration to managed identity in the backlog.

## RBAC Assignments (Target State)
| Role | Scope | Assignee | Status |
| --- | --- | --- | --- |
| Cognitive Services Contributor | `rg-aoai-rag-demo` | Tiberiu | Active |
| Search Service Contributor | `rg-aoai-rag-demo` | Tiberiu | Active |
| Reader | `rg-aoai-rag-demo` | Stakeholders | Pending |

Keep this file updated with actual exports (`az monitor metrics alert show`, `az role assignment list`) when the environment is hardened.
