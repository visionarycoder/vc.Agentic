---
metadata-version: "1.0.0"
title: "CA Performance & Reliability Fixes"
description: "Preserve scoped source guidance for roslyn-ca-perf-reliability-fixes."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# CA Performance & Reliability Fixes

Agent uses this bundle for performance, reliability CA diagnostics. When new CA rules in this category are discovered, agent adds them to Rules Coverage matrix. Agent does not create separate skills for individual CA diagnostics in this category.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Ca Perf Reliability Fixes work | Use this skill |
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
$rules = 'CA1805|CA1824|CA1825|CA1826|CA1829|CA1834|CA1845|CA1846|CA1847|CA1848|CA1850|CA1854|CA1859|CA1860|CA1861|CA1862|CA1866|CA1869|CA1873|CA2017|CA2207|CA2254'
dotnet build <target> /nologo 2>&1 |
  Select-String -Pattern "warning ($rules)" |
  Group-Object { ($_ -split 'warning ')[1].Substring(0,6) } |
  Sort-Object Count -Descending
```
Test: Command completes
Pass: List of CA rules with occurrence counts

### 2. Auto-Fix

Agent runs auto-fixable rules first:
```powershell
dotnet format analyzers <project> --diagnostics CA1805,CA1825,CA1826,CA1829,CA1834,CA1845,CA1846,CA1847,CA1850,CA1854,CA1859,CA1860,CA1861,CA1862,CA1866,CA1869,CA1873,CA2017,CA2207 --severity warn
```
Test: Run command
Pass: Auto-fixable rule counts drop significantly

Agent reviews CA2207 changes where `0` had prior meaning.

### 3. Manual Fixes

Agent applies patterns from Rules Coverage matrix:

**CA1824** (One-Time Per Assembly):
```xml
<ItemGroup>
  <AssemblyAttribute Include="System.Resources.NeutralResourcesLanguageAttribute">
    <_Parameter1>en-US</_Parameter1>
  </AssemblyAttribute>
</ItemGroup>
```

**CA1848/CA2254** (Logging Performance):
Agent uses `references/logging-performance.md` for LoggerMessage patterns.

**CA1869** (Cache JsonSerializerOptions):
```csharp
private static readonly JsonSerializerOptions s_options = new() { PropertyNameCaseInsensitive = true };
// Reuse s_options instead of new JsonSerializerOptions() per call
```

### 4. Verify

Agent verifies:
- [ ] `dotnet build` clean, zero new warnings
Test: Run `dotnet build`
Pass: Zero build errors. Zero new warnings.
- [ ] `dotnet test` green for touched projects
Test: Run `dotnet test [project]`
Pass: All tests pass.
- [ ] `default(TEnum)` semantics unchanged (spot-check callers)
- [ ] Assembly attribute present exactly once per assembly
- [ ] Commit per rule

## Common Pitfalls

| Rule or Area | Pitfall | Fix |
|---|---|---|
| CA1824 | Add duplicate assembly attributes | Centralize attribute once per assembly or in shared build props |
| CA1825 / CA1873 | Fix allocation sites inconsistently | Normalize all empty-array cases in touched scope |
| CA1848 / CA2254 | Convert all logging to LoggerMessage without measuring impact | Start with high-frequency paths (>1000 calls/sec) |
| CA1869 | Create new JsonSerializerOptions per call | Hoist to static readonly field |
| CA2207 | Add `None = 0` when zero already means something else | Review callers before changing enum semantics |
| Future rules | Create another micro-skill for one analyzer ID | Extend this bundle instead |

## References

- Fix providers: `src/ifx/Ifx.CodeFixes/Providers/CA/` (for auto-fixable rules)
- Logging patterns: `references/logging-performance.md`
- Rule docs: https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca<id>

## Overview

Agent handles allocation avoidance, string optimization, logging performance, resource localization, and reliability-sensitive defaults. Agent extends this bundle for future perf/reliability CA diagnostics instead of creating new skills.

## Critical Rules

1. **CA2207** — Verify `default(TEnum)` is not already relied upon before adding `None = 0`
2. **CA1824** — Add assembly attribute once per assembly, avoid duplication
3. **CA1848/CA2254** — Use `references/logging-performance.md` for high-frequency paths only
4. **Never blanket-suppress** — Inline justification required
5. **Build + test after each rule**

## Rules Coverage

| Rule | Description | Fix | Auto |
|------|-------------|-----|------|
| CA1805 | Do not initialize unnecessarily | Remove redundant initializers | Yes |
| CA1824 | Mark assemblies with NeutralResourcesLanguage | Add assembly attribute | No |
| CA1825 | Avoid zero-length array allocations | Use `Array.Empty<T>()` | Yes |
| CA1826 | Use property instead of Enumerable method | `.Count()` → `.Count` | Yes |
| CA1829 | Use Length/Count property | `Enumerable.Count()` → `.Count`/`.Length` | Yes |
| CA1834 | Use StringBuilder.Append(char) | Single-char string → char | Yes |
| CA1845 | Use span-based string.Concat | Use span overloads | Yes |
| CA1846 | Prefer AsSpan over Substring | `.Substring().StartsWith()` → `.AsSpan().StartsWith()` | Yes |
| CA1847 | Use string.Contains(char) | Single-char string → char | Yes |
| CA1848 | Use LoggerMessage delegates | See `references/logging-performance.md` | No |
| CA1850 | Prefer static HashData method | Use static `HashData` | Yes |
| CA1854 | Prefer Dictionary.TryGetValue | `.ContainsKey()` + indexer → `.TryGetValue()` | Yes |
| CA1859 | Use concrete types when possible | Interface/abstract → concrete | Yes |
| CA1860 | Avoid Enumerable.Any() for count checks | `.Any()` → `.Count > 0` | Yes |
| CA1861 | Avoid constant arrays as arguments | Hoist to static readonly | Yes |
| CA1862 | Use StringComparison overload | Add StringComparison parameter | Yes |
| CA1866 | Use char overload | Single-char string methods → char | Yes |
| CA1869 | Cache JsonSerializerOptions | Hoist to static readonly | No |
| CA1873 | Avoid conditional access on boxing | Remove redundant `?.` | Yes |
| CA2017 | Parameter count mismatch | Fix placeholder count | Yes |
| CA2207 | Use integral/string enum base | Add `None = 0` | Yes |
| CA2254 | Template is static expression | See `references/logging-performance.md` | No |

## Adding New Rules

When new performance or reliability CA rule appears:

Agent performs:
1. Agent verifies rule belongs to allocation, resource/perf metadata, reliability defaults, or similar runtime-efficiency guidance
2. Agent adds rule to **Rules Coverage** with severity, detection pattern, fix strategy, code-fix availability
3. Agent updates scan regex, auto-fix command examples when appropriate
4. Agent adds rule-specific semantic-risk notes when fix can alter runtime behavior
5. Agent keeps this bundle as only performance/reliability CA surface. Agent does not create new single-rule skill.

## Verification Checklist

Agent verifies:
- [ ] Targeted perf/reliability CA warnings removed or intentionally suppressed with justification
- [ ] `Array.Empty<T>()` conversions preserve behavior
- [ ] String operation replacements (Substring→AsSpan, Contains(string)→Contains(char)) maintain correctness
- [ ] LoggerMessage conversions preserve placeholder order and types
- [ ] JsonSerializerOptions hoisted to static readonly where reused
- [ ] Enum zero-value semantics remain correct
- [ ] Assembly-level attributes not duplicated
- [ ] Touched projects build, tests pass

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Project/solution path | Yes | - |
| Rule subset | No | All 22 rules |

## Outputs

Agent produces:
- Zero unnecessary allocations (empty arrays, constant arrays, boxing)
- Zero unnecessary string operations (prefer char overloads, AsSpan)
- Optimized logging (LoggerMessage where high-frequency)
- Cached JsonSerializerOptions
- `NeutralResourcesLanguage` on all assemblies
- Enums with explicit `None = 0` default
- Justified suppressions where fixes are unsafe
