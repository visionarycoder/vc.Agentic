---
name: "cwe-memory-safety-fixes"
description: "Guidance for CWE-888 memory-safety clusters in .NET interop, unsafe code, and managed bounds logic."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Memory Safety Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE Memory Safety Fixes

Agent uses this bundle for CWE-888 memory-safety clusters that reach .NET through `unsafe` code, P/Invoke, marshaling, bounds logic, and native ownership.

## Activation

**USE FOR:** Memory Access (CWE-890), Memory Management (CWE-891), Faulty Resource Release (CWE-1237), and Failure to Release Memory (CWE-1238) when the path includes unsafe or interop behavior, plus managed bounds analogs.
**DO NOT USE FOR:** Pure nullable-reference defects with no native boundary or GC tuning.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent scopes classic buffer and pointer CWEs to `unsafe`, P/Invoke, marshaling, `stackalloc`, or `Span<T>` bounds code. | Review touched files for `unsafe`, `Marshal`, import attributes, `stackalloc`, and slices. | Every reported defect has an unsafe, interop, or bounds trigger. |
| Agent validates lengths, offsets, and encoding widths before copy, slice, or marshal operations. | Run boundary tests and analyzers on touched paths. | Invalid inputs are rejected before access. |
| Agent encodes native ownership with `SafeHandle`, `using`, and allocator-matched free paths. | Run grep for `SafeHandle`, `Dispose`, allocation APIs, and release paths. | Ownership is explicit and each allocator has one matched release path. |
| Agent treats CWE-476 in this skill as unmanaged pointer null verification only. | Review pointer dereference paths and nullable-managed findings. | Pointer dereferences have guards and general nullable gaps stay owned by `cwe-miscellaneous-security-fixes`. |
| Agent verifies release paths against double-free, invalid-free, and leak regressions. | Run targeted tests for idempotence, cleanup, and handle lifetime. | Repeated cleanup stays safe and failure paths release owned memory. |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification |
|---|---|---|---|---|
| 119 | Bounds restriction failure | `Span<T>.Slice`, `stackalloc`, or pointer arithmetic uses untrusted length or offset | Guard ranges before access | Run boundary and fuzz tests. Pass: Out-of-range inputs fail before access. |
| 120 | Buffer copy without size check | `Marshal.Copy`, `Buffer.MemoryCopy`, or native copy API uses caller-controlled length | Verify capacity, then copy validated count | Run boundary tests. Pass: Oversized copy is rejected. |
| 125 / 129 | Out-of-bounds read or bad index validation | Array or span indexing uses file, network, or native offset without full bounds checks | Validate offset and remaining length before index or slice | Run malformed offset tests. Pass: Invalid index paths fail safely. |
| 476 | NULL pointer dereference at native boundary | `IntPtr`, `void*`, or native out pointer is dereferenced after P/Invoke with no null check | Guard returned pointers and use `SafeHandle` for long-lived handles | Run interop tests. Pass: Null pointer path returns controlled error. |
| 131 / 135 | Buffer size or multibyte length miscalculation | Fixed-size native struct or UTF buffer uses char count as byte count | Compute byte count explicitly with encoding and struct layout facts | Run encoding and struct-size tests. Pass: Buffer sizes match byte counts. |
| 415 / 763 | Double free or invalid release | Repeated `Dispose`, duplicate native free, or raw handle release after ownership transfer | Centralize ownership, make dispose idempotent, and prefer `SafeHandle` | Run idempotence tests. Pass: Repeated cleanup causes no double free. |
| 401 | Missing release after lifetime ends | Missing `using`, abandoned `SafeHandle`, failed cleanup path, or missing `GC.KeepAlive` | Use `using` or `try/finally`, release success and failure paths, and keep the managed owner alive through the native call | Run leak tests. Pass: Owned memory and handles return to baseline. |
| 762 | Mismatched memory management routines | `AllocHGlobal` freed with `FreeCoTaskMem` or wrapper hides allocator contract | Match the free routine to the allocator and document ownership | Run interop tests and header review. Pass: Each allocation path has one correct release. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent scans for `unsafe`, `Marshal`, import attributes, `stackalloc`, `Span<T>`, `SafeHandle`, and native allocators. | Run targeted grep and analyzers. | Hotspot list exists for every touched file. |
| 2. Classify | Agent maps each hotspot to a cluster and CWE row, with managed analog notes where needed. | Review hotspot list. | Every hotspot has one CWE label or out-of-scope note. |
| 3. Fix | Agent adds bounds guards, size logic, `SafeHandle` ownership, matched release, and cleanup. | Run targeted build. | Build passes. |
| 4. Run tests | Agent runs unit, interop, boundary, fuzz, and lifetime tests already in repo. | Run existing tests for touched scope. | All targeted tests pass. |
| 5. Re-scan | Agent runs grep and analyzers again, including CA2020, CA1416, and CA2101 when applicable. | Re-run inventory commands. | Zero unexplained targeted hits remain in touched files. |

## Decision Matrix

| Condition | Use |
|---|---|
| Code copies bytes across managed or native boundary | Use validated count and capacity guards |
| Code slices `Span<T>` or computes offsets from untrusted input | Use range guards before index or slice |
| Code owns native memory or handle beyond one call | Use `SafeHandle` or a single-owner wrapper |
| Code frees memory allocated by another API family | Use allocator-matched release from the same family |
| Finding is general nullable-reference drift with no native boundary | Use `cwe-miscellaneous-security-fixes` instead |

## Repo Notes

| Area | Agent Uses | Agent Avoids |
|---|---|---|
| Managed code default | Honest scoping: most classic buffer and pointer CWEs are not directly reachable in safe C# | Claiming native exploit paths in pure managed code |
| Interop paths | `dotnet-pinvoke` for signature and ownership review | Raw `IntPtr` ownership with undocumented allocator rules |
| Buffer logic | `Span<T>` and explicit length guards | Hidden byte-count assumptions and unchecked slices |

## Verification Checklist

Agent verifies:
- [ ] Touched unsafe or interop paths validate length, offset, and encoding width before access
- [ ] Native ownership paths use `SafeHandle`, `using`, or `try/finally` with matched allocators
- [ ] Dispose and cleanup paths stay idempotent under repeated calls and failures
- [ ] General nullable-reference findings stay routed to `cwe-miscellaneous-security-fixes` unless unmanaged pointers are involved
- [ ] Interop-focused analyzers and boundary tests report zero unexplained new findings

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| CWE subset | No | All 8 rows |
| Native ownership or header contract | No | Existing code and `dotnet-pinvoke` guidance |

## Outputs

Agent generates:
- Hotspot list with cluster and CWE labels
- Patch set for bounds, marshaling, ownership, and cleanup fixes
- Verification notes with analyzer, test, and interop results

## References

- MITRE CWE: https://cwe.mitre.org
- CWE-888 taxonomy
- .NET interop, `SafeHandle`, and `Span<T>` guidance
