---
metadata-version: "1.0.0"
title: "Convert to Central Package Management"
description: "Preserve scoped source guidance for msbuild-convert-to-cpm."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Convert to Central Package Management

Agent uses this skill to migrate PackageReference-based .NET projects to `Directory.Packages.props`.

## When to Use

| User prompt | Use |
|---|---|
| User wants centralized package versions across multiple projects | Agent uses this skill |
| User wants to convert a solution or repository to CPM | Agent uses this skill |
| User wants a before-and-after package baseline | Agent uses this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User has `packages.config` projects | Agent runs PackageReference migration first |
| User already uses CPM cleanly in scope | Agent updates the existing CPM file only |
| User wants one package version bump with no CPM scope | Agent uses a package-update workflow |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Conversion scope | Yes | Agent records project, solution, or directory scope. |
| Conflict decision | Yes | Agent records how version conflicts are resolved. |
| Shared props or targets | No | Agent uses this input to trace hidden versions. |
| Validation scope | No | Agent records build-only or build-plus-test verification. |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent verifies that every in-scope project uses PackageReference. | Run `rg -n "packages.config|PackageReference" <scope>`. | Scope contains PackageReference projects only. |
| 2 | Agent captures baseline build and package data. Agent reads `references/baseline-comparison.md` for the artifact set, package snapshot commands, and before-versus-after comparison rules. | Run `dotnet build <scope>` and `dotnet list <scope> package --format json`. | Baseline build passes and baseline package data exists. |
| 3 | Agent audits conflicts, conditional references, and property-driven versions. Agent reads `references/audit-complexities.md` for conflict classes and `references/msbuild-property-handling.md` for property-tracing decisions. | Read project files and imported props. | Conflict list and property sources are documented before edits. |
| 4 | Agent writes or updates `Directory.Packages.props` and removes inline versions. Agent reads `references/directory-packages-props.md` for placement, conditional versions, and `VersionOverride` rules. | Run `rg -n "PackageVersion|VersionOverride|Version=" <scope>`. | Central versions exist and inline versions remain only for intentional overrides. |
| 5 | Agent rebuilds and compares resolved package data to baseline. Agent reads `references/validation-and-errors.md` for restore and build validation plus NuGet error handling, and reads `references/baseline-comparison.md` for post-conversion diff reporting. | Run `dotnet build <scope>` and `dotnet list <scope> package --format json`. | Post-conversion build passes and package resolution matches the intended decisions. |
| 6 | Agent writes a persistent conversion report under `.sandbox/`. | Read the report file. | Report records scope, conflicts, decisions, risks, and follow-up work. |

## Decision Matrix

| Situation | Agent action |
|---|---|
| `packages.config` detected | Agent stops and routes to PackageReference migration. |
| Multiple versions for one package | Agent records the conflict and uses the approved decision. |
| Property-based package versions | Agent traces the property source before centralization. |
| Conditional package references | Agent preserves conditions or uses `VersionOverride` deliberately. |
| Existing CPM file governs the scope | Agent extends the existing file instead of adding a competing file. |

## Reference Files

| File | Covers | Agent reads when |
|---|---|---|
| `references/baseline-comparison.md` | Baseline and after-state package snapshots, binlog capture, and comparison tables for version-neutral verification. | Agent reads before baseline capture and during final comparison. |
| `references/audit-complexities.md` | Conflict types, conditional references, imported package sources, `VersionOverride` usage, and vulnerability follow-up rules. | Agent reads during the pre-edit audit. |
| `references/msbuild-property-handling.md` | Property-defined package versions, import-order constraints, and cleanup rules for obsolete version properties. | Agent reads when a package version comes from an MSBuild property. |
| `references/directory-packages-props.md` | `Directory.Packages.props` placement, creation, conditional `PackageVersion`, and `VersionOverride` usage. | Agent reads while writing or extending the central package file. |
| `references/validation-and-errors.md` | Clean restore and build validation, CPM-specific NuGet errors, and common post-conversion failure modes. | Agent reads after edits when restore or build validation begins. |

## Validation Checklist

- [ ] Agent verified PackageReference scope first.
- [ ] Agent captured baseline build and package data before edits.
- [ ] Agent documented conflicts and property-driven versions.
- [ ] Agent centralized package versions in `Directory.Packages.props`.
- [ ] Agent rebuilt and compared package resolution after the conversion.
- [ ] Agent wrote a conversion report under `.sandbox/`.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Agent converts without a baseline | Agent captures build and package data first. |
| Agent resolves conflicts silently | Agent records each conflict and decision. |
| Agent deletes comparison artifacts | Agent keeps baseline and after-state data. |
| Agent removes property-based versions without tracing them | Agent audits imports and remaining references first. |
