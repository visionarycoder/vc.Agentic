---
metadata-version: "1.0.0"
title: "CA Design Quality Fixes"
description: "Preserve scoped source guidance for roslyn-ca-design-quality-fixes."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# CA Design Quality Fixes

Agent uses this bundle for design, API-surface CA diagnostics. When new CA rules in this category are discovered, agent adds them to Rules Coverage matrix. Agent does not create separate skills for individual CA diagnostics in this category.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Ca Design Quality Fixes work | Use this skill |
| Request falls inside the roslyn suite and needs this specific surface | Use this skill |
| The routed catalog needs a single current-state owner for this concern | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is broader than this skill and suite routing is still unclear | Use `roslyn-intake-router` first |
| Request belongs to a narrower specialist than this skill | Use that narrower specialist |
| Request is outside this skill's suite or concern | Use the correct suite router or execution skill |

## Workflow

### 1. Inventory

Agent runs:
```powershell
dotnet build <target> /nologo 2>&1 |
  Select-String -Pattern 'warning (CA1051|CA1062|CA1303|CA1413)' |
  Group-Object { ($_ -split 'warning ')[1].Substring(0,6) } |
  Sort-Object Count -Descending
```
Test: Command completes
Pass: List of CA rules with occurrence counts

### 2. Auto-Fix CA1051

Agent runs:
```powershell
dotnet format analyzers <project> --diagnostics CA1051 --severity warn
```
Test: Run command
Pass: CA1051 count drops to zero OR remaining instances are legitimate (serializer contracts) → suppress with justification

### 3. Apply Rule-Specific Remediation

Agent uses Rules Coverage matrix as source of truth. Agent groups fixes by file when safe. Agent verifies per rule.

### 4. Verify

Agent verifies:
- [ ] `dotnet build` — zero new warnings
Test: Run `dotnet build`
Pass: Zero build errors. Zero new warnings.
- [ ] `dotnet test` — green for touched projects
Test: Run `dotnet test [project]`
Pass: All tests pass.
- [ ] Suppressions carry `// CAxxxx: <reason>` comments
- [ ] Public API changes reviewed with owner
- [ ] Commit per rule

## Common Pitfalls

| Rule or Area | Pitfall | Fix |
|---|---|---|
| CA1051 | Convert serializer-bound fields without checking contract requirements | Preserve required field shape. Suppress with justification when conversion is unsafe. |
| CA1062 | Add null guards after first dereference | Place `ThrowIfNull` at top of public entry point |
| CA1303 | Move infrastructure-only messages into resources unnecessarily | Suppress intentional non-localized literals with clear reason |
| CA1413 | Add guards in one path but leave other platform calls unguarded | Audit every call site in affected API path |
| Future rules | Add new micro-skill for one diagnostic | Extend this bundle instead |

## References

- Fix providers: `src/ifx/Ifx.CodeFixes/Providers/CA/Ca{1051,1062,1303,1413}CodeFixProvider.cs`
- Rule docs: https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca<id>

## Activation

**USE FOR:** CA1051, CA1062, CA1303, CA1413 warnings
**DO NOT USE FOR:** Other CA rules → `roslyn-ca-code-quality-fixes`, `roslyn-ca-perf-reliability-fixes`. CS errors with dedicated skill → `roslyn-cs8794-fix`. Security → `cwe-fixes-bundle`.

## Overview

Agent handles:
- Public API shape, argument validation, localization-facing literals, platform/interop usage
- Extensible design-category CA guidance in one bundle
- Future design-category CA diagnostics extend this file (not new standalone skills)

## Critical Rules

1. **API changes require owner review.** CA1051, CA1303 alter public contracts.
2. **Never blanket-suppress.** Every `#pragma warning disable` has inline justification comment.
3. **Build + test after each rule.** `dotnet build` clean. `dotnet test` green.
4. **One commit per rule** for reviewable diffs.

## Rules Coverage

| Rule ID | Severity | Description | Detection Pattern | Fix Strategy | Code Fix Available |
|------|----------|-------------|-------------------|--------------|--------------------|
| CA1051 | Warning | Do not declare visible instance fields | Public or protected instance fields on externally visible types | Convert field to property. When serializer-required, suppress with justification. | Yes |
| CA1062 | Warning | Validate public method arguments for null | Public method dereferences nullable input before guard | Add `ArgumentNullException.ThrowIfNull(param);` near method entry. | No |
| CA1303 | Warning | Do not pass literals as localized parameters | String literal passed where localized resource expected | Move literal to `.resx`. Replace with resource accessor. Suppress only for intentional infrastructure literals. | No |
| CA1413 | Warning | Platform/interop safety guidance for API usage | Platform-specific or interop-sensitive API usage without correct guard/annotation | Add `OperatingSystem.IsWindows()`-style guards OR `[SupportedOSPlatform(...)]` annotations. | No |
| CA1000 | Warning | Do not declare static members on generic types | Static member defined on generic type forces caller to specify type arg unnecessarily | Move static member to non-generic helper class. | No |
| CA1001 | Warning | Type with IDisposable fields implements IDisposable | Type owns disposable fields but does not implement IDisposable | Implement IDisposable pattern. Dispose owned fields. | No |
| CA1036 | Warning | Override comparison methods when implementing IComparable | Type implements IComparable but missing `==`, `!=`, `<`, `>` operators | Implement comparison operators consistently with CompareTo. | No |
| CA1041 | Warning | Provide ObsoleteAttribute message | `[Obsolete]` without message | Add descriptive message explaining why obsolete and migration path. | No |
| CA1068 | Warning | CancellationToken parameter comes last | CancellationToken parameter not in final position | Move CancellationToken to last parameter position. | No |
| CA1510 | Warning | Use ArgumentNullException.ThrowIfNull | Manual null check instead of ThrowIfNull | Replace `if (x == null) throw new ArgumentNullException(...)` with `ArgumentNullException.ThrowIfNull(x)`. | Yes |
| CA2211 | Warning | Non-constant fields are not visible | Public or protected static non-readonly field | Make field `readonly`, `const`, or convert to property. | No |
| CA2253 | Warning | Named placeholders are unique | Logging template reuses same placeholder name | Rename placeholders to unique names. Preserves structured logging correctness. | No |
| CS0660 | Warning | Type defines operator== but not Equals | Type overloads `operator==` without overriding `Equals` | Override `Equals` and `GetHashCode` consistently with `operator==`. | No |
| CS0661 | Warning | Type defines operator!= but not GetHashCode | Type overloads `operator!=` without overriding `GetHashCode` | Override `GetHashCode` and `Equals` consistently with operators. | No |
| **Future design-category CA/CS rules** | - | Add new rules in this category here | Extend this matrix instead of creating new skill | Document detection + fix path in this bundle | - |

## Adding New Rules

When new design-category CA rule is introduced:

Agent performs:
1. Agent verifies rule belongs to API surface, argument validation, localization, or platform/interop guidance
2. Agent adds new row to **Rules Coverage** with rule ID, severity, description, detection pattern, fix strategy, code-fix availability
3. Agent extends **Activation**, **Inventory** commands when new rule is included in default scans
4. Agent adds rule-specific guardrails or validation notes when fix can break API behavior
5. Agent keeps this bundle as only design-category CA entry point. Agent does not create separate skill.

## Verification Checklist

Agent verifies:
- [ ] Build output shows targeted design-category CA warnings removed or intentionally suppressed
- [ ] Tests pass for touched projects
- [ ] Public API, localization changes reviewed where required
- [ ] Inline suppressions explain why warning remains

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Project/solution path | Yes | - |
| Rule subset | No | All 4 |

## Outputs

Agent produces:
- Reduced diagnostic count for CA1051/1062/1303/1413
- Justified suppressions where auto-fix is unsafe
