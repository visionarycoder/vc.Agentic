---
metadata-version: "1.0.0"
title: "MSBuild Anti-Pattern Catalog"
description: "Preserve scoped source guidance for msbuild-antipatterns."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# MSBuild Anti-Pattern Catalog

Agent audits build files for common anti-patterns and replaces them with safer MSBuild-native patterns.

## When to Use

Agent uses this skill when:
- User requests maintainability cleanup in `.csproj`, `.props`, or `.targets`
- Build logic looks shell-heavy, duplicated, or non-portable
- Agent prepares build files for modernization or diagnostics

## When Not to Use

Agent does not use this skill when:
- Build system is not MSBuild based
- Task is a full SDK-style migration
- Runtime code quality is the only concern

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| File scope | Yes | One or more build files |
| Project style | Yes | SDK-style, legacy, mixed, or migration stage |
| Cleanup goal | No | Portability, readability, incrementality, or restore hygiene |

## Diagnostic Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1. Scan categories | Agent searches for shelling out, duplication, hardcoded paths, default noise, and the extended AP-16 through AP-22 cases in `references/additional-antipatterns.md` | Agent groups findings by anti-pattern | Agent has a short prioritized findings list |
| 2. Confirm project context | Agent verifies SDK-style versus legacy behavior | Agent checks file type and existing conventions | Agent avoids invalid blanket edits |
| 3. Replace with native patterns | Agent uses built-in tasks, shared props, portable paths, and `references/private-assets.md` when tool or analyzer packages leak to consumers | Agent maps each smell to one fix | Replacement improves diagnosability |
| 4. Centralize repeated settings | Agent moves repeated settings into shared build files when appropriate | Agent compares sibling projects | Duplication drops measurably |
| 5. Verify | Agent rebuilds or re-evaluates the touched scope. Agent reads `references/incremental-build-inputs-outputs.md` when custom targets generate files or run on every build. | Agent checks for build correctness and clearer structure | Cleanup preserves behavior |

## High-Value Matrix

| ID | Smell | Agent replacement |
|---|---|---|
| AP-01 | `<Exec>` for file operations | `MakeDir`, `Copy`, `Delete`, `Move`, `WriteLinesToFile` |
| AP-02 | Unquoted `Condition` comparisons | Single-quoted operands on both sides |
| AP-03 | Hardcoded absolute paths | `MSBuildThisFileDirectory`, `MSBuildProjectDirectory`, or repo-relative paths |
| AP-04 | Repeated SDK defaults | Remove explicit defaults and keep only intentional overrides |
| AP-05 | Manual source lists in SDK projects | Use SDK globs plus targeted `Remove` or `Exclude` |
| AP-06 | Legacy NuGet `HintPath` references | `PackageReference` |
| AP-07 | Analyzer or tool packages without `PrivateAssets="all"` | Private project-scoped packages |
| AP-08 | Copied property blocks across projects | `Directory.Build.props`, `Directory.Build.targets`, or `Directory.Packages.props` |

## Reference Files

| File | Covers | Agent reads it when |
|---|---|---|
| `references/additional-antipatterns.md` | Extended anti-pattern catalog entries AP-16 through AP-22 plus the quick-review checklist. | Agent reads it when the audit needs the full catalog beyond the high-value matrix in this file. |
| `references/incremental-build-inputs-outputs.md` | `Inputs`, `Outputs`, `FileWrites`, and generated-file patterns for incremental custom targets. | Agent reads it when a target reruns every build or writes generated files into the build graph. |
| `references/private-assets.md` | `PrivateAssets="all"` guidance for analyzers, source generators, SourceLink, and build-only tooling packages. | Agent reads it when package references include analyzers or build tools that belong to the current project only. |

## Validation

| Check | Test | Pass |
|---|---|---|
| Anti-pattern quality | Agent proves each cleanup removes a real smell | Fixes map to a catalog entry |
| Native replacement | Agent replaces shell or legacy workarounds where possible | MSBuild owns more of the workflow |
| Portability | Agent removes machine-specific paths and brittle commands | Build files become environment-agnostic |
| Behavior preservation | Agent rebuilds the touched scope | Build result stays correct |

## Common Pitfalls

| Pitfall | Agent correction |
|---|---|
| Agent rewrites unusual constructs without context | Agent verifies project style first |
| Agent removes F# compile ordering | Agent preserves explicit order in `.fsproj` files |
| Agent keeps shell commands because they already work | Agent prefers native MSBuild tasks that the engine understands |
| Agent fixes one duplicate block but leaves the pattern | Agent centralizes the shared setting once |
