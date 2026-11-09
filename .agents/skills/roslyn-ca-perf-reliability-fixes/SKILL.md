---
name: "roslyn-ca-perf-reliability-fixes"
description: "Remediate Roslyn CA performance/reliability diagnostics (CA1824, CA1825, CA1873, CA2207) via in-repo code fix providers"
metadata:
  metadata-version: "1.0.0"
  title: "CA Performance & Reliability Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# CA Performance & Reliability Fixes

Agent uses this bundle for performance, reliability CA diagnostics. When new CA rules in this category are discovered, agent adds them to Rules Coverage matrix. Agent does not create separate skills for individual CA diagnostics in this category.

## Activation

**USE FOR:** CA1824, CA1825, CA1873, CA2207 warnings
**DO NOT USE FOR:** API-design rules → `roslyn-ca-design-quality-fixes`. Code-quality rules → `roslyn-ca-code-quality-fixes`. Deeper perf analysis → `analyzing-dotnet-performance`.

## Overview

Agent handles:
- Allocation avoidance, resource localization performance, reliability-sensitive enum defaults
- Extensible performance/reliability CA guidance in one living bundle
- Future perf/reliability CA diagnostics extend this file (not new skills)

## Critical Rules

1. **CA2207 (`None = 0` on enums) is behaviorally significant.** Verify `default(TEnum)` is not already relied upon to mean something else.
2. **CA1824 is assembly-wide attribute.** Add once per assembly. Do not duplicate.
3. **Do not use `#pragma warning disable` to close a diagnostic.** Agent fixes the underlying code. Agent escalates to the owner when no safe code fix exists instead of suppressing.
4. **Build + test after each rule. One commit per rule.**

## Rules Coverage

| Rule ID | Severity | Description | Detection Pattern | Fix Strategy | Code Fix Available |
|------|----------|-------------|-------------------|--------------|--------------------|
| CA1824 | Warning | Mark assemblies with `NeutralResourcesLanguage` | Assembly lacks neutral resources language metadata | Add `[assembly: NeutralResourcesLanguage("en-US")]` or equivalent assembly attribute configuration | No |
| CA1825 | Warning | Avoid zero-length array allocations | `new T[0]` or equivalent empty-array allocation | Replace with `Array.Empty<T>()` | Yes |
| CA1873 | Warning | Avoid potentially expensive logging | Expensive argument expression (method call, string interpolation, object creation) passed to a logging call, evaluated regardless of enabled log level | Automate the guard+hoist transform: add or reuse a matching `logger.IsEnabled(LogLevel.X)` check and hoist the expensive expression into a local inside that guard block. Prefer `[LoggerMessage]` source-generated methods with raw parameters. Fall back to the manual path only when the logger receiver or log level is not determinable from the call site. Never suppress — the eager-evaluation cost remains at runtime. | Yes |
| CA2207 | Warning | Enum types define zero-valued member | Enum has zero explicit zero value | Add `None = 0` OR align existing zero member semantics explicitly | Yes |
| **Future perf/reliability CA rules** | - | Add new rules in this category here | Extend this matrix instead of creating new skill | Document detection + fix path in this bundle | - |

## Workflow

### 1. Inventory

Agent runs:
```powershell
dotnet build <target> /nologo 2>&1 |
  Select-String -Pattern 'warning (CA1824|CA1825|CA1873|CA2207)' |
  Group-Object { ($_ -split 'warning ')[1].Substring(0,6) } |
  Sort-Object Count -Descending
```
Test: Command completes
Pass: List of CA rules with occurrence counts

### 2. Auto-Fix CA1825 / CA1873 / CA2207

Agent runs:
```powershell
dotnet format analyzers <project> --diagnostics CA1825,CA1873,CA2207 --severity warn
```
Test: Run command
Pass: CA1825/1873/2207 counts drop to zero

Agent reviews CA2207 changes where `0` had prior meaning.

### 3. Auto-Fix CA1873 (Fallback: Manual Remediation)

Agent runs the automated fix from step 2 or targets CA1873 independently:
```powershell
dotnet format analyzers <project> --diagnostics CA1873 --severity warn
```
The automated fix handles the common cases:
- Extension-method logging calls
- `[LoggerMessage]`-generated static logging calls
- Calls that need a new matching guard
- Calls already inside a matching guard where the expensive expression still needs hoisting

Agent uses the manual fallback only when the provider cannot determine the logger receiver or the log level from the call site and intentionally registers no fix instead of guessing.

Agent performs, per fallback call site:
1. Identify the `[LoggerMessage]`-generated method and its declared `Level`.
2. Wrap the call in `if (logger.IsEnabled(LogLevel.<Level>)) { ... }` when not already guarded.
3. When the argument is an expensive expression (sanitizer call, `string.Join`, interpolation, object allocation), compute it as a local variable inside the guard block rather than inline in the call — this keeps the guard's protective effect visible to reviewers and avoids relying on the analyzer tracing an inline expression.
4. Never wrap the call in `#pragma warning disable CA1873` instead of adding or fixing the guard — the eager-evaluation cost this rule flags still happens at runtime under a pragma.
Test: `dotnet build` on the affected project
Pass: Zero CA1873 warnings remain and zero `#pragma warning disable CA1873` exist in touched files, whether resolved by the automated fix or the manual fallback

### 4. CA1824 (One-Time Per Assembly)

Agent adds to `Directory.Build.props` (repo-wide):
```xml
<ItemGroup>
  <AssemblyAttribute Include="System.Resources.NeutralResourcesLanguageAttribute">
    <_Parameter1>en-US</_Parameter1>
  </AssemblyAttribute>
</ItemGroup>
```
OR per-project `AssemblyInfo.cs`:
```csharp
[assembly: System.Resources.NeutralResourcesLanguage("en-US")]
```

### 5. Verify

Agent verifies:
- [ ] `dotnet build` clean, zero new warnings
Test: Run `dotnet build`
Pass: Zero build errors. Zero new warnings.
- [ ] `dotnet test` green for touched projects
Test: Run `dotnet test [project]`
Pass: All tests pass.
- [ ] `default(TEnum)` semantics unchanged (spot-check callers)
- [ ] Assembly attribute present exactly once per assembly
- [ ] Zero `#pragma warning disable CA1873` (or other rule IDs in this bundle) added
- [ ] Commit per rule

## Adding New Rules

When new performance or reliability CA rule appears:

Agent performs:
1. Agent verifies rule belongs to allocation, resource/perf metadata, reliability defaults, or similar runtime-efficiency guidance
2. Agent adds rule to **Rules Coverage** with severity, detection pattern, fix strategy, code-fix availability
3. Agent updates scan regex, auto-fix command examples when appropriate
4. Agent adds rule-specific semantic-risk notes when fix alters runtime behavior
5. Agent keeps this bundle as only performance/reliability CA surface. Agent does not create new single-rule skill.

## Verification Checklist

Agent verifies:
- [ ] Targeted perf/reliability CA warnings removed or intentionally suppressed with justification
- [ ] `Array.Empty<T>()` conversions preserve behavior
- [ ] Enum zero-value semantics remain correct
- [ ] Assembly-level attributes not duplicated
- [ ] Touched projects build, tests pass

## Common Pitfalls

| Rule or Area | Pitfall | Fix |
|---|---|---|
| CA1824 | Add duplicate assembly attributes | Centralize attribute once per assembly or in shared build props |
| CA1825 / CA1873 | Fix allocation sites inconsistently | Normalize all empty-array cases in touched scope |
| CA2207 | Add `None = 0` when zero already means something else | Review callers before changing enum semantics |
| Future rules | Create another micro-skill for one analyzer ID | Extend this bundle instead |

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Project/solution path | Yes | - |
| Rule subset | No | All 4 |

## Outputs

Agent produces:
- Zero unnecessary empty-array allocations
- `NeutralResourcesLanguage` on all assemblies
- Enums with explicit `None = 0` default
- Justified suppressions where fixes are unsafe

## References

- Fix providers: `src/ifx/Ifx.CodeFixes/Providers/CA/Ca{1824,1825,1873,2207}CodeFixProvider.cs`
- Rule docs: https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca<id>

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [ca-perf-reliability-fixes-alternative-1](references/contexts/ca-perf-reliability-fixes-alternative-1/guide.md)
- [ca-perf-reliability-fixes-alternative-2](references/contexts/ca-perf-reliability-fixes-alternative-2/guide.md)
- [ca-perf-reliability-fixes-alternative-3](references/contexts/ca-perf-reliability-fixes-alternative-3/guide.md)
- [ca-perf-reliability-fixes-alternative-4](references/contexts/ca-perf-reliability-fixes-alternative-4/guide.md)
- [ca-perf-reliability-fixes-alternative-5](references/contexts/ca-perf-reliability-fixes-alternative-5/guide.md)
- [ca-perf-reliability-fixes-alternative-6](references/contexts/ca-perf-reliability-fixes-alternative-6/guide.md)
