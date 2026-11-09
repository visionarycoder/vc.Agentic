---
title: Repository Discovery
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Repository Discovery

Inspect the repository before generating projects.

## Inspect

Look for:

```text
global.json
Directory.Build.props
Directory.Build.targets
Directory.Packages.props
NuGet.config
*.slnx
src/
tests/
existing Manager/Engine/Access components
existing test projects
existing module classes
existing health-check conventions
existing analyzer configuration
```

## `Directory.Build.props` is authoritative

Use it as the source of truth for repository-wide settings, including when present:

- `RootNamespace`
- `TargetFramework`
- `LangVersion`
- nullable configuration
- implicit usings
- analyzer settings
- warnings-as-errors
- common package/project metadata

Do not duplicate repository-wide properties into generated project files unless existing neighboring projects require a local override.

## Root namespace

Do not ask for a root namespace when `Directory.Build.props` defines it. Evaluate and follow the repository convention.

## Central Package Management

When `Directory.Packages.props` exists:

- follow CPM
- add a package version centrally only when a new package is actually required
- keep generated project `PackageReference` items versionless
- do not create a competing package-management scheme

## Framework selection

Use the latest stable .NET SDK supported by the repository. Prefer repository configuration over hard-coded skill assumptions.

## Physical layout

Default to the hierarchical VBD layout.

If the repository uses a materially different existing structure, show both choices and ask whether the new component should follow:

- the existing repository structure, or
- the hierarchical VBD structure

Default to hierarchical.

## Test conventions

Discover:

- test framework
- mocking framework
- assertion library
- coverage tooling

If existing tests are mixed or represent a migration, ask the developer which convention applies to the new component.
