---
name: "roslyn-ca-code-quality-fixes"
description: "Remediate Roslyn CA/CS code-quality diagnostics (maintainability, naming, dead code) via in-repo code fix providers plus manual guidance"
metadata:
  metadata-version: "1.0.0"
  title: "CA Code Quality Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# CA Code Quality Fixes

Agent uses this bundle for code-quality, maintainability CA diagnostics. When new CA rules in this category are discovered, agent adds them to Rules Coverage matrix. Agent does not create separate skills for individual CA diagnostics in this category.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Ca Code Quality Fixes work | Use this skill |
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
$rules = 'CA1704|CA1707|CA1801|CA1806|CA1812|CA1819|CA1822|CA1823'
dotnet build <target> /nologo 2>&1 |
  Select-String -Pattern "warning ($rules)" |
  Group-Object { ($_ -split 'warning ')[1].Substring(0,6) } |
  Sort-Object Count -Descending
```
Test: Command completes
Pass: List of CA rules with occurrence counts

### 2. Apply Auto-Fixes

Agent runs:
```powershell
dotnet format analyzers <project> --diagnostics CA1801,CA1806,CA1822,CA1823 --severity warn
```
Test: Run command
Pass: Auto-fixable rule counts drop to zero

### 3. Manual Remediation

Agent performs in order:
1. **CA1823** — Agent deletes unused private fields (verify reflection first)
2. **CA1822** — Agent applies `static` where analyzer cannot (e.g., overrides — skip)
3. **CA1812** — Agent verifies activation path. Agent deletes or annotates.
4. **CA1801/1806** — Agent replaces analyzer discards with real usage where sensible
5. **CA1819** — Agent refactors property to `IReadOnlyList<T>`/`ImmutableArray<T>` per audit with owner
6. **CA1704/1707** — Agent renames + adds shim (public API only)

### 4. Verify

Agent verifies:
- [ ] `dotnet build` clean, zero new warnings
Test: Run `dotnet build`
Pass: Zero build errors. Zero new warnings.
- [ ] `dotnet test` green for touched projects
Test: Run `dotnet test [project]`
Pass: All tests pass.
- [ ] Suppressions carry `// CAxxxx: <reason>` comments
- [ ] Public renames have `[Obsolete]` shims
- [ ] Commit per rule

## Common Pitfalls

| Rule or Area | Pitfall | Fix |
|---|---|---|
| CA1704 / CA1707 | Rename public APIs without migration plan | Use shims or coordinated API updates when compatibility matters |
| CA1801 | Add `_ = param;` everywhere | Remove parameter when signature can change safely |
| CA1806 | Discard results that carry behavior | Review API contract before using `_ =` |
| CA1812 / CA1823 | Delete members activated through reflection or DI | Verify runtime activation before removal |
| CA1819 | Replace arrays without considering callers | Use owner review for public API changes |
| Future rules | Spin up another micro-skill | Extend this bundle instead |

See `references/naming-quality-rules.md` for extended guidance on CA1711, CA1716, CA1720, CA1725, CA1727, CA2201, CS0108, CS0168-CS0414, CS1717, CS9113.

## References

- Fix providers: `src/ifx/Ifx.CodeFixes/Providers/CA/`, `Providers/CS/`
- Rule docs: https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/

## Activation

**USE FOR:** CA1704, CA1707, CA1801, CA1806, CA1812, CA1819, CA1822, CA1823 warnings
**DO NOT USE FOR:** API-surface/interop rules → `roslyn-ca-design-quality-fixes`. Performance rules → `roslyn-ca-perf-reliability-fixes`. CS errors with dedicated skill → `roslyn-cs8794-fix`.

## Overview

Agent handles:
- Naming hygiene, unused members, discarded results, static correctness, collection/API maintainability
- Extensible code-quality CA guidance in one bundle
- Future maintainability-focused CA rules extend this bundle (not new micro-skills)

## Critical Rules

1. **Renames of public identifiers (CA1704, CA1707) are breaking.** Add `[Obsolete]` shim for existing callers.
2. **CA1819 refactor changes public API.** Verify with owner before switching `T[]` return to `IReadOnlyList<T>`.
3. **CA1812/CA1823 removals are semantic.** Verify zero reflection/serializer/DI activation before deleting.
4. **Never blanket-suppress.** Every `#pragma warning disable` has inline justification comment.
5. **Build + test after each rule. One commit per rule.**

## Rules Coverage

| Rule ID | Description | Auto-Fix |
|---------|-------------|----------|
| CA1704 | Spell public identifiers correctly | No |
| CA1707 | Remove underscores from identifiers | No |
| CA1801 | Review unused parameters | Yes |
| CA1806 | Do not ignore method results | Yes |
| CA1812 | Avoid uninstantiated internal classes | No |
| CA1819 | Do not expose arrays from properties | No |
| CA1822 | Mark members static | Yes |
| CA1823 | Warning | Remove unused private fields | Yes |
| CA1711 | Warning | Rename types to avoid reserved suffixes | No |
| CA1716 | Warning | Rename identifiers to avoid keyword conflicts | No |
| CA1720 | Warning | Identifier contains type name | No |
| CA1725 | Warning | Parameter name does not match base | No |
| CA1727 | Warning | Use PascalCase for log placeholders | No |
| CA2201 | Warning | Do not raise reserved exception types | No |
| CS0108 | Warning | Member hides inherited (missing `new`) | Yes |
| CS0168 | Warning | Variable declared but never used | Yes |
| CS0169 | Warning | Field never used | Yes |
| CS0219 | Warning | Variable assigned but never used | Yes |
| CS0414 | Warning | Field assigned but never used | Yes |
| CS1717 | Warning | Assignment made to same variable | Yes |
| CS9113 | Warning | Primary constructor parameter not used | Yes |
| CS0618 | Warning | Type/member is obsolete | No |
| **Future code-quality CA/CS rules** | - | Add new maintainability rules here | - |

## Adding New Rules

When new code-quality CA diagnostic appears:

Agent performs:
1. Agent verifies rule belongs to naming, dead code, static correctness, result usage, or maintainability
2. Agent adds row to **Rules Coverage** with severity, detection pattern, fix strategy, code-fix availability
3. Agent updates `Inventory` regex, `dotnet format analyzers` examples when new rule is auto-fixable
4. Agent adds breaking-change notes to **Critical Rules** or **Common Pitfalls**
5. Agent keeps this bundle as sole code-quality CA entry point. Agent does not add separate diagnostic skill.

## Verification Checklist

Agent verifies:
- [ ] Targeted code-quality CA warnings removed or intentionally suppressed with justification
- [ ] Public renames keep compatibility requirements explicit
- [ ] Reflection, serializer, DI activation paths work after removals
- [ ] Touched projects build, tests pass

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Project/solution path | Yes | - |
| Rule subset | No | All 8 |

## Outputs

Agent produces:
- Reduced diagnostic count for 8 rules above
- Cleaner naming, fewer dead members, correct static usage
- Justified suppressions where auto-fix is unsafe

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [ca-code-quality-fixes-alternative-1](references/contexts/ca-code-quality-fixes-alternative-1/guide.md)
- [ca-code-quality-fixes-alternative-2](references/contexts/ca-code-quality-fixes-alternative-2/guide.md)
- [ca-code-quality-fixes-alternative-3](references/contexts/ca-code-quality-fixes-alternative-3/guide.md)
- [ca-code-quality-fixes-alternative-4](references/contexts/ca-code-quality-fixes-alternative-4/guide.md)
- [ca-code-quality-fixes-alternative-5](references/contexts/ca-code-quality-fixes-alternative-5/guide.md)
