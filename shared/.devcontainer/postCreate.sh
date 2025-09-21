#!/usr/bin/env bash
set -euo pipefail

# Use python -m pip to ensure the pip target matches the active Python interpreter
python -m pip install --upgrade pip
if [ -f requirements.txt ]; then
  python -m pip install -r requirements.txt
fi
PROJECT_REQ="projects/01-azure-openai-rag/requirements.txt"
if [ -f "$PROJECT_REQ" ]; then
  python -m pip install -r "$PROJECT_REQ"
fi
# Ensure Azure CLI has Bicep support
az bicep install
