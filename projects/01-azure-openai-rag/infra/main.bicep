targetScope = 'resourceGroup'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Base name/prefix for resources')
param namePrefix string = 'ai-demo-01'

@description('Tags applied to all resources')
param tags object = {
  project: 'rag-demo'
}

@description('Azure AI Search SKU (e.g., basic, standard, standard2, standard3)')
@allowed([ 'basic', 'standard', 'standard2', 'standard3', 'storage_optimized_l1', 'storage_optimized_l2' ])
param searchSku string = 'basic'

@description('Azure OpenAI SKU (must be S0 for OpenAI)')
@allowed([ 'S0' ])
param openAiSkuName string = 'S0'

@description('Azure OpenAI model name to deploy (e.g., gpt-4o-mini, gpt-4o)')
param modelName string = 'gpt-4o-mini'

@description('Azure OpenAI model version (consult your region availability; e.g., 2024-07-18)')
param modelVersion string = '2024-07-18'

@description('Deployment name for the model (used by your app)')
param deploymentName string = 'gpt4oMini'

@description('Throughput units for the model deployment (capacity)')
@minValue(1)
param deploymentCapacity int = 1

@description('SKU tier used for the Azure OpenAI model deployment')
@allowed([
  'GlobalStandard'
  'GlobalStandard-Limited'
  'Standard'
])
param deploymentSkuName string = 'GlobalStandard'

@description('Custom domain name for the Azure OpenAI endpoint (must be globally unique)')
param openAiCustomDomainName string = toLower('${namePrefix}aoai')

@description('Search replicas (increase for query throughput)')
@minValue(1)
param searchReplicaCount int = 1

@description('Search partitions (increase for index size)')
@minValue(1)
param searchPartitionCount int = 1

// === Modules ===

module search './modules/search.bicep' = {
  name: 'searchService'
  params: {
    location: location
    name: toLower('${namePrefix}search')
    sku: searchSku
    replicaCount: searchReplicaCount
    partitionCount: searchPartitionCount
    tags: tags
  }
}

module aoai './modules/azureOpenAI.bicep' = {
  name: 'azureOpenAI'
  params: {
    location: location
    accountName: toLower('${namePrefix}aoai')
    customDomainName: openAiCustomDomainName
    skuName: openAiSkuName
    tags: tags
    modelName: modelName
    modelVersion: modelVersion
    deploymentName: deploymentName
    capacity: deploymentCapacity
    deploymentSkuName: deploymentSkuName
  }
}

// === Outputs ===
@secure()
output searchAdminKey string = search.outputs.adminKey
output searchEndpoint string = search.outputs.endpoint
output searchResourceId string = search.outputs.resourceId

@secure()
output openAiPrimaryKey string = aoai.outputs.primaryKey
@secure()
output openAiSecondaryKey string = aoai.outputs.secondaryKey
output openAiEndpoint string = aoai.outputs.endpoint
output openAiDeploymentName string = aoai.outputs.deploymentName
output openAiResourceId string = aoai.outputs.resourceId
