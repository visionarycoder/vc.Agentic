---
name: "roslyn-feature-guide-coverage-audit"
description: "Audit FeatureGuides coverage against source analyzer, code-fix, and generator surfaces. Use this when verifying whether documentation and samples are truly complete."
metadata:
  metadata-version: "1.0.0"
  title: "Feature Guide Coverage Audit"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Feature Guide Coverage Audit

## Purpose

Use this skill to compare the current source surface with FeatureGuides documentation density and discoverability.

## Scope

- `samples/FeatureGuides/**`
- `src/vc.Analyzers/**`
- `src/vc.CodeFixes/**`
- `src/vc.Generators/**`
- `README.md`
- project-level `README.md` files under `src/`

## Required Checks

### FGCA0001: Category and Family Inventory

List all analyzer categories, code-fix categories, and generator families from `src/`.

### FGCA0002: Guide Presence

Verify that each source category or family has a matching FeatureGuides folder and README.

### FGCA0003: Guide Density

Classify each guide as:
- `complete`
- `partial`
- `minimal`
- `missing`

Use actual source breadth to justify the classification.

### FGCA0004: Sample Completeness

Verify whether each guide has:
- documented feature/value/use/avoid/expected output,
- sample input or before/after assets,
- stable contract-oriented examples.

### FGCA0005: Discoverability

Check that top-level and project READMEs link to the relevant guide indexes and do not understate or overstate coverage.

## Output Contract

1. A coverage table for analyzers, code fixes, and generators.
2. A list of missing or thin guides.
3. A list of README discoverability gaps.
4. A prioritized expansion order for documentation work.
