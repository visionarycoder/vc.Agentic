---
name: "cwe-logic-correctness-fixes"
description: "Consolidated guidance for Risky Values and Unused entities CWEs with C#/.NET trigger, fix, and verification patterns."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Logic & Correctness Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE Logic & Correctness Fixes

Agent uses this bundle for Risky Values and Unused entities defects that corrupt arithmetic, conversions, initialization, operator logic, or executable state.

## Activation

**USE FOR:** CWE-190, CWE-191, CWE-195, CWE-196, CWE-197, CWE-369, CWE-456, CWE-457, CWE-480, CWE-481, CWE-704, CWE-561, CWE-563, CWE-482.
**DO NOT USE FOR:** Access-control defects, input-shape verification, or unrelated domain-rule disputes.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent guards arithmetic on sizes, counters, offsets, and money values. | Run boundary tests and `dotnet build <project>.csproj /p:TreatWarningsAsErrors=true`. | Boundary inputs are rejected or handled safely. |
| Agent verifies divisors and narrowing casts before evaluation. | Run zero-divisor and conversion tests. | Zero-divide and out-of-range cast paths are blocked. |
| Agent initializes fields, options, structs, and nullable value flow before first read. | Run default-state tests. | No touched path reads default-invalid state. |
| Agent removes dead logic only after branch and state tests prove no behavior change. | Run targeted unit tests after cleanup. | Removed code has no remaining effect. |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification |
|---|---|---|---|---|
| 190 | Integer overflow | Unchecked `count * size`, `offset + len`, money math | Use `checked`, guards, or wider types | Boundary tests + `dotnet build <project>.csproj /p:TreatWarningsAsErrors=true`. Pass: Overflow path fails predictably. |
| 191 | Integer underflow | `remaining -= request`, `index--` below zero | Guard lower bounds or reject | Min-value tests. Pass: No negative wrap occurs. |
| 195/196 | Signed or unsigned conversion | `int`/`uint`/`nint` cast, enum or interop size flip | Validate range and keep one signedness | Conversion tests. Pass: Out-of-range cast is rejected. |
| 197 | Numeric truncation | `(int)long`, decimal-to-int, ticks-to-ms cast | Preserve wide type or validate before cast | Max and max+1 tests. Pass: Precision loss is explicit or blocked. |
| 369 | Divide by zero | `/` or `%` on request totals or computed averages | Guard zero or short-circuit | Zero-divisor tests. Pass: Zero path returns expected result. |
| 456/457 | Missing initialization | `Unsafe.SkipInit`, `default` struct read, nullable value type default, unbound option member | Initialize in constructor or factory and validate defaults | Default-state tests. Pass: Invalid default state is rejected. |
| 480/481 | Incorrect operator or assignment | `&` or `|` instead of `&&` or `||`, `if ((isValid = Check()))` | Use explicit locals, correct operator, and clear comparison | Branch tests + build. Pass: Truth table matches intent. |
| 704 | Incorrect cast | Cast from `object`, boxed numeric, payload, or enum without check | Use pattern matching, `as` guard, or validated mapper | Invalid-type tests. Pass: Bad cast input is rejected. |
| 561 | Dead code | Code after `return` or `throw`, impossible branch | Delete unreachable blocks after proof | Build + targeted tests. Pass: Build is clean and behavior is unchanged. |
| 563 | Unused assignment | Dead store, overwritten local, `_ =` ignored result, `CS0219` or `IDE0059` | Remove unused assignment or use the value | `dotnet build <project>.csproj /p:TreatWarningsAsErrors=true`. Pass: Touched warnings are gone. |
| 482 | Comparing instead of assigning | Ported logic keeps `==` where state update was intended | Separate mutation from comparison and assert state change | State-mutation tests. Pass: Target state changes on the intended path. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent scans touched files for unchecked math, casts, division, default reads, suspicious boolean expressions, unreachable blocks, and unused assignments. | Run grep, IDE diagnostics, and existing analyzers. | Hotspot list exists for every touched file. |
| 2. Classify | Agent maps each hotspot to one CWE row. | Review hotspot list. | Every hotspot has one CWE label or explicit out-of-scope note. |
| 3. Fix | Agent adds guards, checked arithmetic, explicit initialization, operator cleanup, cast validation, and dead-code removal. | Run targeted build for touched project. | Build passes with zero new errors. |
| 4. Run tests | Agent runs boundary, branch, and state-mutation tests already in repo. | Run existing tests for touched scope. | All targeted tests pass. |
| 5. Re-scan | Agent runs analyzers and warning checks again. | Re-run inventory commands. | Zero unexplained targeted hits remain in touched files. |

## Decision Matrix

| Condition | Use |
|---|---|
| Arithmetic uses user-controlled counts, sizes, or offsets | Use `checked` or explicit range guards |
| Code narrows or flips signedness | Use pre-cast range validation |
| Code reads struct, option, or nullable defaults | Use constructor initialization and default-state rejection |
| Condition mixes assignment, bitwise, and boolean logic | Use explicit locals and branch tests |
| Local, branch, or method has no observable use | Remove it after state and coverage verification |

## Repo Notes

| Area | Agent Uses | Agent Avoids |
|---|---|---|
| Build verification | Existing .NET build with warnings as errors | New analyzer packages for one-off cleanup |
| Arithmetic and conversions | `checked`, range guards, explicit helpers | Silent narrowing casts in business logic |
| Cleanup work | Targeted dead-code and dead-store removal | Broad speculative deletion outside task scope |

## Verification Checklist

Agent verifies:
- [ ] Touched arithmetic and conversion paths cover boundary values
- [ ] Zero divisors are rejected or handled explicitly
- [ ] Touched default-value reads fail fast or initialize correctly
- [ ] Suspicious operator logic has branch tests
- [ ] Dead code and unused assignments are absent from touched scope

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| CWE subset | No | All 14 |
| Boundary test command | No | Existing repo default |

## Outputs

Agent generates:
- Hotspot list with CWE labels
- Patch set for arithmetic, conversion, initialization, operator, and dead-code fixes
- Verification notes with build, analyzer, and test results

## References

- MITRE CWE-888, CWE-885, CWE-886: https://cwe.mitre.org
- .NET numeric conversion and `checked` guidance
- Roslyn diagnostics: CS0219, IDE0059, CA1508
