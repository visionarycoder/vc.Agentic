---
metadata-version: "1.0.0"
title: "Caching Patterns for .NET"
description: "Preserve scoped source guidance for caching-patterns-dotnet."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Caching Patterns for .NET

Agent applies caching—in-memory, distributed, or hybrid—when the cache improves latency or load without hiding correctness defects.

## When to Use

| Condition | Use |
|---|---|
| Agent reduces repeated read cost | Use this skill |
| Agent caches reference data, feature data, or external responses | Use this skill |
| Agent chooses `IMemoryCache`, `IDistributedCache`, or `HybridCache` (net10+) | Use this skill |
| Agent adds expiration or invalidation strategy | Use this skill |
| Agent optimizes between local and distributed tiers | Use HybridCache for multi-tier efficiency |

## When Not to Use

| Condition | Use |
|---|---|
| Source of truth changes every request | Use direct read path |
| Defect is N+1 query or poor SQL shape | Fix query first |
| Write path or transaction consistency is main bottleneck | Use non-cache optimization |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Cached data | Yes | Value, projection, or expensive computation |
| Staleness budget | Yes | Minutes, seconds, or zero |
| Cache scope | Yes | Process-local, shared across instances, or hybrid tier |
| Invalidation trigger | No | Expiration, write success, or event |
| Target framework | No | `net10.0+` enables HybridCache; earlier versions use IMemoryCache or IDistributedCache |

## Workflow

1. Agent identifies the cached data and stale-data budget.
2. Agent selects process-local, distributed, or hybrid cache by deployment scope and framework version.
3. Agent adds explicit expiration, invalidation, and stampede control.
4. Agent verifies hit, miss, expiry, and cache-outage behavior.

Test: Run `dotnet build [project].csproj`.
Pass: Zero compile errors. Zero cache entry without explicit freshness rule in changed scope.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Shared data uses process-local cache | Use distributed cache or HybridCache with distributed backend |
| Cache key strings are copied inline | Centralize key helper |
| Write path skips invalidation | Remove, update, or tag-invalidate cache entries |
| Cache outage aborts source fallback | Use source fallback |
| HybridCache configured without distributed backend | Ensure L2 backend is registered; L1-only cache is just IMemoryCache |
| HybridCache L1 lifetime set too long | Balance between local freshness and distributed consistency |
| Tag-based invalidation overused for single-entry deletes | Use direct key deletion for individual purges, tags for grouped invalidation |

## HybridCache Configuration (.NET 10+)

Agent registers `HybridCache` with dependency injection and configures both L1 and L2 backends.

| Step | Configuration | Example |
|---|---|---|
| 1. Register distributed backend | Add `IDistributedCache` (Redis, SQL, etc.) | `services.AddStackExchangeRedisCache(...)` |
| 2. Add HybridCache service | Use `AddHybridCache()` extension | `services.AddHybridCache()` |
| 3. Configure L1 options | Set memory limits, eviction policy | `options.DefaultEntryOptions.LocalCacheDuration = TimeSpan.FromMinutes(5)` |
| 4. Inject HybridCache | Request `HybridCache` in services | `public MyService(HybridCache cache) { _cache = cache; }` |

Agent uses `GetOrCreateAsync<T>(key, factory, options, token)` for single-flight miss handling and automatic serialization.

Example:
```csharp
var value = await _cache.GetOrCreateAsync(
    "user:123",
    async ct => await _userService.GetUserAsync(123, ct),
    new HybridCacheEntryOptions
    {
        LocalCacheDuration = TimeSpan.FromMinutes(5),
        DistributedCacheDuration = TimeSpan.FromMinutes(30)
    },
    cancellationToken
);
```

## L1 vs L2 Tier Selection

| Decision | L1 (In-Memory) | L2 (Distributed) | Both (HybridCache) |
|---|---|---|---|
| Data scope | Instance-local | Shared across instances | Shared, with local fast-path |
| Staleness cost | Higher (local writes not visible to others) | Lower (all instances consistent) | Configurable per tier |
| Network cost | Zero | Per miss and invalidation | Reduced (L1 prevents L2 hits) |
| Use when | Single instance or acceptable local stale | Multi-instance consistency required | Multi-instance with high hit rate |

## Rule Matrix

| Rule | Agent verifies | Detection pattern | Fix |
|---|---|---|---|
| CACHE-001 | Cache scope matches deployment scope | Process-local cache used for shared multi-instance data | Use distributed cache |
| CACHE-002 | Every entry has explicit freshness rule | Entry added with no absolute or sliding expiration | Add expiration policy |
| CACHE-003 | Mutable data has invalidation plan | Writes succeed and stale entry remains | Remove or update cache on write |
| CACHE-004 | Key format stays centralized | Inline string keys appear across files | Move key generation to helper |
| CACHE-005 | Cache-aside path is explicit | Cache read and fill logic is duplicated | Centralize miss handling |
| CACHE-006 | Expensive misses have stampede control | Hot-key miss fans out to many source calls | Add per-key lock or single-flight pattern |
| CACHE-007 | Cache outage does not become service outage | Cache exception aborts source fallback | Fall back to source path |
| CACHE-008 | Telemetry exposes hit and miss behavior | No counters or logs for cache results | Add structured hit, miss, and eviction telemetry |

## Pattern Matrix

| Scenario | Use | Avoid |
|---|---|---|
| Single instance API | `IMemoryCache` with explicit expiration | Distributed cache without need |
| Multi-instance service | `IDistributedCache` or Redis | Process-local cache for shared data |
| Mutable reference data | Expiration plus write invalidation | No invalidation path |
| Expensive hot key | Cache-aside plus stampede control | Unbounded concurrent misses |
| Multi-tier (.NET 10+) | `HybridCache` for L1 local + L2 distributed | Manual two-tier coordination |
| L1 miss amplification (.NET 10+) | `HybridCache` GetOrCreateAsync with single-flight deduplication | Concurrent backend floods on same key miss |

## HybridCache Overview (.NET 10+)

`HybridCache` provides automatic multi-tier caching: L1 (in-process) + L2 (distributed backend). Requires `net10.0` or later.

| Feature | Behavior | Impact |
|---|---|---|
| Automatic L1 + L2 | In-memory tier checked first; distributed backend as fallback | Reduces distributed cache load and latency |
| Single-flight for missing keys | Concurrent miss requests await one backend call | Eliminates cache-stampede amplification on hot misses |
| Serialization abstraction | Agent provides value factory; HybridCache handles serialization to L2 | Simplifies per-key logic; automatic L1/L2 invalidation |
| L1 size and lifetime | Set per cache instance via options | Configure `IMemoryCache` behaviors independently |
| Tag-based invalidation | Invalidate groups by tag; applies to both L1 and L2 | Coordinated multi-entry purge without individual keys |

## Verification Matrix

| Test | Run | Pass |
|---|---|---|
| Compile verification | `dotnet build [project].csproj` | Zero compile errors |
| Scope verification | Search changed files for inline cache keys or entries with no expiration | Zero unauthorized matches |
| Behavior verification | Run `dotnet test [test-project].csproj --filter Cache` when tests exist | Zero failing tests |

## Verification Checklist

Agent verifies:
- [ ] Cache scope matches deployment scope
- [ ] Every entry has explicit expiration or invalidation
- [ ] Mutable data has cache update or removal path
- [ ] Expensive misses use stampede control when load warrants it
- [ ] Telemetry exposes hit, miss, and cache-outage behavior

## C# 14+ Caching Patterns (.NET 10)

Agent uses modern language features in caching implementations. See `references/csharp14-patterns.md` for:
- Primary constructors with required members
- Collection expressions for cache tag sets
- File-scoped types for cache key constants
- Params collections with minimal allocations

Showcase these patterns when implementing caching services to demonstrate current platform capabilities.
