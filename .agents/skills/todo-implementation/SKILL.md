---
name: "todo-implementation"
description: "Implement TODO, FIXME, and placeholder methods with deterministic behavior and minimal, safe scope changes. Use this for TODO remediation and placeholder completion in production code, especially analyzers, code fixes, generators, and service-model aligned runtime components."
metadata:
  metadata-version: "1.0.0"
  title: "TODO Implementation"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# TODO Implementation

## Purpose

Use this skill to complete TODO and placeholder implementation work in production code while preserving existing architecture boundaries.

## Primary Sources

Apply guidance in this order:

1. Repository guidance:
- docs/roadmap.md
- docs/ref/dotnet-csharp.pdf
- docs/ref/dotnet-fundamentals.pdf

2. Microsoft Roslyn/source generator references (when applicable):
- https://learn.microsoft.com/dotnet/api/microsoft.codeanalysis.generatordriver.rungeneratorsandupdatecompilation
- https://learn.microsoft.com/dotnet/api/microsoft.codeanalysis.csharp.csharpgeneratordriver.create
- https://learn.microsoft.com/dotnet/csharp/language-reference/compiler-messages/source-generator-errors

## When To Use

Use when tasks include:

- TODO/FIXME/NotImplementedException completion,
- placeholder method body replacement,
- converting scaffolds to real behavior,
- implementing missing generator/analyzer pipeline steps,
- behavior-preserving refactors required to complete TODOs safely.

## Core Rules

### TDI0001: Behavior Contract First

Define expected behavior before coding: inputs, outputs, exceptions, diagnostics, and side effects.

### TDI0002: Minimal Scope

Implement the smallest coherent change set that resolves the TODO without unrelated refactors.

### TDI0003: Deterministic Outputs

For generators/analyzers/code fixes, ensure deterministic output for identical inputs.

### TDI0004: Preserve Architectural Boundaries

Respect project boundaries and shared abstractions; avoid copying logic that belongs in shared projects.

### TDI0005: Scaffold Policy Awareness

Classify placeholders as:

- must-implement now,
- intentional scaffold,
- out-of-scope debt.

Only convert intentional scaffolds when the task explicitly requires it.

### TDI0006: No Silent Behavior Drift

If implementation changes externally visible behavior, update documentation and sample surfaces accordingly.

## Execution Workflow

1. Discover and classify TODOs/placeholders.
2. Define acceptance criteria for each item.
3. Implement minimal production changes.
4. Run targeted tests for impacted projects.
5. Run full solution tests.
6. Hand off to `unit-test-hardening` for systematic test matrix expansion and coverage validation.

## Output Contract

For each run, provide:

1. TODOs completed.
2. TODOs intentionally deferred with reason.
3. Changed behavior summary.
4. Test results from targeted and full runs.
5. Any risk notes or follow-up recommendations.
