---
metadata-version: "1.0.0"
title: "CWE Exception Management Fixes"
description: "Preserve scoped source guidance for dotnet-exception-handling."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# CWE Exception Management Fixes

Agent uses this bundle for exception and status-check defects in .NET code.

## Activation

**USE FOR:** CWE-248, CWE-252, CWE-253, CWE-392, CWE-396, CWE-397, CWE-460, CWE-478, CWE-484, CWE-584, CWE-636, CWE-703, CWE-754, CWE-755.
**DO NOT USE FOR:** Authentication-only, input-only, or resource-lifetime-only work.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent catches specific exception types and preserves stack with `throw;` on rethrow. | Run `rg -n "catch \(Exception|throw ex;" -g "**/*.cs"`. | Zero new broad catches or stack-reset rethrows remain in touched files. |
| Agent checks every status-bearing return path and routes expected failures through `bool`, `Result`, or `Result<T>` flow. | Run analyzers and `rg -n "_ = |TryParse\(|TryGetValue\(" -g "**/*.cs"`. | Zero unexplained ignored status results remain. |
| Agent restores cleanup with `using`, `await using`, or `finally` on exceptional exits. | Run targeted throw-path tests. | Resources release on success and failure paths. |
| Agent fails closed on security-relevant exception paths. | Run negative authorization, configuration, or dependency-failure tests. | Faulted security checks reject access or stop the operation. |
| Agent defines one global exception boundary for ASP.NET Core hosts and one default switch branch. | Run integration tests and grep for `UseExceptionHandler`, `IExceptionHandler`, `default:`, and `_ =>`. | Unhandled faults reach the global boundary. |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification |
|---|---|---|---|---|
| 396 / 397 | Ambiguous exception type | `catch (Exception ex)`, `throw new Exception(...)`, or broad exception contracts | Catch specific exception types and rethrow with `throw;` when propagation is required | Run CA1031 and CA2200 checks. Pass: Broad catches and stack-reset rethrows are absent. |
| 392 / 460 | Missing report or cleanup on error | Empty catch, log-only catch, success-only cleanup, or missing `finally` after acquisition | Report, translate, or rethrow the failure and move cleanup to `using`, `await using`, or `finally` | Run fault-path tests. Pass: Failure is observable and cleanup runs on thrown paths. |
| 584 | Return inside finally | `return`, `break`, or state overwrite inside `finally` | Remove control-flow statements from `finally` and keep cleanup side-effect free | Run targeted unit test. Pass: Original exception or result reaches the caller unchanged. |
| 636 | Failing open | Catch-and-continue around authorization, signature, configuration, or policy checks | Reject the request, stop the workflow, or disable the operation safely | Run negative-path security tests. Pass: Faulted checks deny access or stop processing. |
| 703 / 754 / 755 | Improper exceptional-condition handling | Catch-all fallback, inconsistent status mapping, or exception control for expected outcomes | Use typed result flow for expected outcomes and central exception mapping for faults | Run targeted tests. Pass: Expected outcomes use status flow and faults map consistently. |
| 252 / 253 | Unchecked or incorrect status condition | Ignored `Task`, ignored `bool` from `TryParse` or `TryGetValue`, discarded `Result<T>`, or inverted status check | Await returned tasks, branch on `bool` and result states, and return early on failure | Run CA1806 and unit tests. Pass: Every status-bearing call is checked deliberately. |
| 248 | Uncaught exception | Host lacks global exception middleware or top-level fault boundary | Add global exception handling and map faults to safe edge contracts | Run endpoint or handler failure test. Pass: Caller receives the stable edge contract. |
| 478 / 484 | Missing default case or omitted branch | `switch` statement or switch expression lacks `default:` or `_ =>` for unexpected values | Add explicit default branch that rejects, throws, or returns failed result | Run analyzer or unknown-value tests. Pass: Unexpected input follows an explicit branch. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent scans for broad catches, stack-reset rethrows, ignored status returns, missing cleanup, missing global handlers, and missing default branches. | Run targeted grep and analyzers. | Hotspot list exists for every touched file. |
| 2. Classify | Agent maps each hotspot to exception type, exception behavior, or status condition coverage. | Review hotspot list. | Every hotspot has one CWE label or explicit out-of-scope note. |
| 3. Fix | Agent adds typed exceptions, cleanup guards, fail-closed behavior, explicit status checks, global handlers, and default branches. | Run targeted build for touched component. | Build passes with zero new errors. |
| 4. Run tests | Agent runs unit and integration tests that exercise propagation, cleanup, safe failure, and status checks. | Run existing test project for touched scope. | All targeted tests pass. |
| 5. Re-scan | Agent runs grep and analyzers again. | Re-run inventory commands. | Zero unexplained targeted hits remain in touched files. |

## Decision Matrix

| Condition | Use |
|---|---|
| Outcome is expected and caller-correctable | Use `bool`, `Result`, or `Result<T>` flow |
| Outcome is exceptional and aborts the operation | Use a specific exception type |
| Catch block adds logging or translation only | Use specific catch and preserve stack with `throw;` |
| Security check faults | Use fail-closed handling |
| Switch handles external or future values | Use `default:` or `_ =>` explicit branch |

## .NET Exception Patterns

| Area | Agent Uses | Agent Avoids |
|---|---|---|
| Catch behavior | Specific exception types and `throw;` | `catch (Exception)` and `throw ex;` |
| Expected outcomes | `Try*` checks and `Result<T>` flow | Exception-driven branching for routine outcomes |
| Cleanup | `using`, `await using`, and `finally` cleanup | Cleanup on success path only |
| Host boundary | `UseExceptionHandler`, `AddProblemDetails`, and `IExceptionHandler` | Controller-local catch-all duplication |
| Switch handling | `default:` and `_ =>` reject or fail branches | Non-exhaustive switch logic |

## Verification Checklist

Agent verifies:
- [ ] Touched files avoid new broad catches and stack-reset rethrows
- [ ] Touched status-bearing calls check `Task`, `bool`, and `Result<T>` outcomes
- [ ] Exceptional paths release resources and do not return from `finally`
- [ ] Security-relevant fault paths fail closed
- [ ] Global handlers and switch defaults cover unexpected faults and values

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or project path | Yes | - |
| CWE subset | No | All 8 rows |
| Host, library, or worker scope | No | All matching files |

## Outputs

Agent generates:
- Hotspot list with CWE and cluster labels
- Patch set for exception typing, cleanup, fail-closed handling, status checks, and edge boundaries
- Verification notes with analyzer, build, and test results

## References

- MITRE CWE: https://cwe.mitre.org
- ASP.NET Core error handling: https://learn.microsoft.com/aspnet/core/fundamentals/error-handling
- Roslyn rules: CA1031, CA1806, CA2200
