---
title: No Caching Anti-Pattern Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: azure-performance-antipatterns
---

# No Caching Anti-Pattern

## Description

Repeatedly executing the same expensive read path instead of serving stable data from a cache with explicit expiration.

## Detection Signals

- Frequently accessed static data bypasses cache
- Same query runs for every request with identical parameters
- Lookup tables, configuration values, or product metadata load from the source every time
- Expensive upstream call dominates repeated read latency
- Hot read endpoints hit the database at the same rate as request volume

## Why This Is Problematic

- Repeated I/O consumes database and network capacity
- Response time stays bound to the slowest dependency
- Traffic bursts amplify load on the origin system
- Memory and CPU waste cycles on duplicate materialization

## Remediation

**Cache hot local reads with `IMemoryCache`:**

```csharp
// ❌ BEFORE: Always reads the database
public async Task<ProductCatalogDto> GetCatalogAsync(CancellationToken cancellationToken)
{
    var products = await _context.Products
        .AsNoTracking()
        .OrderBy(p => p.Name)
        .ToListAsync(cancellationToken);

    return new ProductCatalogDto(products);
}

// ✅ AFTER: Reuse cached result with expiration
public async Task<ProductCatalogDto> GetCatalogAsync(CancellationToken cancellationToken)
{
    return await _memoryCache.GetOrCreateAsync("catalog:v1", async entry =>
    {
        entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10);
        entry.SlidingExpiration = TimeSpan.FromMinutes(2);

        var products = await _context.Products
            .AsNoTracking()
            .OrderBy(p => p.Name)
            .ToListAsync(cancellationToken);

        return new ProductCatalogDto(products);
    }) ?? new ProductCatalogDto(Array.Empty<Product>());
}
```

**Use `IDistributedCache` for shared instances:**

```csharp
public async Task<ExchangeRateDto?> GetRateAsync(string currencyPair, CancellationToken cancellationToken)
{
    string cacheKey = $"fx:{currencyPair}";
    string? cached = await _distributedCache.GetStringAsync(cacheKey, cancellationToken);

    if (cached is not null)
    {
        return JsonSerializer.Deserialize<ExchangeRateDto>(cached);
    }

    ExchangeRateDto rate = await _ratesClient.GetRateAsync(currencyPair, cancellationToken);

    await _distributedCache.SetStringAsync(
        cacheKey,
        JsonSerializer.Serialize(rate),
        new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
        },
        cancellationToken);

    return rate;
}
```

## Verification

Test: Measure dependency call count, cache hit ratio, and median read latency under repeated requests.
Pass: Cache hit ratio rises after warm-up. Dependency call count drops. Median read latency decreases.

## Reference

[No Caching Anti-Pattern - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/no-caching/)
