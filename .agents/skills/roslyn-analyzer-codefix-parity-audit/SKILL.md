---
name: "roslyn-analyzer-codefix-parity-audit"
description: "Audit analyzer diagnostics against code-fix implementations, tests, and sample guides. Use this when repo claims full analyzer/code-fix parity or when planning missing fixes."
metadata:
  metadata-version: "1.0.0"
  title: "Analyzer Code-Fix Parity Audit"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Analyzer Code-Fix Parity Audit

## Purpose

Use this skill to produce a source-of-truth parity review for analyzers and code fixes.

## Scope

- `src/vc.Analyzers/**`
- `src/vc.Analyzers.Abstractions/DiagnosticIds.cs`
- `src/vc.CodeFixes/**`
- `tests/vc.Analyzers.Tests/**`
- `tests/vc.CodeFixes.Tests/**`
- `samples/FeatureGuides/Analyzers/**`
- `samples/FeatureGuides/CodeFixes/**`
- root and project README parity claims

## Required Checks

### ACPA0001: Analyzer Inventory

List analyzer categories, analyzer files, and diagnostic IDs.

### ACPA0002: Code-Fix Match

For each analyzer concern, classify parity as:
- `implemented`
- `manual-only`
- `missing`

### ACPA0003: Test Match

Verify whether matching analyzer and code-fix tests exist.

### ACPA0004: Sample Match

Verify whether FeatureGuides include a relevant analyzer/code-fix sample.

### ACPA0005: Claim Reconciliation

Check README and docs claims against actual parity state.

## Output Contract

1. Findings ordered by severity.
2. A parity table with analyzer, diagnostic ID, code-fix match, tests, and sample coverage.
3. A list of misleading claims that must be corrected.
4. A recommended implementation order for missing fixes or exception docs.
