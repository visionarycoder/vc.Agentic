---
name: "roslyn-analyzer-authoring"
description: "Author Roslyn analyzers with precise diagnostics, narrow registration, C# 14 implementation within the netstandard2.0 runtime ceiling, and MSTest verification for src/ifx projects."
metadata:
  metadata-version: "1.0.0"
  title: "Roslyn Analyzer Authoring"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# Roslyn Analyzer Authoring

Agent authors analyzers for `src/ifx` packages. Agent keeps analyzer logic deterministic, narrow, and written in C# 14 for `netstandard2.0` Roslyn projects (`<LangVersion>14.0</LangVersion>` plus `PolySharp`).

Use for new diagnostic rules, compile-time architecture or API enforcement, and analyzer tests or packaging updates.

## When Not to Use

| User prompt | Route |
|---|---|
| User asks for automatic source edits | Use `roslyn-codefix-authoring` |
| User asks for generated code instead of diagnostics | Use `roslyn-source-generator-authoring` |
| User asks for a one-time grep or script audit | Use direct tools |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Rule intent | Yes | State the exact invalid pattern. |
| Diagnostic metadata | Yes | Provide ID, title, message, category, severity. |
| Analysis surface | Yes | Pick syntax, symbol, operation, or compilation scope. |
| False-positive limits | Recommended | List exclusions, generated code rules, and valid exceptions. |
| Packaging target | No | State analyzer package or project target. |

## Guardrail Matrix

| Concern | Agent action |
|---|---|
| Target framework | Agent confirms `netstandard2.0` before using Roslyn project patterns. |
| Language level | Agent confirms `<LangVersion>14.0</LangVersion>` and the `PolySharp` reference, then uses C# 14 syntax (primary constructors, collection expressions, file-scoped namespaces, records) inside `src/ifx`. Agent avoids runtime-dependent features (default interface members, static abstract interface members) and BCL APIs absent from `netstandard2.0`. |
| Initialize | Agent calls `ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None)` unless the rule needs generated files, and `EnableConcurrentExecution()`. |
| Locations | Agent uses `Diagnostic.Create(rule, syntax.GetLocation(), args)` or a member location. |
| Tests | Agent adds positive, negative, boundary, and location MSTest cases. |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent defines one rule contract. | Read descriptor draft. | ID, title, message, category, and severity are explicit. |
| 2 | Agent selects the narrowest registration surface. | Inspect `Initialize`. | Registration uses syntax, symbol, or operation callbacks only where needed. |
| 3 | Agent filters cheaply before semantic work. | Inspect analysis method. | Syntax or symbol shape removes obvious non-candidates. |
| 4 | Agent resolves semantic facts late. | Inspect semantic calls. | Symbol or compilation lookups appear only after cheap filters. |
| 5 | Agent reports one stable diagnostic. | Run analyzer tests. | Squiggle location and message match the rule contract. |
| 6 | Agent validates hot-path cost. | Review allocations and cached lookups. | No repeated expensive lookups appear in per-node paths. |
| 7 | Agent adds MSTest coverage. | Run analyzer test project. | Positive and negative tests pass. |
| 8 | Agent verifies package loading. | Inspect `.csproj` and package assets. | Analyzer output lands under `analyzers/dotnet/cs` when packing applies. |

## References

Agent reads `references/analyzer-patterns.md` for descriptor templates, registration examples, performance notes, and test snippets.

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [roslyn-analyzer-authoring-alternative-1](references/contexts/roslyn-analyzer-authoring-alternative-1/guide.md)
- [roslyn-analyzer-authoring-alternative-2](references/contexts/roslyn-analyzer-authoring-alternative-2/guide.md)
- [roslyn-analyzer-authoring-alternative-3](references/contexts/roslyn-analyzer-authoring-alternative-3/guide.md)
