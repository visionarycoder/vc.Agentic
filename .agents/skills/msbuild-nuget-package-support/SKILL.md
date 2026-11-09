---
name: "msbuild-nuget-package-support"
description: "Add or review NuGet package support for existing .NET projects, including packability decisions for libraries, apps, tests, benchmarks, analyzers, and source generators."
metadata:
  metadata-version: "1.0.0"
  title: ".NET NuGet Package Support"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# .NET NuGet Package Support

Agent uses this skill to add package metadata, classify project packability, and verify local `dotnet pack` output for an existing .NET solution.

## When to Use

| Condition | Use |
|---|---|
| User asks to create NuGet packages for existing projects | Use this skill |
| User asks whether a project should be packaged | Use this skill |
| User asks to add `IsPackable`, `PackageId`, package metadata, symbols, or package output settings | Use this skill |
| User asks to package analyzers, code fixes, or source generators | Use this skill and the matching Roslyn authoring skill |

## When Not to Use

| Condition | Route |
|---|---|
| User asks to publish packages to nuget.org or replace API-key publishing | Use `nuget-trusted-publishing` after local packaging succeeds |
| User asks only to update dependency versions | Use central package management or dependency update guidance |
| User asks to create a new library from scratch | Use the project creation workflow first, then return to this skill |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Project list | Yes | Agent inventories every `.csproj` in scope before edits. |
| Package identity | Yes | Agent uses existing assembly/project names unless the user gives different package IDs. |
| Consumer model | Yes | Agent identifies whether consumers need runtime assemblies, analyzers, code fixes, source generators, content, or tools. |
| Version source | Yes | Agent uses existing repository versioning or adds one central default for local packages. |

## Packability Matrix

| Project type | Default | Rationale |
|---|---|---|
| Reusable class library | Pack | Libraries are the normal NuGet unit when another project can reference them independently. |
| Abstractions/contracts library | Pack | Contracts often need independent versioning and low-dependency distribution. |
| Roslyn analyzer | Pack | Analyzer packages distribute assemblies under `analyzers/dotnet/cs`. |
| Source generator | Pack | Generator packages distribute assemblies under `analyzers/dotnet/cs`; runtime output stays separate. |
| Code fix provider | Pack when paired with analyzers or local tooling needs it | Code fixes belong with analyzer distribution; avoid a package when no IDE/analyzer consumption path exists. |
| Web app, API app, worker app, or executable app | Do not pack by default | Deployable applications usually need publish/container/deployment artifacts, not library packages. |
| Unit, integration, or functional test project | Do not pack | Tests validate packages; they are not normally consumed as packages. |
| Benchmark project | Do not pack | Benchmarks are measurement executables; package their measured libraries instead. |
| Documentation-only project | Do not pack | Docs projects organize files; publish docs through site, artifact, or repository documentation channels. |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Inventory `.csproj`, `Directory.Build.props`, `Directory.Build.targets`, and `Directory.Packages.props`. | Read project SDKs, target frameworks, references, and existing package metadata. | Each project has a classification. |
| 2 | Mark non-package projects with `IsPackable=false` when the setting is absent. | Review app, test, benchmark, and docs project files. | Non-package projects cannot create accidental `.nupkg` files. |
| 3 | Add central package defaults for shared metadata and output path. | Read central props. | Defaults are applied once and can be overridden per project. |
| 4 | Add per-project package metadata only where identity or package type differs. | Read each packable project file. | Package IDs, titles, and descriptions match the project purpose. |
| 5 | For Roslyn packages, include analyzer assemblies under `analyzers/dotnet/cs` and avoid leaking Roslyn dependencies transitively. | Inspect Roslyn project files. | Package layout is analyzer-compatible. |
| 6 | Run local package verification. | Run `dotnet pack` for packable projects or the solution when appropriate. | Expected `.nupkg` files are created; non-package projects are skipped. |

## Verification Checklist

- [ ] Agent inventoried every project in scope.
- [ ] Agent classified test, benchmark, app, and docs projects as non-packable unless the user explicitly requested a different distribution model.
- [ ] Agent used central metadata for shared package settings.
- [ ] Agent kept package IDs stable and based on project identity.
- [ ] Agent configured Roslyn analyzer/source-generator package layout when needed.
- [ ] Agent ran local `dotnet pack` verification.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Packing a web app because `dotnet pack` allows it | Set `IsPackable=false` and use publish/deploy artifacts for the app. |
| Packing unit tests or benchmarks | Keep them non-packable; package the library under test. |
| Putting analyzer assemblies in `lib/` only | Set analyzer package layout so consumers receive analyzers correctly. |
| Adding metadata to every project one by one | Put shared metadata in central props and override only project-specific values. |
| Inventing public claims, URLs, or license terms | Use known repository facts or leave metadata unset until the owner confirms it. |
