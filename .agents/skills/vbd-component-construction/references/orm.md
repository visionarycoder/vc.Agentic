---
title: Access ORM Scaffold
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Access ORM Scaffold

ORM projects exist only inside Access components.

## Project naming

For each symbolic resource:

```text
Access.<Capability>.Orm.<SymbolicResource>
```

Do not encode the physical database/container name in the project name.

## Required folders

Create these folders in each ORM project even when initially empty:

```text
Configuration/
Models/
```

Do not create `Models` folders in Contract or Service projects during component construction.

## Resource context

Create:

```text
<SymbolicResource>Context.cs
```

Pattern:

```csharp
public sealed class FinancialContext(
    DbContextOptions<FinancialContext> options)
    : DbContext(options)
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(GetType().Assembly);
    }
}
```

The context is intentionally dumb.

Do not generate:

- placeholder `DbSet<T>` properties
- `OnConfiguring`
- connection strings
- provider selection
- physical database names
- entities
- provider-specific behavior

Provider binding belongs to runtime/module implementation work, not this scaffold.

## References

Add automatically:

```text
Access.<Capability>.Service
    -> Access.<Capability>.Orm.<SymbolicResource>
```

Never add:

```text
Access.<Capability>.Contract
    -> Access.<Capability>.Orm.<SymbolicResource>
```

## Tests

Create:

```text
Access.<Capability>.Orm.<SymbolicResource>.IntegrationTests
```

Reference the ORM project only, not Service.
