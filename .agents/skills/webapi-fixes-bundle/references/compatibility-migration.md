---
title: Compatibility Migration Playbook
doc_type: reference
status: active
last_updated: 2026-08-14
---

# Compatibility Migration

Migrate legacy endpoints while preserving backward compatibility; retire old contracts with deprecation warnings.

## Patterns

| Pattern | Issue | Fix |
|---|---|---|
| Direct rename breaks clients | Endpoint `/api/users/{id}` renamed to `/api/v2/users/{id}` with no redirect | Keep old route alongside new; use `[Obsolete]` or `Deprecated` header |
| Contract change without versioning | Property renamed or type changed without warning | Version API or create adapter endpoint that maps old contract to new |
| No deprecation timeline | Legacy endpoint removed without notice | Add deprecation header with sunset date; give clients migration window |
| Silent compatibility break | Old clients continue calling removed endpoint, silently fail | Return 410 Gone with migration guidance or proxy to new endpoint |
| No adapter path | Clients must rewrite all calls to use new contract | Create compatibility endpoint that translates old request to new, returns mapped response |

## Verification

Test: Call deprecated endpoint with old client; verify redirect or compatibility response.
Pass: Old contract remains callable until retirement date; clients see clear migration path.
