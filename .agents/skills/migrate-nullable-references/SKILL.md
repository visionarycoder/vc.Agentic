---
name: "migrate-nullable-references"
description: "Enable C# nullable reference analysis and fix CS8xxx/CS9xxx warnings without changing runtime behavior."
metadata:
  metadata-version: "1.0.0"
  title: "Nullable Reference Migration"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Nullable Reference Migration

Agent enables nullable reference analysis and fixes warnings with metadata-only edits.

## When to Use

| User prompt | Use |
|---|---|
| User asks to enable nullable references | Use this skill |
| User asks to fix CS86xx warnings | Use this skill |
| User asks to annotate public APIs for nullability | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Project already has zero CS86xx warnings | Audit suppressions only |
| User asks for runtime guard fixes | Open a separate task |
| Target uses C# earlier than 8 | Stop and report the version block |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Project or solution path | Yes | Scope for the migration |
| Build command | No | Read repo defaults when omitted |
| Test command | No | Read repo defaults when omitted |
| Migration scope | No | Project-wide, warnings-first, or file-by-file |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent reads `.csproj` files for target framework, language version, and nullable settings. | Read project files. | Target supports C# 8 or later. |
| 2 | Agent selects one migration strategy from the strategy matrix. | Read the planned edits. | Strategy matches project size and warning count. |
| 3 | Agent enables nullable analysis in the project or file scope. | Run `dotnet build`. | Build emits CS86xx warnings for the chosen scope. |
| 4 | Agent fixes dereference warnings without adding runtime branches. | Run `dotnet build`. | `CS8600`, `CS8602`, `CS8603`, and `CS8604` are zero in scope. |
| 5 | Agent fixes declaration warnings and field initialization warnings. | Run `dotnet build`. | Remaining CS86xx warnings are zero or explicitly documented. |
| 6 | Agent audits `!`, `#pragma`, and `#nullable disable`. | Read changed files. | Each suppression has proof or is removed. |
| 7 | Agent runs tests for the touched scope. | Run repo test command. | Zero new test failures. |

## Warning Coverage

Agent fixes these nullable reference warnings:

| Code | Description | Fix Strategy |
|------|-------------|--------------|
| CS8600 | Converting null literal to non-nullable | Annotate target nullable or provide non-null value |
| CS8601 | Possible null reference assignment | Annotate source/target nullable or add null guard |
| CS8602 | Dereference of possibly null reference | Annotate nullable, add `!`, or guard |
| CS8603 | Possible null reference return | Annotate return nullable or ensure non-null |
| CS8604 | Possible null reference argument | Annotate parameter nullable or ensure non-null |
| CS8605 | Unboxing possibly null value | Annotate nullable value type or check before unbox |
| CS8613 | Nullability mismatch in return type | Align return annotations with implementation |
| CS8618 | Non-nullable property not initialized | Initialize, annotate nullable, or use `[MemberNotNull]` |
| CS8619 | Nullability mismatch in assignment | Align source/target annotations |
| CS8620 | Argument cannot be used for parameter | Align parameter annotations |
| CS8625 | Cannot convert null literal | Change target to nullable or use non-null value |
| CS8629 | Nullable value type is null | Add `.HasValue` check or use `.Value` safely |
| CS8765 | Nullability mismatch in parameter | Align delegate/lambda parameter annotations |
| CS9264 | Non-nullable property has initializer | Add initializer, constructor assignment, or annotate nullable |

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Agent adds runtime guards during metadata migration | Agent opens a separate task for runtime fixes. |
| Agent hides warnings with blanket suppressions | Agent writes typed fixes first. |
| Agent changes public contracts silently | Agent reports the contract change. |
| Agent ignores build order across projects | Agent migrates shared libraries before consumers. |

## Use Rules

| Topic | Rule |
|---|---|
| Runtime behavior | Agent keeps runtime behavior unchanged |
| Allowed edits | Agent adds `?`, `!`, nullable attributes, `#nullable`, and project nullable settings |
| Public contracts | Agent flags public nullability changes for user review |
| Suppressions | Agent removes suppressions when a typed fix exists |

## Strategy Matrix

| Scope | Use |
|---|---|
| Small project | Enable nullable and fix warnings in one pass |
| Large project | Use `warnings` first, then `enable` |
| Very large project | Use `#nullable enable` file by file |

## Warning Matrix

| Warning group | Agent fix |
|---|---|
| `CS8600`, `CS8602`, `CS8603`, `CS8604` | Agent fixes upstream nullability or adds justified `!` |
| `CS8618` | Agent initializes, annotates nullable, or uses nullable attributes |
| `CS8625` | Agent writes a nullable target or non-null value |
| Public contract changes | Agent reports the change before finalizing |

## Verification Checklist

- [ ] Agent verified C# 8 or later support.
- [ ] Agent kept runtime behavior unchanged.
- [ ] Agent reduced CS86xx warnings to zero in scope or documented blockers.
- [ ] Agent flagged public contract changes.
- [ ] Agent audited suppressions.
- [ ] Agent ran build and tests.

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [migrate-nullable-references-alternative-1](references/contexts/migrate-nullable-references-alternative-1/guide.md)
- [migrate-nullable-references-alternative-2](references/contexts/migrate-nullable-references-alternative-2/guide.md)
- [migrate-nullable-references-alternative-3](references/contexts/migrate-nullable-references-alternative-3/guide.md)
- [migrate-nullable-references-alternative-4](references/contexts/migrate-nullable-references-alternative-4/guide.md)
