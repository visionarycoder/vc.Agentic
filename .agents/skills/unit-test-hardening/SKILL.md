---
name: "unit-test-hardening"
description: "Add and repair unit tests with Microsoft .NET best practices, deterministic assertions, and coverage-gated validation. Use this for unit-test alignment after refactors, generator/analyzer test hardening, and enforcing 80% minimum coverage with explicit reporting."
metadata:
  metadata-version: "1.0.0"
  title: "Unit Test Hardening"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Unit Test Hardening

## Purpose

Use this skill to build and maintain high-quality unit tests that are stable, readable, and aligned with Microsoft guidance.

## Primary Sources

Apply guidance in this order:

1. Microsoft unit testing best practices:
- https://learn.microsoft.com/dotnet/core/testing/unit-testing-best-practices

2. Microsoft code coverage guidance:
- https://learn.microsoft.com/dotnet/core/testing/unit-testing-code-coverage
- https://learn.microsoft.com/dotnet/core/additional-tools/dotnet-coverage

3. Microsoft Roslyn/source generator references (when applicable):
- https://learn.microsoft.com/dotnet/api/microsoft.codeanalysis.generatordriver.rungeneratorsandupdatecompilation
- https://learn.microsoft.com/dotnet/api/microsoft.codeanalysis.csharp.csharpgeneratordriver.create
- https://learn.microsoft.com/dotnet/csharp/language-reference/compiler-messages/source-generator-errors

4. Repository guidance:
- docs/test-coverage-plan.md
- docs/roadmap.md
- docs/ref/dotnet-csharp.pdf
- docs/ref/dotnet-fundamentals.pdf

## When To Use

Use when tasks include:

- adding tests for new behavior,
- fixing brittle tests after expected output drift,
- improving branch/line coverage,
- implementing deterministic test patterns for generators/analyzers/code fixes,
- validating coverage thresholds for release readiness.

## Core Rules

### UTH0001: AAA + Single Concern

Each test must follow Arrange-Act-Assert and verify one concern.

### UTH0002: Naming Standard

Use `MethodName_Scenario_ExpectedBehavior` naming.

### UTH0003: Required Test Matrix

For each changed behavior, include:

- happy path,
- boundary cases,
- invalid input cases,
- failure/exception paths,
- deterministic output checks where applicable.

### UTH0004: Avoid Overspecified Assertions

Assert behavior and contracts, not incidental formatting unless formatting is the contract.

### UTH0005: Isolate Unit Tests

Avoid infrastructure dependencies; use mock/fake dependencies for deterministic and fast execution.

### UTH0006: Roslyn Test Expectations

For generators/analyzers/code fixes, validate:

- expected diagnostics and IDs,
- generated source shape/contracts,
- absent-attribute/unsupported-context behavior,
- deterministic outputs across repeated runs.

### UTH0007: Coverage Gate

Minimum line coverage target is 80%; ideal is 100% for touched logic.

Coverage command priority:

1. `dotnet test --collect:"XPlat Code Coverage"`
2. fallback: `dotnet-coverage collect "dotnet test" -f cobertura -o TestResults/coverage.cobertura.xml`

### UTH0008: Defect Logging

When tests expose a production defect outside current scope, log it in:

- docs/test-failure-code-issues.md

Include symptom, repro, impact, and recommended follow-up.

## Execution Workflow

1. Identify test gaps and brittle assertions.
2. Add/update tests with AAA and theory/data-driven patterns.
3. Run targeted tests, then full solution tests.
4. Collect coverage and report line-rate.
5. Document confirmed out-of-scope production defects.

## Recommended Command Set

```powershell
Set-Location main

# Fast loop
dotnet test tests/vc.Generators.Tests/vc.Generators.Tests.csproj

# Full validation
dotnet test

# Coverage (primary)
dotnet test --collect:"XPlat Code Coverage" --results-directory TestResults

# Coverage (fallback)
dotnet-coverage collect "dotnet test" -f cobertura -o TestResults/coverage.cobertura.xml
```

## Output Contract

For each run, provide:

1. Tests added/updated and rationale.
2. Test summary (total/passed/failed).
3. Coverage result (line-rate and report path).
4. Confirmed production defects, or explicit none-found statement.
