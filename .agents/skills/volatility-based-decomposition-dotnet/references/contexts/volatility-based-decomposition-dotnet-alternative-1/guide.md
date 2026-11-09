---
metadata-version: "1.0.0"
title: "Volatility-Based Decomposition for .NET"
description: "Preserve scoped source guidance for volatility-based-decomposition-dotnet."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Volatility-Based Decomposition for .NET

## Overview

Volatility-based decomposition (VBD) organizes systems by _where change occurs_, not by functional domains. Components encapsulate areas of volatility—aspects likely to change together or frequently—so changes remain contained rather than rippling across the system.

For consistency with Lowy's guidance and the rest of this repository, **VBD always expands to Volatility-Based Decomposition**.

This skill implements VBD using a three-layer component taxonomy (Manager/Engine/Access) with strict communication rules, Contract/Service project separation, and RPC-based inter-component communication. The goal: maximize reuse, minimize coupling, and isolate change.

Repository guardrails used by this skill:

- Never use underscore prefixes.
- In .NET 10+ projects, prefer primary constructors and C# 14+ features.
- In .NET Standard 2.0 and Roslyn projects, use C# 8 features.

## Core Principles

### Volatility vs. Variability

- **Volatility** = _type of activity_ (e.g., data access, validation, orchestration)
- **Variability** = _domain differences_ (e.g., Customer vs. Order)

Decompose by volatility, not variability. A `ValidatingEngine` applies to many domains; a `CustomerManager` ties you to one domain and limits reuse.

### Why VBD Matters

Functional decomposition groups by features (e.g., "OrderProcessing", "Inventory"). When requirements change, modifications cascade across multiple components because functionality is spread out. VBD encapsulates the _reason for change_—when business rules change, only Engine components update; when data storage changes, only Access components update.

## Component Taxonomy

### Manager Components

**Purpose:** Orchestrate workflows by composing Engine and Access components.

**Naming:** `<Activity>Manager` (e.g., `DataManager`, `ReportingManager`, `IntegrationManager`)

**Responsibilities:**

- Coordinate multi-step workflows
- Route requests to appropriate Engines and Access components
- Handle cross-cutting orchestration logic
- Aggregate results from multiple lower-layer components

**Communication rules:**

- Can call Engine and Access components
- Can call other Managers _only through an external message bus_ (never direct references)
- Clients reference only Manager contracts

**Example:**

```csharp
public interface IDataManager
{
    Task<ValidationResult<T>> ValidateAndStore<T>(T entity, StorageOptions options);
}

public class DataManager(IValidatingEngine validatingEngine, IStoringAccess storingAccess) : IDataManager
{
    public async Task<ValidationResult<T>> ValidateAndStore<T>(T entity, StorageOptions options)
    {
        var validationResult = await validatingEngine.ValidateAsync(entity);
        if (!validationResult.IsValid) return validationResult;

        await storingAccess.SaveAsync(entity, options);
        return validationResult;
    }
}
```

### Engine Components

**Purpose:** Apply business rules, calculations, transformations, and logic.

**Naming:** Use gerund form: `<Action>ingEngine` (e.g., `ValidatingEngine`, `CalculatingEngine`, `AggregatingEngine`, `TransformingEngine`)

**Responsibilities:**

- Object validation
- Business rule enforcement
- Data transformation and mapping
- Aggregation and calculation
- Stateless operations

**Communication rules:**

- Can call Access components
- Cannot call Managers or other Engines in the same layer

**Example:**

```csharp
public interface IValidatingEngine
{
    Task<ValidationResult<T>> ValidateAsync<T>(T entity);
}

public class ValidatingEngine(IRuleAccess ruleAccess) : IValidatingEngine
{
    public async Task<ValidationResult<T>> ValidateAsync<T>(T entity)
    {
        var rules = await ruleAccess.GetRulesForType<T>();
        var errors = new List<string>();

        foreach (var rule in rules)
        {
            if (!rule.Evaluate(entity))
                errors.Add(rule.ErrorMessage);
        }

        return new ValidationResult<T>(entity, !errors.Any(), errors);
    }
}
```

### Access Components

**Purpose:** Abstract all external resource interactions.

**Naming:** `<Resource>Access` (e.g., `DatabaseAccess`, `FileAccess`, `ApiAccess`, `CacheAccess`)

**Responsibilities:**

- Database queries and commands
- File system operations
- Third-party API calls
- Message queue interactions
- Cache operations

**Communication rules:**

- Can only communicate with external resources
- Cannot call other components

**Example:**

```csharp
public interface IDatabaseAccess
{
    Task<T> GetByIdAsync<T>(Guid id) where T : class;
    Task SaveAsync<T>(T entity) where T : class;
    Task<IEnumerable<T>> QueryAsync<T>(FilterCriteria filter) where T : class;
}

public class DatabaseAccess(DbContext dbContext) : IDatabaseAccess
{
    public async Task<T> GetByIdAsync<T>(Guid id) where T : class
    {
        return await dbContext.Set<T>().FindAsync(id);
    }

    public async Task SaveAsync<T>(T entity) where T : class
    {
        dbContext.Set<T>().Add(entity);
        await dbContext.SaveChangesAsync();
    }

    public async Task<IEnumerable<T>> QueryAsync<T>(FilterCriteria filter) where T : class
    {
        // Apply filter logic
        return await dbContext.Set<T>().ToListAsync();
    }
}
```

## Project Structure

### Naming Convention

`<Volatility-Type>.<Capability>.<Implementation>`

- **Volatility-Type:** Layer/category of change (for example: `Manager`, `Engine`, `Access`)
- **Capability:** Gerund activity name (for example: `Orchestrating`, `Validating`, `Transforming`, `Storing`)
- **Implementation:** `Contract`, `Service`, `Orm`, `Simulator`, or `Emulator`

### Example Structure

```
Engine.Validating.Contract/
  IValidatingEngine.cs
  ValidationRequest.cs
  ValidationResult.cs

Engine.Validating.Service/
  ValidatingEngine.cs
  Internal/
    RuleEvaluator.cs
    ValidationMapper.cs

Access.Storing.Contract/
    IStoringAccess.cs
  StorageOptions.cs
  FilterCriteria.cs

Access.Storing.Service/
  DatabaseAccess.cs
  FileAccess.cs

Access.Storing.Orm/
  Entities/
  Configurations/

Manager.Orchestrating.Contract/
    IOrchestratingManager.cs
    OrchestrationRequest.cs
    OrchestrationResponse.cs

Manager.Orchestrating.Service/
    OrchestratingManager.cs

Infrastructure.Ifx/
  Constants/
  Extensions/
  Helpers/

Infrastructure.Utilities/
  Logging/
  Serialization/
```

## Contract Design

### Interface Exposure

Contract projects expose interfaces aligned with layer + gerund capability:

```csharp
// Engine.Validating.Contract
public interface IValidatingEngine
{
    Task<ValidationResult<T>> ValidateAsync<T>(ValidationRequest<T> request);
}

// Access.Storing.Contract
public interface IStoringAccess
{
    Task<StorageResult<T>> SaveAsync<T>(StorageRequest<T> request);
    Task<T> RetrieveAsync<T>(RetrievalRequest request);
}
```

### Use Generics to Minimize Surface Area

Prefer generic methods over type-specific overloads:

```csharp
// Good: Single generic method
Task<ValidationResult<T>> ValidateAsync<T>(T entity);

// Avoid: Type-specific methods
Task<ValidationResult<Customer>> ValidateCustomer(Customer customer);
Task<ValidationResult<Order>> ValidateOrder(Order order);
```

### Message Envelopes

Wrap arguments in request/response envelopes:

```csharp
public class ValidationRequest<T>
{
    public T Entity { get; set; }
    public ValidationOptions Options { get; set; }
    public Dictionary<string, object> Context { get; set; }
}

public class ValidationResult<T>
{
    public T Entity { get; set; }
    public bool IsValid { get; set; }
    public IEnumerable<string> Errors { get; set; }
    public Dictionary<string, object> Metadata { get; set; }
}
```

### Filter Objects for Query Flexibility

```csharp
public class FilterCriteria
{
    public Expression<Func<T, bool>> Predicate { get; set; }
    public PaginationOptions Pagination { get; set; }
    public SortOptions Sort { get; set; }
}

public class PaginationOptions
{
    public int PageNumber { get; set; }
    public int PageSize { get; set; }
}
```

## Service Implementation

### Keep Internals Hidden

Place mappers, converters, and helpers in `Internal/` folders or use `internal` access modifiers:

```csharp
// Engine.Validating.Service/Internal/ValidationMapper.cs
internal static class ValidationMapper
{
    internal static ValidationResult<T> ToResult<T>(T entity, List<string> errors)
    {
        return new ValidationResult<T>
        {
            Entity = entity,
            IsValid = !errors.Any(),
            Errors = errors
        };
    }
}
```

### ServiceModel Decoration

For WCF/CoreWCF RPC, decorate service implementations with `[ServiceContract]` and `[OperationContract]`:

```csharp
[ServiceContract]
public interface IValidatingData
{
    [OperationContract]
    Task<ValidationResult<T>> ValidateAsync<T>(ValidationRequest<T> request);
}
```

## Dependency Injection Setup

### Registration by Layer

Organize registrations with extension methods:

```csharp
// Engine.Validating.Service/ServiceCollectionExtensions.cs
public static class ValidationServiceExtensions
{
    public static IServiceCollection AddValidationServices(this IServiceCollection services)
    {
        services.AddScoped<IValidatingEngine, ValidatingEngine>();
        return services;
    }
}

// Access.Storing.Service/ServiceCollectionExtensions.cs
public static class StorageServiceExtensions
{
    public static IServiceCollection AddStorageServices(this IServiceCollection services)
    {
        services.AddScoped<IDatabaseAccess, DatabaseAccess>();
        services.AddScoped<IFileAccess, FileAccess>();
        return services;
    }
}

// Manager.Orchestrating.Service/ServiceCollectionExtensions.cs
public static class DataManagementExtensions
{
    public static IServiceCollection AddDataManagement(this IServiceCollection services)
    {
        services.AddScoped<IDataManager, DataManager>();
        return services;
    }
}
```

### Hosting Project

Create a hosting project to wire everything together:

```csharp
var builder = WebApplication.CreateBuilder(args);

// Register components by layer
builder.Services.AddStorageServices();
builder.Services.AddValidationServices();
builder.Services.AddDataManagement();

// Configure CoreWCF if using RPC
builder.Services.AddServiceModelServices();
builder.Services.AddServiceModelMetadata();

var app = builder.Build();

// Configure CoreWCF endpoints
app.UseServiceModel(serviceBuilder =>
{
    serviceBuilder.AddService<DataManager>();
    serviceBuilder.AddServiceEndpoint<DataManager, IDataManager>(
        new BasicHttpBinding(),
        "/DataService");
});

app.Run();
```

## RPC Communication

### CoreWCF for Modern .NET

Use CoreWCF (Microsoft-supported) for WCF-style RPC on .NET 8+. CoreWCF 1.9+ supports .NET 8, .NET 9, and .NET 10.

**Install packages:**

```bash
dotnet add package CoreWCF.Http
dotnet add package CoreWCF.Primitives
```

**Configure endpoints:**

```csharp
app.UseServiceModel(builder =>
{
    builder.AddService<DataManager>(options =>
    {
        options.DebugBehavior.IncludeExceptionDetailInFaults = isDevelopment;
    });

    builder.AddServiceEndpoint<DataManager, IDataManager>(
        new BasicHttpBinding(BasicHttpSecurityMode.Transport),
        "/api/data");
});
```

### Allow Communication Flexibility

While RPC provides type safety and contract-first design, structure your components so communication mechanisms can be swapped. Keep service interfaces clean and avoid WCF-specific attributes in Contract projects when possible. Consider providing both RPC and REST endpoints from the same implementation.

## Avoid Feature Silos

Don't create `CustomerValidationEngine` and `OrderValidationEngine`. Create one `ValidatingEngine` that works generically across all domains. Volatility is about _activity type_, not domain.

**Bad (domain-specific):**

```csharp
public interface ICustomerValidator { }
public interface IOrderValidator { }
public interface IProductValidator { }
```

**Good (activity-specific):**

```csharp
public interface IValidatingEngine
{
    Task<ValidationResult<T>> ValidateAsync<T>(T entity);
}
```

The same engine validates customers, orders, products—any type. Rules come from Access components, not hardcoded into domain-specific engines.

## Utility and Infrastructure Projects

### Utility Projects

Non-business, reusable logic:

```
Infrastructure.Utilities/
  Logging/
  Serialization/
  Compression/
  Encryption/
```

### Ifx Projects

Application-specific helpers and constants:

```
Infrastructure.Ifx/
  Constants/
    ErrorCodes.cs
    ConfigKeys.cs
  Extensions/
    StringExtensions.cs
    EnumerableExtensions.cs
  Helpers/
    DateTimeHelper.cs
```

## Technology Choices

- **Target:** Latest stable .NET (currently .NET 8+)
- **Prefer:** Built-in .NET libraries and Microsoft-maintained packages
- **RPC:** CoreWCF for WCF-style services (Microsoft-supported as of 2022)
- **DI:** Built-in `Microsoft.Extensions.DependencyInjection`
- **ORM:** Entity Framework Core for database access

Follow Microsoft best practices. When choosing between third-party and Microsoft-provided solutions, default to Microsoft unless there's a compelling reason otherwise.

## Communication Rules Summary

| Layer       | Can Call                                       |
| ----------- | ---------------------------------------------- |
| **Client**  | Manager.Contract only                          |
| **Manager** | Engine, Access, other Managers via message bus |
| **Engine**  | Access only                                    |
| **Access**  | External resources only                        |

No horizontal communication within a layer. No upward calls (Access can't call Engine; Engine can't call Manager).

## Example: Complete Component

```csharp
// Manager.Processing.Contract/IProcessingManager.cs
public interface IProcessingData
{
    Task<ProcessingResult<T>> ProcessAsync<T>(ProcessingRequest<T> request);
}

public class ProcessingRequest<T>
{
    public T Data { get; set; }
    public ProcessingOptions Options { get; set; }
}

public class ProcessingResult<T>
{
    public T ProcessedData { get; set; }
    public bool Success { get; set; }
    public IEnumerable<string> Messages { get; set; }
}

// Manager.Processing.Service/ProcessingManager.cs
public class ProcessingManager(
    IValidatingEngine validatingEngine,
    ITransformingEngine transformingEngine,
    IStoringAccess storingAccess) : IProcessingData
{
    public async Task<ProcessingResult<T>> ProcessAsync<T>(ProcessingRequest<T> request)
    {
        // Validate
        var validationResult = await validatingEngine.ValidateAsync(request.Data);
        if (!validationResult.IsValid)
        {
            return new ProcessingResult<T>
            {
                Success = false,
                Messages = validationResult.Errors
            };
        }

        // Transform
        var transformedData = await transformingEngine.TransformAsync(
            request.Data,
            request.Options.TransformationRules);

        // Store
        await storingAccess.SaveAsync(transformedData);

        return new ProcessingResult<T>
        {
            ProcessedData = transformedData,
            Success = true
        };
    }
}

// Registration
public static IServiceCollection AddProcessingServices(this IServiceCollection services)
{
    services.AddScoped<IProcessingData, ProcessingManager>();
    return services;
}
```

This manager orchestrates validation, transformation, and storage—three distinct volatilities—without knowing their implementations. When validation rules change, only the `ValidatingEngine` updates. When storage moves from SQL to NoSQL, only `StoringAccess` changes. The manager remains stable.
