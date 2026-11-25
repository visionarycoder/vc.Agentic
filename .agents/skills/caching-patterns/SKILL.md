---
name: "caching-patterns"
description: "Choose cache scope, expiration, invalidation, two-tier layering, and stampede control so caching improves latency or load without hiding correctness defects."
metadata:
  metadata-version: "1.0.0"
  title: "Caching Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-24"
  collection: "optional"
---

# Caching Patterns

Add a cache only when it reduces repeated read cost and the staleness budget is known.

## When Not to Cache

| Condition | Action |
|---|---|
| Source of truth changes on every request | Use the direct read path |
| Defect is an N+1 query or poor query shape | Fix the query first |
| Write path or transaction consistency is the bottleneck | Use a non-cache optimization |

## Required Inputs

| Input | Notes |
|---|---|
| Cached data | Value, projection, or expensive computation |
| Staleness budget | Minutes, seconds, or zero |
| Cache scope | Process-local, shared across instances, or two-tier |
| Invalidation trigger | Expiration, write success, or event |
| Stampede protection | Required for hot keys and expensive misses |

## Scope Decision

| Scenario | Choice |
|---|---|
| Single instance | Process-local cache |
| Multiple instances, read-heavy | Two-tier cache: local tier (L1) plus shared tier (L2) |
| Multiple instances, write-heavy or high consistency | Shared tier only, no local tier |
| Static reference data | Long TTL, optionally seeded at startup |
| Rapidly changing data | Short TTL or bypass |
| Per-user session state | Shared tier, so it survives instance loss |
| Hot key with expensive source | Per-key single-flight (one loader per key) |

Prefer a library that provides two-tier layering, single-flight, and tag invalidation over a hand-written wrapper.

## Two-Tier Expiration

- L1 expiration is 10-20% of L2 expiration, which limits cross-instance staleness.
- L2 expiration matches the staleness tolerance of the source.
- Write invalidation removes both tiers.

## Invalidation Strategies

| Strategy | Use when | Trade-off |
|---|---|---|
| Invalidate on write (cache-aside) | Reads dominate and brief staleness after a write is acceptable | Simple write path; next read misses |
| Write-through | Read-after-write freshness is required and writes are infrequent | No miss after write; higher write latency and coordination |
| Seeding at startup | Static, small, predictable working set | No cold misses; load spike on the source at startup, unsuitable for large or dynamic sets |

## Rules

| Rule | Verify | Fix |
|---|---|---|
| CACHE-001 | Cache scope matches deployment scope | Do not use process-local cache for shared multi-instance data |
| CACHE-002 | Every entry has an explicit freshness rule | Add absolute or sliding expiration |
| CACHE-003 | Mutable data has an invalidation plan | Remove or update the entry on write |
| CACHE-004 | Key format is centralized | Move key generation to one helper |
| CACHE-005 | Miss handling is not duplicated | Centralize the cache-aside path |
| CACHE-006 | Expensive misses have stampede control | Add per-key single-flight |
| CACHE-007 | A cache outage does not become a service outage | Fall back to the source |
| CACHE-008 | Hits, misses, and evictions are observable | Add structured telemetry |
| CACHE-009 | L1 expiration is shorter than L2 | Set L1 to 10-20% of L2 |
| CACHE-010 | Bulk invalidation uses tags or key prefixes | Replace manual key enumeration |

## Verification

| Check | Pass |
|---|---|
| Search changed code for inline keys and entries without expiration | No unauthorized matches |
| Hit, miss, expiry, and cache-outage tests | Behavior matches the staleness budget; outage falls back to the source |
| Compare chosen design with the scope decision | Selection matches deployment and consistency needs |
