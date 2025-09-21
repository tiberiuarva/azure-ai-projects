#!/usr/bin/env bash
set -Eeuo pipefail

log() {
  echo "[postCreate] $*"
}

# Resolve repository root relative to this script so we work from a known location
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)
cd "$REPO_ROOT"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  log "Python interpreter not found in PATH"
  exit 1
fi

log "Upgrading pip"
"$PYTHON" -m pip install --upgrade pip

if [[ -f requirements.txt ]]; then
  log "Installing root requirements.txt"
  "$PYTHON" -m pip install -r requirements.txt
fi

shopt -s nullglob
project_requirements=(projects/*/requirements*.txt)
for req_file in "${project_requirements[@]}"; do
  log "Installing ${req_file}"
  "$PYTHON" -m pip install -r "$req_file"
done
shopt -u nullglob

shopt -s nullglob
project_pyprojects=(projects/*/pyproject.toml)
for pyproject in "${project_pyprojects[@]}"; do
  project_dir=$(dirname "$pyproject")
  log "Installing editable package from ${project_dir}"
  (cd "$project_dir" && "$PYTHON" -m pip install -e .)
done
shopt -u nullglob

if command -v az >/dev/null 2>&1; then
  log "Ensuring Azure Bicep CLI is installed"
  az bicep install
else
  log "Azure CLI not available; skipping bicep installation"
fi
