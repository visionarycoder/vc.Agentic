---
metadata-version: "1.0.0"
title: "Test Platform and Framework Detection"
description: "Preserve scoped source guidance for platform-detection."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Test Platform and Framework Detection

This skill identifies the active test platform and framework from project metadata.
This skill remains non-user-invocable and reference-only.

## Detection Matrix

| Clue | Interpretation | Agent action |
|---|---|---|
| VSTest SDK packages or classic test SDK usage | VSTest platform | Agent emits `dotnet test` commands and VSTest filter syntax. |
| Microsoft.Testing.Platform package set or explicit MTP configuration | MTP platform | Agent emits MTP-aligned commands and filter syntax. |
| `MSTest` packages | MSTest framework | Agent uses MSTest-specific filtering and examples. |
| `xunit` packages | xUnit framework | Agent uses xUnit-specific filtering and examples. |
| `NUnit` packages | NUnit framework | Agent uses NUnit-specific filtering and examples. |
| `TUnit` packages | TUnit framework | Agent uses TUnit-specific filtering and examples. |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Inspect | Agent reads the project file and central package props when needed. | Package inventory |
| 2. Detect platform | Agent classifies the runner surface as VSTest or MTP. | Platform result |
| 3. Detect framework | Agent classifies the framework package set. | Framework result |
| 4. Route | Agent passes the result to downstream testing skills. | Downstream-ready metadata |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Platform accuracy | Compare the detection result to project package references. | The platform result matches the installed runner surface. |
| Framework accuracy | Compare the detection result to test framework packages. | The framework result matches the active test framework. |
| Routing fit | Review downstream command generation. | Downstream skills receive the correct platform and framework pair. |
