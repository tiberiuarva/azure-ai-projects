#!/usr/bin/env bash
set -euo pipefail

# ==== CONFIG ====
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SUBSCRIPTION_ID="bfd8500c-73fd-46d1-bf00-73523502d6d3"
RESOURCE_GROUP="rg-aoai-rag-demo-001"
LOCATION="westeurope"

# ==== Set Subscription ====
az account set --subscription "$SUBSCRIPTION_ID"

# ==== Resource Cleanup ====
if az group show --name "$RESOURCE_GROUP" --subscription "$SUBSCRIPTION_ID" --query "name" -o tsv >/dev/null 2>&1; then
  echo "Deleting resource group '$RESOURCE_GROUP' in subscription '$SUBSCRIPTION_ID' (location: $LOCATION)..."
  az group delete --name "$RESOURCE_GROUP" --subscription "$SUBSCRIPTION_ID" --yes --no-wait
  echo "Deletion requested. Azure will remove all resources in the group shortly."
else
  echo "Resource group '$RESOURCE_GROUP' not found. Nothing to delete."
fi

# ==== Local artifacts ====
rm -f "$SCRIPT_DIR/.deploy-output.json" "$SCRIPT_DIR/app/.env"

echo "Local deployment artifacts removed."
echo "Cleanup script finished."
