---
name: "roslyn-analyzer-rule-composition"
description: "Use when creating, refactoring, or reviewing vc.Analyzers rule composition so analyzers remain composition roots, rules stay in local Rules folders, and DiagnosticIds ownership stays consistent."
metadata:
  metadata-version: "1.0.0"
  title: "Analyzer Rule Composition"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Analyzer Rule Composition

Use this skill when implementing or refactoring analyzers in `src/vc.Analyzers`.

## Canonical Pattern

- Analyzer class is the composition root.
- Each diagnostic rule lives in its own rule class/file.
- Rule classes live in a local `Rules` subfolder next to the analyzer.
- Rule namespace matches analyzer namespace plus `.Rules`.

## Composition Requirements

### ARC0001: One Rule Class per Diagnostic Rule

- No inline descriptor-and-analysis blocks in analyzer classes.
- No analyzer class owning multiple rule implementations directly.

### ARC0002: Analyzer as Composition Root

Analyzer classes should:

- Compose `IAnalyzerRule` instances.
- Register each rule in `Initialize`.
- Expose `SupportedDiagnostics` as the union of composed descriptors.

### ARC0003: Rule Folder Locality

Rules stay local to the analyzer folder, including nested paths.

```text
src/vc.Analyzers/Api/
  ApiDesignAnalyzer.cs
  Rules/
    MissingApiControllerRule.cs
    NonRestfulNameRule.cs

src/vc.Analyzers/Design/Vbd/
  VbdAccessAnalyzer.cs
  VbdEngineAnalyzer.cs
  VbdManagerAnalyzer.cs
  Rules/
    VbdAccessBoundaryViolationRule.cs
    VbdEngineNondeterminismRule.cs
    VbdManagerOrchestrationRule.cs
```

### ARC0004: Rule Contract

Preferred contract:

```csharp
public interface IAnalyzerRule
{
    DiagnosticDescriptor Descriptor { get; }
    void Register(AnalysisContext context);
}
```

### ARC0005: Unified Diagnostic IDs

- Descriptor IDs must come from `DiagnosticIds` constants.
- No magic string IDs.

### ARC0006: Name Alignment

- Rule class names match semantic rule names used by the analyzer/descriptors.
- Prefer semantic names such as `MissingApiControllerRule` over analyzer-prefixed noise.
- File names match class names.

## Ownership Guardrails

When a rule is duplicated across analyzers, keep only one canonical owner.

- Generic async correctness belongs in `Core/AsyncCorrectnessAnalyzer`.
- Exception safety belongs in `Design/ExceptionSafetyAnalyzer`.
- Hardcoded secret detection belongs in `Security/HardcodedSecretAnalyzer` and owns `DiagnosticIds.SecurityHardcodedSecret`.

If duplicate diagnostic IDs appear across analyzers, keep the broadest canonical owner and remove redundant registrations.

## Refactor Workflow

1. Add or reuse local `Rules` folder.
2. Extract each descriptor and callback into one rule class.
3. Convert analyzer to pure composition and registration.
4. Verify descriptor IDs come from `DiagnosticIds`.
5. Validate build.

Validation command:

```powershell
dotnet build src/vc.Analyzers/vc.Analyzers.csproj --no-incremental
```

## Related

- `.agents/skills/roslyn-unified-diagnostic-id/SKILL.md`
- `docs/instructions/unified-diagnostic-ids.md`
- `docs/instructions/analyzer-rule-composition.md`
