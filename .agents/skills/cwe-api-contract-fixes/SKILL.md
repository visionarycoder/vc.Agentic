---
name: "cwe-api-contract-fixes"
description: "Consolidated guidance for obsolete, contract, argument-mismatch, low-level, and implementation-defined API misuse CWEs with measurable verification."
metadata:
  metadata-version: "1.0.0"
  title: "CWE API Contract Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE API Contract Fixes

Agent uses this bundle for obsolete, contract, argument-mismatch, low-level, and implementation-defined API misuse defects.

## Activation

**USE FOR:** CWE-227, CWE-242, CWE-477, CWE-573, CWE-628, CWE-683, CWE-685, CWE-686, CWE-688, CWE-695, CWE-758.
**DO NOT USE FOR:** Input validation, authorization redesign, or cryptography.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent replaces dangerous and obsolete APIs with supported alternatives. | Run `dotnet build` and targeted grep. | Zero unexplained dangerous or obsolete API hits remain. |
| Agent honors dispose, async, cancellation, and ownership contracts. | Run `dotnet build` and targeted tests. | Contract paths complete without leak or reuse-after-dispose. |
| Agent hardens reflection, `dynamic`, and optional-parameter binding with typed adapters. | Run invocation tests. | Call sites bind deterministically. |
| Agent prefers framework abstractions over raw threads, sockets, and timers. | Run grep and analyzers. | Touched scope uses supported abstractions or wrappers. |
| Agent removes implementation-defined ordering, culture, and numeric assumptions. | Run deterministic tests. | Touched logic stays stable across supported runtimes. |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification |
|---|---|---|---|---|
| 227 | General API abuse | API usage contradicts lifecycle, threading, or ownership intent | Align usage with docs, analyzer guidance, and typed wrappers | Run `dotnet build` and targeted tests. Pass: Misuse path is absent. |
| 242 | Dangerous native API use; mostly inapplicable outside interop | Deprecated Win32 `DllImport`, unsafe `Marshal` access, raw pointer copy | Replace with supported .NET API or validated wrapper | Run `rg -n "DllImport|Marshal\.|unsafe"` and `dotnet build`. Pass: Dangerous native calls are absent or wrapped. |
| 477 | Obsolete API use | `[Obsolete]` members or deprecated package APIs | Replace with supported API and remove obsolete suppression | Run `dotnet build`. Pass: `CS0618` is absent in touched scope. |
| 573 | Caller violates contract | Missing `Dispose` or `DisposeAsync`, disposed-object reuse, ignored ownership contract | Use `using`, `await using`, and ownership tests | Run `dotnet build` and dispose tests. Pass: `CA2000` findings and contract-test failures are absent. |
| 628 | Incorrectly specified call | Reflection or `dynamic` call misstates named or optional arguments | Use typed overload or validated argument map | Run invocation tests. Pass: Optional and named arguments bind correctly. |
| 683 | Incorrect argument order | Positional reflection or manual mapping swaps arguments | Use DTO mapping or wrapper with explicit names | Run invocation tests. Pass: Order defects are absent. |
| 685 | Incorrect argument count | `MethodInfo.Invoke` or `DynamicInvoke` passes wrong count | Use typed delegate or count guard | Run invocation tests. Pass: Wrong-count calls are rejected before invocation. |
| 686 | Incorrect argument type | Boxed or `dynamic` input reaches incompatible parameter type | Convert early, validate type, and use typed overloads | Run invocation tests and `dotnet build`. Pass: Wrong-type calls fail validation, not runtime dispatch. |
| 688 | Incorrect reference or aliasing argument; mostly interop and `ref` edges | Wrong `ref` or `out` target, alias reuse across boundary | Use explicit ownership boundary, copy when isolation is required, and wrap interop signatures | Run targeted unit or interop tests. Pass: Reference side effects match contract. |
| 695 | Low-level API bypass | Raw `Socket`, `Thread`, `Timer`, or manual synchronization | Use `HttpClient`, `TcpClient`, `Task`, `PeriodicTimer`, or `BackgroundService` | Run `rg -n "new Socket|new Thread|Task\.Factory\.StartNew|System\.Timers\.Timer"` and `dotnet build`. Pass: Low-level bypasses are absent or justified. |
| 758 | Implementation-defined behavior | Logic depends on dictionary order, culture-implicit parsing, or exact floating equality | Use explicit ordering, explicit culture, and tolerant comparison | Run targeted tests and `dotnet test`. Pass: Results stay stable across supported runtimes and cultures. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent scans for obsolete APIs, interop edges, reflection calls, dispose paths, raw threading, and ordering assumptions. | Run targeted grep and analyzers. | Hotspot list exists for every touched file. |
| 2. Classify | Agent maps each hotspot to one CWE row. | Review hotspot list. | Every hotspot has one CWE label or explicit out-of-scope note. |
| 3. Fix | Agent replaces unsafe APIs, restores contracts, wraps dynamic invocation, and removes unstable assumptions. | Run targeted build. | Build passes with zero new errors. |
| 4. Run tests | Agent runs unit tests, invocation tests, dispose tests, and deterministic behavior tests already in repo. | Run existing tests for touched scope. | All targeted tests pass. |
| 5. Re-scan | Agent runs grep and analyzers again. | Re-run inventory commands. | Zero unexplained targeted hits remain. |

## Decision Matrix

| Condition | Use |
|---|---|
| API surface is obsolete or dangerous | Use supported replacement or validated wrapper |
| Call site uses reflection or `dynamic` | Use typed adapter, validated map, or direct call |
| API contract includes dispose or async lifetime | Use `using`, `await using`, and ownership tests |
| Code reaches raw thread, socket, or timer APIs | Use framework abstraction or repo wrapper |
| Logic depends on runtime-specific behavior | Use explicit ordering, culture, and tolerant comparison |

## Repo Notes

| Area | Agent Uses | Agent Avoids |
|---|---|---|
| Native interop | Narrow wrapper plus platform guard | Scattered `DllImport` or `Marshal` calls |
| Async lifetime | `using`, `await using`, cancellation, ownership boundaries | Reuse-after-dispose and fire-and-forget cleanup |
| Dynamic invocation | Strongly typed delegate, adapter, or DTO map | Positional `object[]` calls without validation |

## Verification Checklist

Agent verifies:
- [ ] Touched scope contains zero unexplained dangerous or obsolete API usage
- [ ] Dispose and async lifetime contracts hold across success and failure paths
- [ ] Reflection and dynamic call sites validate count, order, type, and reference semantics
- [ ] Framework abstractions replace avoidable low-level API usage
- [ ] Deterministic tests confirm no implementation-defined behavior remains in touched logic

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| CWE subset | No | All 11 |
| Build and test commands | No | Existing repo defaults |

## Outputs

Agent generates:
- Hotspot list with CWE labels
- Patch set for API replacement, contract restoration, invocation hardening, and determinism fixes
- Verification notes with analyzer, build, and test results

## References

- MITRE CWE-888 API Cluster and CWE-1001 Improper API cluster guidance
- MITRE CWE entries: CWE-227, CWE-242, CWE-477, CWE-573, CWE-628, CWE-683, CWE-685, CWE-686, CWE-688, CWE-695, CWE-758
- .NET analyzer guidance for obsolete API, dispose, and platform compatibility
