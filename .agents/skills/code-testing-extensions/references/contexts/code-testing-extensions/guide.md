---
metadata-version: "1.0.0"
title: "Code Testing Extensions"
description: "Preserve scoped source guidance for code-testing-extensions."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Code Testing Extensions

This skill routes the code-testing pipeline to the correct language reference.
This skill remains non-user-invocable and reference-only.

## Extension Map

| Language | Base reference | Example reference | Agent action |
|---|---|---|---|
| .NET | `extensions/dotnet.md` | `extensions/dotnet-examples.md` | Agent loads both files. |
| Python | `extensions/python.md` | `extensions/python-examples.md` | Agent loads both files. |
| TypeScript or JavaScript | `extensions/typescript.md` | `extensions/typescript-examples.md` | Agent loads both files. |
| PowerShell | `extensions/powershell.md` | `extensions/powershell-examples.md` | Agent loads both files when the example file exists. |
| C++, Go, Java, Rust, Ruby, Swift, Kotlin | Matching file in `extensions/` | Matching `-examples.md` file when present | Agent loads the mapped pair. |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Detect | Agent detects the target language from file paths or project files. | Language choice |
| 2. Load | Agent reads the mapped base reference and example reference when one exists. | Guidance set |
| 3. Apply | Agent follows the loaded guidance before generating tests, plans, or fix cycles. | Language-aligned work |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Language detection | Compare the chosen language to target files. | Agent selected the matching reference set. |
| Base file load | Verify that the mapped base file exists and was read. | Exactly one base reference was loaded. |
| Example file load | Verify example file existence for the selected language. | Agent loaded the example reference whenever one existed. |
| Scope control | Review generated advice. | Advice stays inside the selected language surface. |
