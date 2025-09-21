// infra/main.bicep
targetScope = 'resourceGroup'

param name string = 'ai-portfolio'
param location string = resourceGroup().location

// Import shared modules (reference path as needed)
module aiOpenAi '../shared-placeholder.bicep' = {
  name: 'aiOpenAi'
  params: {}
}

// TODO: replace with actual resources per project.
