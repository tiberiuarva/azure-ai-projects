param location string
param name string
@allowed([
  'basic'
  'standard'
  'standard2'
  'standard3'
  'storage_optimized_l1'
  'storage_optimized_l2'
])
param sku string
@minValue(1)
param replicaCount int
@minValue(1)
param partitionCount int
param tags object = {}

resource search 'Microsoft.Search/searchServices@2023-11-01' = {
  name: name
  location: location
  sku: {
    name: sku
  }
  properties: {
    replicaCount: replicaCount
    partitionCount: partitionCount
    hostingMode: 'default'
    semanticSearch: 'Free'
    disableLocalAuth: false
    publicNetworkAccess: 'enabled'
  }
  tags: tags
}
 
var adminKeys = search.listAdminKeys()
 
@secure()
output adminKey string = adminKeys.primaryKey
output endpoint string = 'https://${name}.search.windows.net'
output resourceId string = search.id
