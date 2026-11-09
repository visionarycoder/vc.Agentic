---
metadata-version: "1.0.0"
title: "Test Filter Syntax Reference"
description: "Preserve scoped source guidance for filter-syntax."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Test Filter Syntax Reference

This skill provides canonical filter snippets for test runners.
This skill remains non-user-invocable and reference-only.

## Filter Matrix

| Platform | Framework | Example | Notes |
|---|---|---|---|
| VSTest | MSTest | `--filter "TestCategory=Smoke"` | Agent uses legacy VSTest property names. |
| VSTest | xUnit | `--filter "FullyQualifiedName~Namespace.Class"` | Agent prefers portable fully qualified name filters. |
| VSTest | NUnit | `--filter "Name~Critical"` | Agent validates property support for the runner. |
| MTP | MSTest | Runner-specific property filters | Agent emits the MTP form only after platform detection. |
| MTP | xUnit v3 or TUnit | Runner-specific property filters | Agent matches the exact framework package and runner surface. |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Detect | Agent identifies the active test platform and framework. | Platform choice |
| 2. Select | Agent picks the matching syntax row from this reference. | Filter expression |
| 3. Apply | Agent inserts the filter into the requested test command. | Runnable command |
| 4. Validate | Agent sanity-checks the expression against the selected runner surface. | Valid filter |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Platform match | Compare emitted syntax to project detection results. | The command uses the right platform syntax. |
| Framework match | Compare emitted properties to the framework row. | The filter uses supported properties. |
| Scope | Review the final command. | The filter narrows only the requested tests. |
