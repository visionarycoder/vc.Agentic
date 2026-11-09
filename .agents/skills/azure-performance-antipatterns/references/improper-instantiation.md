---
title: Improper Instantiation Anti-Pattern Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: azure-performance-antipatterns
---

# Improper Instantiation Anti-Pattern

## Description

Creating and destroying shared or expensive objects for each operation instead of reusing them through dependency injection or factories.

## Detection Signals

- `new DbContext()` or `new HttpClient()` per operation
- New serializer, regex, or mapping configuration inside hot paths
- Transient creation of expensive clients that hold sockets or buffers
- Per-request object churn drives Gen 0 and Gen 1 collections
- Connection setup repeats for every call

## Why This Is Problematic

- Allocation rate rises without user value
- Garbage collection interrupts throughput
- Socket and connection reuse disappear
- Shared configuration scatters across the codebase

## Remediation

**Use DI lifetimes for shared services:**

```csharp
// ❌ BEFORE: New client and context for each operation
public sealed class InventorySyncService
{
    public async Task SyncAsync(CancellationToken cancellationToken)
    {
        using var context = new AppDbContext();
        using var client = new HttpClient { BaseAddress = new Uri("https://inventory") };

        var items = await client.GetFromJsonAsync<List<ItemDto>>("/items", cancellationToken);
        context.Items.UpdateRange(items!.Select(Map));
        await context.SaveChangesAsync(cancellationToken);
    }
}

// ✅ AFTER: Reuse injected dependencies
public sealed class InventorySyncService(
    AppDbContext context,
    HttpClient client)
{
    public async Task SyncAsync(CancellationToken cancellationToken)
    {
        var items = await client.GetFromJsonAsync<List<ItemDto>>("/items", cancellationToken);
        context.Items.UpdateRange(items!.Select(Map));
        await context.SaveChangesAsync(cancellationToken);
    }
}
```

**Register the correct lifetimes:**

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("App")));

builder.Services.AddHttpClient<InventorySyncService>(client =>
{
    client.BaseAddress = new Uri("https://inventory");
});
```

## Verification

Test: Capture allocation rate, GC collections, and outbound socket usage during a load test.
Pass: Allocation rate drops. GC frequency drops. Outbound connection reuse increases.

## Reference

[Improper Instantiation Anti-Pattern - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/improper-instantiation/)
