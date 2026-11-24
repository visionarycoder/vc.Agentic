---
name: "cwe-concurrency-fixes"
description: "Consolidated guidance for synchronization-related CWEs in the CWE-888 taxonomy with .NET triggers and fixes."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Concurrency & Synchronization Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "security"
---

# CWE Concurrency & Synchronization Fixes

Agent uses this bundle for races, missing locks, TOCTOU, lock misuse, and exposed lock objects.

## Activation

**USE FOR:** CWE-362, CWE-366, CWE-367, CWE-412, CWE-413, CWE-414, CWE-543, CWE-567, CWE-609, CWE-667, CWE-764, CWE-765, CWE-894, CWE-986, CWE-987, CWE-988, and CWE-989.
**DO NOT USE FOR:** General async tuning, deadlock-only diagnosis, or scheduler redesign.

## Rules

- Use one explicit synchronization strategy per shared mutable path. Use `lock` only on `private readonly object` fields.
- Use `SemaphoreSlim` for awaited critical sections; never `await` inside `lock`.
- Use `Interlocked` for simple counters and flags; `lock` when state spans multiple fields or collection operations.
- Replace check-then-act races and ad-hoc singleton or cache initialization with atomic APIs, `Lazy<T>`, `LazyInitializer`, or `ConcurrentDictionary`.

## CWE Coverage

| CWE | Trigger Pattern | Fix and Verification |
|---|---|---|
| 362 / 366 / 413 / 414 / 567 / 667 | Unsynchronized shared state; check-then-act such as `if (!set.Contains(x)) set.Add(x)` | Private lock, `Interlocked`, or `ConcurrentDictionary.GetOrAdd`; parallel `Task.WhenAll` test shows no lost updates or `InvalidOperationException`. |
| 367 | `File.Exists` then `File.Open`, or cache miss then separate populate | Open with an atomic file mode; for caches use one critical section with `Lazy<T>`. |
| 543 / 609 | Unsynchronized lazy singleton or hand-written double-checked locking | `Lazy<T>`, `LazyInitializer.EnsureInitialized`, or static initialization; parallel test shows one constructor run, one instance, no partial state. |
| 764 / 765 | Recursive acquisition on a non-reentrant primitive, duplicate `Monitor.Enter`, mismatched `Monitor.Exit` | `lock` or `try/finally` around `Monitor`; exception-path and recursion tests show balanced locks and no `SynchronizationLockException`. |
| 412 | `lock (this)`, `lock (typeof(Foo))`, public lock field | `private readonly object syncRoot = new();` with narrow scope; grep touched files for zero exposed lock targets. |

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| CWE subset | No | All listed |
| Stress or analyzer command | No | Existing repo default |

## Outputs

Agent generates:
- Hotspot list with CWE and cluster labels
- Patch set for locking, atomicity, publication, and lock-scope fixes
- Verification notes with analyzer and stress results

## References

- MITRE CWE: https://cwe.mitre.org
- .NET threading guidance for `lock`, `Monitor`, `Interlocked`, `SemaphoreSlim`, `Lazy<T>`, and `ConcurrentDictionary`
- Analyzer guidance for lock-scope review
