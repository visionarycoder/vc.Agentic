---
name: "dotnet-code-quality-standards"
description: "Apply repository-specific .NET quality rules with correct split between modern application code and Roslyn tooling constraints."
metadata:
  metadata-version: "1.0.0"
  title: ".NET Code Quality Standards"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# .NET Code Quality Standards

Agent enforces repository's quality bar. Key split: modern net10 application code vs netstandard2.0 Roslyn tooling under `src/ifx`.

## When to Use

Use when:
- Reviewing or implementing .NET changes that pass repository quality expectations
- Applying quality rules in mixed-target solutions
- Preparing work for CI, code review, or analyzer enforcement
- Interpreting repo standards when generic .NET advice is insufficient

## When Not to Use

Do not use when:
- Single tiny local change with zero quality-policy impact
- Experimental throwaway code not intended for governed review
- Task belongs wholly to narrower specialist skill

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Target scope | Yes | File, project, module, or solution slice evaluated |
| Target framework | Yes | net10 app code or netstandard2.0 Roslyn tooling |
| Quality focus | Yes | Naming, async, maintainability, docs, analyzers, or full sweep |
| Validation command | No | Build, test, analyzer, or lint command that proves compliance |

## Workflow

Agent follows these steps:

1. Agent classifies target framework (net10 app or netstandard2.0 Roslyn)
2. Agent applies rule matrix with framework-specific constraints
3. Agent fixes issues improving readability, maintainability, analyzability
4. Agent verifies with build/test/analyzer
Test: Run `dotnet build [project].csproj`
Pass: Zero build errors. Zero new warnings.

## Rule Matrix

| Rule | Enforcement | Detection Pattern | Fix |
|---|---|---|---|
| QUAL-001 | Apply C# 14 everywhere; respect runtime ceiling | Verbose boilerplate, or `netstandard2.0`-absent BCL API or runtime-dependent feature in `src/ifx` | Use primary constructors, collection expressions, and file-scoped namespaces in all projects. Keep `src/ifx` within the `netstandard2.0` BCL. |
| QUAL-002 | Keep public APIs documented, intentional | Missing XML docs or noisy public surface | Document public members. Reduce accidental exposure. |
| QUAL-003 | Enforce naming, async suffixes, parameter-order conventions | Repo-specific signature or naming drift | Apply standard naming, method-shape rules |
| QUAL-004 | Keep methods, files maintainable | Long files, deep nesting, complex methods | Split responsibilities. Reduce nesting. |
| QUAL-005 | Make invariants explicit | Repeated literals, hidden defaults, implicit behavior | Use constants, options, enums, value objects |
| QUAL-006 | Use analyzable patterns | Dynamic or reflection-heavy code where explicit code is clearer | Use straightforward, analyzable constructs |
| QUAL-007 | Honor coverage, validation expectations | Critical paths changed without targeted tests or validation | Add or run smallest meaningful verification step |
| QUAL-008 | Use repository standards as source of truth | Generic advice conflicting with local rules | Follow repo contract. Escalate when rules conflict. |

## Framework Split

| Target | Constraint |
|---|---|
| net10 application code | C# 14 features; `ArgumentNullException.ThrowIfNull` and current BCL APIs |
| netstandard2.0 Roslyn tooling | C# 14 features (`<LangVersion>14.0</LangVersion>` plus `PolySharp`); no default or static abstract interface members; no BCL APIs absent from `netstandard2.0` |
| Public APIs | Require docs, clarity, stable naming |
| Quality validation | Use targeted build/test/analyzer checks |

## Validation Checklist

Agent verifies:
- [ ] Target framework identified before applying style guidance
- [ ] Naming, async, public API conventions are repo-aligned
- [ ] Complexity, file size remain maintainable
- [ ] Tests or validation cover changed behavior
- [ ] Advice does not conflict with repository-specific constraints

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Apply modern C# suggestions to Roslyn tooling blindly | Classify framework first |
| Treat quality as style-only cleanup | Include maintainability, docs, validation, analyzability |
| Quote generic best practices over repo rules | Use repository contract as baseline |
| Skip validation when change looks small | Run smallest relevant proof command |

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [dotnet-code-quality-standards-alternative-1](references/contexts/dotnet-code-quality-standards-alternative-1/guide.md)
