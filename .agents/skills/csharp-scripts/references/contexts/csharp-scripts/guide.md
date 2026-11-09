---
metadata-version: "1.0.0"
title: "File-Based C# Apps"
description: "Preserve scoped source guidance for csharp-scripts."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# File-Based C# Apps

This skill runs focused C# experiments without creating a full project.
This skill activates only when the user explicitly wants C# or .NET.

## Directive Table

| Directive | Purpose | Agent rule |
|---|---|---|
| `#:package` | Adds a NuGet package. | Agent pins a version unless the scenario explicitly allows floating versions. |
| `#:property` | Sets an MSBuild property. | Agent uses the smallest required property set. |
| `#:project` | References a real project. | Agent keeps the path relative. |
| `#:ref` | References another file-based app as a separate assembly. | Agent uses the directive only when assembly boundaries matter. |
| `#:include` / `#:exclude` | Adds helper files to the same compilation. | Agent requires SDK `10.0.300` or later. |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Verify SDK | Agent runs `dotnet --version` and confirms .NET 10 support. | SDK decision |
| 2. Place file | Agent creates the app outside existing project folders when the app is purely experimental. | Isolated `.cs` file |
| 3. Author | Agent writes top-level statements and adds only required directives. | Runnable source |
| 4. Execute | Agent runs `dotnet <file>.cs -- <args>` when execution is required. | Program output |
| 5. Clean | Agent deletes throwaway files or runs `dotnet clean <file>.cs` when the experiment is complete. | Clean workspace |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| SDK compatibility | Review `dotnet --version`. | The SDK supports every directive the file uses. |
| Scope fit | Review user intent and file placement. | The task is experimental and is not better served by a real project edit. |
| Execution | Run the file-based app when execution was requested. | The app runs without project scaffolding. |
| Cleanup | Review generated files after the task. | No unwanted experimental files remain. |
