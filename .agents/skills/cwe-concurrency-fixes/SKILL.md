---
name: "cwe-concurrency-fixes"
description: "Consolidated guidance for synchronization-related CWEs in the CWE-888 taxonomy with .NET triggers and fixes."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Concurrency & Synchronization Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE Concurrency & Synchronization Fixes

Agent uses this bundle for races, missing locks, TOCTOU, lock misuse, and exposed lock objects.

## Activation

**USE FOR:** CWE-362, CWE-366, CWE-367, CWE-412, CWE-413, CWE-414, CWE-543, CWE-567, CWE-609, CWE-667, CWE-764, CWE-765, CWE-894, CWE-986, CWE-987, CWE-988, and CWE-989.
**DO NOT USE FOR:** General async tuning, deadlock-only diagnosis, or scheduler redesign.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent protects shared mutable state with one explicit synchronization strategy. | Run grep for touched shared fields and caches. | Every touched mutation path uses one documented primitive. |
| Agent uses `lock` only on private readonly objects. | Run grep for `lock (this)`, `lock (typeof`, and non-private lock fields. | Zero externally accessible lock targets remain. |
| Agent uses `SemaphoreSlim` for awaited critical sections. | Review touched async methods for `await` inside `lock`. | Zero touched async critical sections combine `lock` and `await`. |
| Agent replaces check-then-act races with atomic APIs or one critical section. | Run targeted stress tests with parallel callers. | Parallel runs preserve counts and state. |
| Agent replaces ad-hoc singleton and cache initialization with `Lazy<T>`, `LazyInitializer`, or `ConcurrentDictionary`. | Run parallel initialization test. | Initialization count stays at one. |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification |
|---|---|---|---|---|
| 362 | Race condition | Unsynchronized static field, singleton cache, or shared counter updates without `lock` or `Interlocked` | Guard shared mutable state with private readonly lock object or `Interlocked` for simple counters | Run `Task.WhenAll` with parallel writers. Pass: Final value and count stay deterministic. |
| 366 | Race condition within a thread | Check-then-act on shared state, such as `if (!set.Contains(x)) set.Add(x)` | Use atomic API, one critical section, or `ConcurrentDictionary.GetOrAdd` | Run repeated parallel add test. Pass: Duplicate or lost updates do not appear. |
| 367 | TOCTOU | `File.Exists` then `File.Open`, or cache miss then separate populate path | Open with atomic file mode or use one critical section and `Lazy<T>` population | Run contention test with parallel open or populate calls. Pass: State stays consistent. |
| 413 / 414 / 667 | Improper resource locking | Shared `List<T>`, `Dictionary<TKey,TValue>`, or mutable service state accessed from multiple threads without `lock` or `SemaphoreSlim` | Use private readonly lock object, `SemaphoreSlim` for async paths, or `ConcurrentDictionary` | Run parallel read-write test. Pass: No `InvalidOperationException` or count mismatch appears. |
| 543 | Unsynchronized singleton | Lazy singleton uses null check without synchronization or safe publication | Replace with `Lazy<T>`, `LazyInitializer.EnsureInitialized`, or static initialization | Run parallel singleton access test. Pass: Constructor runs once and callers get one instance. |
| 567 | Unsynchronized shared data access | Shared `Dictionary` or `List` mutated from tasks, timers, or async continuations | Use `ConcurrentDictionary`, immutable snapshot swap, or lock-guarded mutation | Run stress test with mixed readers and writers. Pass: Reads stay consistent and writes do not throw. |
| 609 | Double-checked locking | Manual double-checked locking without correct publication semantics | Replace with `Lazy<T>` or `LazyInitializer`; otherwise use one locked path | Run parallel initialization test. Pass: One instance publishes and partial state never appears. |
| 764 / 765 | Multiple locks or unlocks | Recursive acquisition on non-reentrant primitive, duplicate `Monitor.Enter`, or mismatched `Monitor.Exit` | Use `lock`, `try/finally` around `Monitor`, or one acquisition per path | Run exception-path and recursion tests. Pass: Lock count balances and no `SynchronizationLockException` appears. |
| 412 | Unrestricted externally accessible lock | `lock (this)`, `lock (typeof(Foo))`, or public lock object field | Use `private readonly object syncRoot = new();` and hide lock scope | Run grep and CA2002-style review. Pass: Touched files expose zero public lock objects. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent scans for shared fields, shared collections, singleton initialization, file check-open gaps, and public lock targets. | Run targeted grep and analyzers. | Hotspot list exists for every touched file. |
| 2. Classify | Agent maps each hotspot to one CWE row and one synchronization cluster. | Review hotspot list. | Every hotspot has one CWE label and one cluster label or out-of-scope note. |
| 3. Fix | Agent applies one synchronization strategy per hotspot: `lock`, `SemaphoreSlim`, `Interlocked`, `ConcurrentDictionary`, `Lazy<T>`, or atomic file operation. | Run targeted build for touched component. | Build passes with zero new errors. |
| 4. Run tests | Agent runs unit tests, integration tests, and stress tests already in repo for the touched scope. | Run existing tests for touched scope. | All targeted tests pass. |
| 5. Re-scan | Agent re-runs grep, analyzers, and concurrency assertions. | Re-run inventory commands. | Zero unexplained targeted hits remain in touched files. |

## Decision Matrix

| Condition | Use |
|---|---|
| Shared counter or flag update is simple and synchronous | Use `Interlocked` |
| Shared mutable state spans multiple fields or collection operations | Use `lock` on private readonly object |
| Critical section crosses `await` boundary | Use `SemaphoreSlim` |
| Shared key-based cache serves many readers and writers | Use `ConcurrentDictionary` or immutable snapshot swap |
| One-time initialization or singleton publication is needed | Use `Lazy<T>` or `LazyInitializer` |
| Lock target is externally reachable | Replace with private lock object |

## Repo Notes

| Area | Agent Uses | Agent Avoids |
|---|---|---|
| Async services and hosted workers | `SemaphoreSlim`, channels, and cancellation-aware critical sections | `await` inside `lock` |
| Shared caches and lookup tables | `ConcurrentDictionary`, `Lazy<T>`, immutable snapshot swap | Shared `Dictionary<TKey,TValue>` mutation |
| Lock objects | `private readonly object` fields with narrow scope | `lock (this)`, `lock (typeof(...))`, public sync roots |

## Verification Checklist

Agent verifies:
- [ ] Touched shared mutable state uses one documented synchronization strategy
- [ ] Touched async critical sections use async-safe coordination
- [ ] Touched singleton and cache initialization paths publish exactly one instance
- [ ] Touched lock objects are private and hidden
- [ ] Stress or analyzer checks report zero new synchronization defects

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| CWE subset | No | All 12 |
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
