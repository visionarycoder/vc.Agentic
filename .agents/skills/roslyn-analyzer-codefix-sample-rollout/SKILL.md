---
name: "roslyn-analyzer-codefix-sample-rollout"
description: "Implement analyzer and code-fix sample slices in compact category batches. Use this for before/after diagnostic samples, expected diagnostic mapping, and runnable documentation for vc.Analyzers and vc.CodeFixes."
metadata:
  metadata-version: "1.0.0"
  title: "Analyzer and Code-Fix Sample Rollout"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Analyzer and Code-Fix Sample Rollout

## Purpose

Use this skill to implement one analyzer or analyzer+code-fix category sample at a time with minimal token overhead.

## Scope

- `samples/FeatureGuides/Analyzers/*`
- `samples/FeatureGuides/CodeFixes/*`
- shared README/index updates for guide discoverability

## Required Rules

### ACSR0001: One Category Per Slice

Each run covers one category only:
- `Architecture`
- `Api`
- `Core`
- `Design`
- `Distributed`
- `Performance`
- `Resilience`
- `Security`
- or one code-fix-only category such as `Async`, `Data`, `Documentation`, `Naming`, `NullSafety`, `Observability`

### ACSR0002: Before/After Contract

Each code-fix sample should include:
1. violating source,
2. corrected source,
3. expected diagnostic IDs,
4. fix rationale.

### ACSR0003: Diagnostic Precision

Document exact diagnostic IDs from `DiagnosticIds.cs` and describe the rule intent in one sentence each.

### ACSR0004: Runnable Verification

Every slice must be verifiable via build/test commands, typically:
- `dotnet test tests/vc.Analyzers.Tests`
- `dotnet test tests/vc.CodeFixes.Tests`

### ACSR0005: Anti-Pattern Inclusion

Each sample must explicitly explain what the violating code gets wrong and why the fix is safer.

## Token-Efficient Workflow

1. Pick one category from the rollout plan.
2. Reuse the existing `samples/FeatureGuides` structure.
3. Add one README and the minimum before/after sources.
4. Prefer tables over long prose.
5. Stop after one category is documented and validated.

## Output Contract

1. Category implemented.
2. Diagnostic IDs covered.
3. Files added/updated.
4. Validation commands run.
5. Next category recommended.
