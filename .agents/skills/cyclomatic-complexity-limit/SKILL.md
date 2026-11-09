---
name: "cyclomatic-complexity-limit"
description: "Limit new and edited methods to a cyclomatic complexity (CC) of 10 or less, per Thomas J. McCabe's original complexity measure."
metadata:
  metadata-version: "1.0.0"
  title: "Cyclomatic Complexity Limit"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Cyclomatic Complexity Limit

Agent keeps method cyclomatic complexity (CC) at or below 10 when authoring new methods or editing existing ones.

## Why CC <= 10

Thomas J. McCabe introduced cyclomatic complexity in "A Complexity Measure" (IEEE Transactions on Software Engineering, SE-2(4), 1976). CC counts the number of linearly independent paths through a method's control flow graph — equivalently, `1 + (decision points)`, where decision points are `if`, `for`, `foreach`, `while`, `do`, `case`, `?:`, and `&&`/`||`.

McCabe recommended 10 as a practical upper bound: above that, a single method covers too many independent paths to reason about, test exhaustively, or safely modify. Complexity above 10 correlates with higher defect density and disproportionately larger test-case counts (each additional independent path needs at least one dedicated test to reach full branch coverage).

Agent treats 10 as the default ceiling, not an arbitrary style preference.

## When to Use

| Condition | Use |
|---|---|
| Writing a new method | Use this skill before finalizing the method |
| Adding a branch, loop, or condition to an existing method | Use this skill to check the updated CC |
| Reviewing a pull request that touches control flow | Use this skill to flag CC regressions |

## When Not to Use

| Condition | Alternative |
|---|---|
| Method is long but has low branching (e.g., a long sequential data mapping) | Use `code-smell-detection` (Long Method) instead |
| Complexity comes from class-level or architectural coupling, not one method | Use `design-smell-detection` |
| Diagnostic already reported as CA1502 by a code-quality gate | Use `roslyn-ca-code-quality-fixes` |

## Computing CC

Agent computes CC as:

```text
CC = 1 + count(if, for, foreach, while, do, case, ?:, &&, ||)
```

This matches the calculation used by this repository's `CQ104`/`CQ105` analyzer (`src/ifx/Ifx.Analyzers/Helpers/CodeQualityMetrics.cs`).

## Workflow

| Step | Agent Action | Output |
|---|---|---|
| 1. Draft | Agent writes or edits the method. | Candidate method body |
| 2. Measure | Agent counts decision points and computes CC (`1 + decision points`). | CC value |
| 3. Compare | Agent compares CC to the repository's configured thresholds (`.editorconfig`: `cq104_warning_threshold`, default 10; `cq105_error_threshold`, default 15). | Pass/warn/fail classification |
| 4. Refactor | When CC > 10, agent applies a refactoring technique below until CC <= 10. | Reduced-complexity method(s) |
| 5. Verify | Agent re-measures CC and runs existing tests. | Confirmed CC <= 10, behavior preserved |

## Refactoring Techniques (Highest Leverage First)

| Technique | When to Apply | Effect on CC |
|---|---|---|
| Extract Method | A block handles one sub-decision or sub-task | Moves decision points to a new method, each method's CC drops independently |
| Guard Clauses / Early Return | Nested `if` blocks for validation or edge cases | Removes nesting without removing decision points, but each guard becomes independently testable |
| Replace Conditional with Polymorphism | `switch`/`if-else` chain dispatches by type or enum | Replaces N branches in one method with N small overrides, each with CC 1 |
| Replace Conditional with Strategy | Behavior varies by injected policy/rule | Moves branching to composition (DI), reducing the orchestrating method's CC |
| Decision Table / Lookup | Conditions map to fixed outcomes | Replaces branches with data, often reducing CC to 1 |
| Consolidate Duplicate Conditional Fragments | Same branch logic repeated across a method | Removes duplicate decision points |

Agent prefers Extract Method and Guard Clauses first: they are low-risk and preserve existing call signatures. Agent uses polymorphism/strategy refactors only when the resulting design change is justified beyond just lowering CC.

## Enforcement in This Repository

Agent relies on the in-repo analyzer for automated enforcement (agent should not rely on manual counting alone):

- `CQ104` (`src/ifx/Ifx.Analyzers/CodeQuality/Cq104TooHighCyclomaticComplexity.cs`) — reports a **warning** when CC is greater than `cq104_warning_threshold` (default 10) and at or below `cq105_error_threshold` (default 15).
- `CQ105` (same file) — reports an **error** when CC exceeds `cq105_error_threshold` (default 15).
- Both thresholds are configurable per project via `.editorconfig` (`cq104_warning_threshold`, `cq105_error_threshold`).
- For the well-known equivalent legacy rule name, see `roslyn-ca-code-quality-fixes` (CA1502 — Avoid excessive complexity).

## Verification Checklist

Agent verifies:
- [ ] New or edited method has CC <= 10 (no `CQ104`/`CQ105` diagnostic)
- [ ] Refactoring did not change public method signatures without justification
- [ ] Existing tests pass after refactor (`dotnet test [project]`)
- [ ] Extracted methods have clear, single-purpose names
- [ ] No `#pragma warning disable CQ104` / `CQ105` added without inline justification

## References

- McCabe, T.J. (1976). "A Complexity Measure." *IEEE Transactions on Software Engineering*, SE-2(4), 308–320.
- `src/ifx/Ifx.Analyzers/CodeQuality/Cq104TooHighCyclomaticComplexity.cs`
- `src/ifx/Ifx.Analyzers/Helpers/CodeQualityMetrics.cs`
- `.editorconfig` (`cq104_warning_threshold`, `cq105_error_threshold`)
