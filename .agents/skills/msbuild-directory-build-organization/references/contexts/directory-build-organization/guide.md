---
metadata-version: "1.0.0"
title: "Organizing Build Infrastructure with Directory.Build Files"
description: "Preserve scoped source guidance for msbuild-directory-build-organization."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Organizing Build Infrastructure with Directory.Build Files

Agent places shared MSBuild settings in the correct central file so projects stay predictable and maintainable.

## When to Use

Agent uses this skill when:
- User wants shared build settings across many projects
- Project files duplicate properties, package versions, or custom targets
- Agent needs correct placement for CPM, repo-wide targets, or default CLI flags
- Evaluation-order bugs appear in shared build infrastructure

## When Not to Use

Agent does not use this skill when:
- Build system is not MSBuild based
- Repository contains only one simple project with no shared settings
- Task is a full SDK-style migration rather than organization work

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Repo or folder scope | Yes | Root plus any nested build layers |
| Shared settings inventory | Yes | Repeated properties, packages, and targets |
| Project-type differences | No | `src`, `test`, tooling, or packaging splits |

## Placement Matrix

| File | Agent places here | Agent avoids here |
|---|---|---|
| `Directory.Build.props` | Early property defaults, common item definitions, metadata, analyzers | Late-bound SDK-dependent values and custom target logic |
| `Directory.Build.targets` | Custom targets, post-SDK validation, late-bound properties | Early defaults that projects need to override |
| `Directory.Packages.props` | Central `PackageVersion` and `GlobalPackageReference` entries | Arbitrary project-specific package metadata |
| `Directory.Build.rsp` | Default CLI switches for local or CI builds | Project content or XML-based build logic |

## Diagnostic Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1. Audit repetition | Agent catalogs repeated properties, packages, and targets across projects | Agent groups identical settings | Shared candidates are explicit |
| 2. Place by evaluation timing | Agent chooses `.props` or `.targets` based on when the value is needed. Agent reads `references/targetframework-props-pitfall.md` for `$(TargetFramework)` timing defects and `references/common-patterns.md` for file-placement examples. | Agent checks whether SDK-defined values are required | Setting lands in the correct file |

| 3. Centralize packages | Agent moves shared package versions into `Directory.Packages.props`. Agent reads `references/common-patterns.md` for package and artifact centralization patterns. | Agent removes duplicated `Version=` attributes | Version authority becomes single-source |

| 4. Build layered hierarchy | Agent chains nested `Directory.Build.*` files with `GetPathOfFileAbove` when folder-specific overrides exist. Agent reads `references/multi-level-examples.md` for parent-import structure and before-versus-after repo layouts. | Agent inspects import flow | Inner files extend rather than replace parent rules |
| 5. Verify | Agent restores, builds, and optionally preprocesses one representative project | Agent checks final evaluated values | Shared settings apply exactly once and with correct precedence |

## Critical Rules

| Rule | Agent action |
|---|---|
| Evaluation order | Agent remembers `Directory.Build.props → SDK .props → project → SDK .targets → Directory.Build.targets` |
| `TargetFramework` pitfall | Agent puts single-targeting `$(TargetFramework)` property conditions in `.targets`, not `.props` |
| Multi-level import | Agent imports the parent file explicitly at the top of nested `Directory.Build.props` or `.targets` |
| Shared versions | Agent keeps shared NuGet versions in `Directory.Packages.props` |

## Validation

| Check | Test | Pass |
|---|---|---|
| Placement correctness | Agent preprocesses or inspects effective values | Each centralized setting lands at the intended precedence point |
| Package centralization | Agent checks `PackageReference` entries after the move | Shared versions exist only in `Directory.Packages.props` |
| Layering | Agent verifies nested imports | Parent and child rules both apply |
| Build safety | Agent runs restore and build | Centralization introduces no regressions |

## Reference Files

| File | Covers | Agent reads when |
|---|---|---|
| `references/common-patterns.md` | Common `Directory.Build.props`, `Directory.Build.targets`, and artifact-layout patterns for shared build settings. | Agent reads while placing shared settings and package centralization rules. |
| `references/multi-level-examples.md` | Full parent-import examples, `src` and `test` layering, and before-versus-after centralization samples. | Agent reads when the repo uses nested build layers or folder-specific overrides. |
| `references/targetframework-props-pitfall.md` | Early-evaluation failure mode for `$(TargetFramework)` conditions in `.props` files and the safe alternatives. | Agent reads when a candidate setting depends on target-framework conditions. |

## Common Pitfalls

| Pitfall | Agent correction |
|---|---|
| Agent puts SDK-dependent properties in `.props` | Agent moves them to `.targets` |
| Agent assumes MSBuild auto-imports every nested `Directory.Build.props` | Agent adds explicit parent imports |
| Agent centralizes project-unique settings | Agent leaves project-specific values in the project file |
| Agent duplicates package version authority | Agent keeps one source of truth in `Directory.Packages.props` |
