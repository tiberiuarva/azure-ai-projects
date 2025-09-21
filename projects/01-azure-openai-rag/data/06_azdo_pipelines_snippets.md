# Azure DevOps Pipelines Snippets
Use templates to standardize quality gates:

```yaml
stages:
- stage: Validate
  jobs:
  - job: Lint
    pool: { vmImage: 'ubuntu-latest' }
    steps:
    - script: echo "Run bicep build/lint here"
```
