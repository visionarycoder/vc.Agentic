---
title: C# 14+ Caching Examples
doc_type: reference
status: active
last_updated: 2026-08-15
---

# C# 14+ Caching Patterns

Modern language features in .NET 10 caching implementations.

## Primary Constructor with Required Members

```csharp
// User entity with required fields for cache validation
file record CachedUser(required int Id, required string Name, required string Email)
{
    public DateTime CachedAt { get; init; } = DateTime.UtcNow;
}

// Caching service with primary constructor and hybrid cache
public class UserCacheService(HybridCache cache, IUserRepository repo)
{
    public async ValueTask<CachedUser?> GetUserAsync(int id, CancellationToken ct)
    {
        return await cache.GetOrCreateAsync(
            $"user-{id}",
            async cancel => new CachedUser(
                Id: id,
                Name: await repo.GetNameAsync(id, cancel),
                Email: await repo.GetEmailAsync(id, cancel)
            ),
            flags: HybridCacheEntryFlags.None,
            cancellationToken: ct
        );
    }
}
```

## Collection Expressions for Cache Tag Sets

```csharp
// Use collection expressions instead of .ToList() or .ToArray()
public class CacheTagManager(IDistributedCache cache)
{
    public async Task InvalidateUserTagsAsync(int userId, CancellationToken ct)
    {
        // C# 14 collection expression syntax for tag collections
        var tags = [
            $"user-{userId}",
            $"user-profile-{userId}",
            $"permissions-{userId}"
        ];

        foreach (var tag in tags)
        {
            await cache.RemoveAsync(tag, ct);
        }
    }
}
```

## File-Scoped Type for Cache Key Constants

```csharp
// Hide internal cache key structure in file scope
file static class CacheKeyFormats
{
    internal const string UserFormat = "user-{0}";
    internal const string OrderFormat = "order-{0}";
    internal const string SessionFormat = "session-{0}";
}

// Use directly in this file, hidden from public API
public string BuildUserKey(int id) => string.Format(CacheKeyFormats.UserFormat, id);
```

## Params Collections with Span<T>

```csharp
// Accept multiple cache entries with minimal allocations
public class BulkCacheInvalidator(IDistributedCache cache)
{
    public async Task InvalidateAsync(CancellationToken ct, params string[] keys)
    {
        // Execute invalidations in parallel for performance
        await Task.WhenAll(keys.Select(key => cache.RemoveAsync(key, ct)));
    }
}
```
