param location string
param accountName string
@description('Custom domain name for the endpoint')
param customDomainName string
@description('SKU for the Azure OpenAI account')
@allowed([
  'S0'
])
param skuName string = 'S0'
param tags object = {}

@description('The model being deployed')
param modelName string
@description('Version of the model being deployed')
param modelVersion string
@description('Name of the deployment')
param deploymentName string
@description('Capacity for the deployed model')
@minValue(1)
param capacity int = 1
@description('SKU tier for the deployed model')
@allowed([
  'GlobalStandard'
  'GlobalStandard-Limited'
  'Standard'
])
param deploymentSkuName string = 'GlobalStandard'

resource aoai 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: accountName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: skuName
  }
  kind: 'AIServices'
  properties: {
    customSubDomainName: customDomainName
  }
  tags: tags
}

// Model deployment under the Azure OpenAI account
resource deployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  name: deploymentName
  parent: aoai
  properties: {
    model: {
      format: 'OpenAI'
      name: modelName
      version: modelVersion
    }
  }
  sku: {
    name: deploymentSkuName
    capacity: capacity
  }
}

var keys = aoai.listKeys()

@secure()
output primaryKey string = keys.key1
@secure()
output secondaryKey string = keys.key2
output endpoint string = aoai.properties.endpoint
output deploymentName string = deployment.name
output resourceId string = aoai.id
