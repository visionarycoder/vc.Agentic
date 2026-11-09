# Bicep Generation Patterns

Generate Azure infrastructure as code from service boundary definitions.

## Core Principle

Each service boundary generates its own Bicep module with all required Azure resources. Boundaries deploy independently.

## Boundary Deployment Structure

```
{Boundary}.Deployment/
  main.bicep              — Entry point, orchestrates modules
  modules/
    appService.bicep      — App Service hosting
    storage.bicep         — Storage accounts
    keyVault.bicep        — Secrets and keys
    serviceBus.bicep      — Messaging infrastructure
    sql.bicep             — Database resources
  parameters/
    dev.bicepparam        — Dev environment params
    prod.bicepparam       — Prod environment params
```

## Main Bicep Template

```bicep
targetScope = 'resourceGroup'

@description('Environment name (dev, staging, prod)')
param environmentName string

@description('Location for all resources')
param location string = resourceGroup().location

@description('Boundary name')
var boundaryName = '{{BoundaryName}}'
var resourcePrefix = '${boundaryName}-${environmentName}'

// Key Vault for secrets
module keyVault 'modules/keyVault.bicep' = {
  name: '${boundaryName}-keyvault-deployment'
  params: {
    keyVaultName: '${resourcePrefix}-kv'
    location: location
  }
}

// Storage for boundary data
module storage 'modules/storage.bicep' = {
  name: '${boundaryName}-storage-deployment'
  params: {
    storageAccountName: replace('${resourcePrefix}-storage', '-', '')
    location: location
  }
}

// App Service hosting
module appService 'modules/appService.bicep' = {
  name: '${boundaryName}-appservice-deployment'
  params: {
    appServiceName: '${resourcePrefix}-app'
    location: location
    keyVaultName: keyVault.outputs.keyVaultName
  }
}

output appServiceUrl string = appService.outputs.appServiceUrl
output keyVaultName string = keyVault.outputs.keyVaultName
```

## App Service Module

```bicep
param appServiceName string
param location string
param keyVaultName string

var appServicePlanName = '${appServiceName}-plan'

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  properties: {
    reserved: true // Linux
  }
}

resource appService 'Microsoft.Web/sites@2022-03-01' = {
  name: appServiceName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOTNETCORE|8.0'
      alwaysOn: true
      ftpsState: 'Disabled'
      appSettings: [
        {
          name: 'KeyVaultName'
          value: keyVaultName
        }
      ]
    }
  }
}

output appServiceUrl string = 'https://${appService.properties.defaultHostName}'
output appServicePrincipalId string = appService.identity.principalId
```

## Key Vault Module

```bicep
param keyVaultName string
param location string

resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
  }
}

output keyVaultName string = keyVault.name
output keyVaultUri string = keyVault.properties.vaultUri
```

## Storage Module

```bicep
param storageAccountName string
param location string

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: 'data'
  properties: {
    publicAccess: 'None'
  }
}

output storageAccountName string = storageAccount.name
output blobEndpoint string = storageAccount.properties.primaryEndpoints.blob
```

## Service Bus Module

```bicep
param serviceBusNamespaceName string
param location string
param queueNames array = []
param topicNames array = []

resource serviceBusNamespace 'Microsoft.ServiceBus/namespaces@2022-10-01-preview' = {
  name: serviceBusNamespaceName
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
}

resource queues 'Microsoft.ServiceBus/namespaces/queues@2022-10-01-preview' = [for queueName in queueNames: {
  parent: serviceBusNamespace
  name: queueName
  properties: {
    maxDeliveryCount: 10
    lockDuration: 'PT5M'
  }
}]

resource topics 'Microsoft.ServiceBus/namespaces/topics@2022-10-01-preview' = [for topicName in topicNames: {
  parent: serviceBusNamespace
  name: topicName
}]

output serviceBusNamespaceName string = serviceBusNamespace.name
output serviceBusEndpoint string = serviceBusNamespace.properties.serviceBusEndpoint
```

## SQL Database Module

```bicep
param sqlServerName string
param sqlDatabaseName string
param location string
param administratorLogin string

@secure()
param administratorPassword string

resource sqlServer 'Microsoft.Sql/servers@2023-05-01-preview' = {
  name: sqlServerName
  location: location
  properties: {
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorPassword
    minimalTlsVersion: '1.2'
  }
}

resource sqlDatabase 'Microsoft.Sql/servers/databases@2023-05-01-preview' = {
  parent: sqlServer
  name: sqlDatabaseName
  location: location
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
  }
}

resource firewallRule 'Microsoft.Sql/servers/firewallRules@2023-05-01-preview' = {
  parent: sqlServer
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

output sqlServerFqdn string = sqlServer.properties.fullyQualifiedDomainName
output sqlDatabaseName string = sqlDatabase.name
```

## Parameter Files

**dev.bicepparam:**
```bicep
using './main.bicep'

param environmentName = 'dev'
param location = 'eastus'
```

**prod.bicepparam:**
```bicep
using './main.bicep'

param environmentName = 'prod'
param location = 'eastus'
```

## Generator Implementation

```csharp
public static string GenerateBicepDeployment(BoundaryDefinition boundary)
{
    var modules = new List<string>();

    if (boundary.RequiresStorage)
        modules.Add(GenerateStorageModule(boundary));

    if (boundary.RequiresDatabase)
        modules.Add(GenerateSqlModule(boundary));

    if (boundary.RequiresMessaging)
        modules.Add(GenerateServiceBusModule(boundary));

    modules.Add(GenerateKeyVaultModule(boundary));
    modules.Add(GenerateAppServiceModule(boundary));

    return GenerateMainBicep(boundary, modules);
}
```

## Deployment Scripts

Generate deployment scripts alongside Bicep:

**deploy.sh:**
```bash
#!/bin/bash
set -e

ENVIRONMENT=$1
RESOURCE_GROUP="{{BoundaryName}}-${ENVIRONMENT}-rg"
LOCATION="eastus"

echo "Deploying {{BoundaryName}} to ${ENVIRONMENT}"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy Bicep
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file main.bicep \
  --parameters parameters/${ENVIRONMENT}.bicepparam

echo "Deployment complete"
```

## Testing Bicep

Generate test scripts:

```bash
#!/bin/bash
# Validate Bicep syntax
az bicep build --file main.bicep

# What-if deployment
az deployment group what-if \
  --resource-group test-rg \
  --template-file main.bicep \
  --parameters parameters/dev.bicepparam
```

## Multi-Boundary Orchestration

When multiple boundaries need coordination:

```bicep
targetScope = 'subscription'

param environmentName string
param location string = 'eastus'

// Deploy each boundary
module billingBoundary 'boundaries/Billing/main.bicep' = {
  name: 'billing-deployment'
  scope: resourceGroup('billing-${environmentName}-rg')
  params: {
    environmentName: environmentName
    location: location
  }
}

module orderBoundary 'boundaries/Order/main.bicep' = {
  name: 'order-deployment'
  scope: resourceGroup('order-${environmentName}-rg')
  params: {
    environmentName: environmentName
    location: location
  }
}
```
