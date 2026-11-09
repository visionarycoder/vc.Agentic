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

Agent applies caching only when the cache improves latency or load without hiding correctness defects.

## When to Use

| Condition | Use |
|---|---|
| Agent reduces repeated read cost | Use this skill |
| Agent caches reference data, feature data, or external responses | Use this skill |
| Agent chooses `IMemoryCache` or `IDistributedCache` | Use this skill |
| Agent adds expiration or invalidation strategy | Use this skill |

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
| Cache scope | Yes | Process-local or shared across instances |
| Invalidation trigger | No | Expiration, write success, or event |

## Workflow

1. Agent identifies the cached data and stale-data budget.
2. Agent selects process-local or distributed cache by deployment scope.
3. Agent adds explicit expiration, invalidation, and stampede control.
4. Agent verifies hit, miss, expiry, and cache-outage behavior.

Test: Run `dotnet build [project].csproj`.
Pass: Zero compile errors. Zero cache entry without explicit freshness rule in changed scope.

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

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Shared data uses process-local cache | Use distributed cache |
| Cache key strings are copied inline | Centralize key helper |
| Write path skips invalidation | Remove or update cache entry |
| Cache outage aborts source fallback | Use source fallback |
