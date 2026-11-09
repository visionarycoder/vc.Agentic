---
metadata-version: "1.0.0"
title: "Construct VBD Component"
description: "Preserve scoped source guidance for vbd-component-construction."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Construct VBD Component

Scaffold one Juval Lowy-style Volatility-Based Decomposition (VBD) component with the minimum compilable artifacts required to establish its architectural boundary.

## Priority of guidance

Apply guidance in this order:

1. Juval Lowy's VBD principles and the VBD rules in this skill.
2. Repository-specific architecture, build, namespace, package, and testing conventions.
3. Microsoft .NET and C# guidance.
4. General implementation conventions.

If a lower-priority convention would leak implementation volatility across a VBD boundary, preserve the VBD boundary.

## Scope

This skill creates component structure only. It does not invent business activities, DTOs, mappings, ORM entities, EF Core provider configuration, endpoints, workflows, or domain behavior.

Create a separate activity with the activity skill after the component exists.

Do not use this skill for Roslyn analyzers, code fixes, or source generators. Roslyn projects have separate compatibility requirements such as .NET Standard 2.0 and C# 8.

## Supported vault types

- `Manager`
- `Engine`
- `Access`

## Required conversation flow

Guide the developer through these decisions. Do not require the developer to know VBD terminology that the skill can infer or normalize itself.

1. Ask what volatility or independent change axis the component isolates.
2. Ask for a concise mission statement.
3. Ask for concrete responsibilities.
4. Ask what is explicitly out of scope.
5. Determine whether an existing component already owns this volatility. Prefer reuse over creating a competing vault.
6. Ask for vault type: Manager, Engine, or Access.
7. Ask for the capability name.
8. If the vault is an Engine, normalize the capability to a gerund internally. Only ask when multiple gerund forms would materially change meaning.
9. Inspect repository conventions before proposing files.
10. Ask whether to create optional substitutes using one multi-select: Simulator, Emulator, or Neither.
11. Ask whether a Host is required. Default to no. If requested, default to Worker Service and use the `Host` suffix.
12. For Access, ask whether EF Core-backed resource contexts are required.
13. For each Access resource, ask for the symbolic resource name. A physical database name is known by the developer but is not encoded into project or context names.
14. When multiple resources are requested, confirm they collectively represent one external capability whose storage complexity remains hidden from callers.
15. Discover test conventions. If the repository is mixed or being modernized, ask which test convention to use for this component.
16. Show the proposed project graph before writing files.

## References to load

Always load:

- `references/vbd-rules.md`
- `references/repository-discovery.md`
- `references/naming.md`
- `references/project-topology.md`
- `references/component-base.md`
- `references/module-registration.md`
- `references/health-checks.md`
- `references/testing.md`
- `references/reconciliation.md`
- `references/validation.md`
- `references/generation-procedure.md`

Then load exactly one vault-specific reference:

- Manager: `references/manager.md`
- Engine: `references/engine.md`
- Access: `references/access.md`

Additionally:

- Access with EF Core resources: `references/orm.md`
- Simulator or Emulator selected: `references/substitutes.md`
- Host selected: `references/host.md`

Use the templates in `templates/` as generation patterns. Adapt namespaces and package references to the repository rather than copying placeholders literally.

## Generation invariants

- Use hierarchical physical layout by default.
- Use `.slnx` and add every created or reused project to the selected solution.
- Mirror the physical vault/capability hierarchy with solution folders.
- Add all required project references.
- Respect `Directory.Build.props` as the source of truth for root namespace and shared MSBuild settings.
- Respect Central Package Management when `Directory.Packages.props` exists.
- Default to the latest stable .NET SDK supported by the repository. As of this skill version, .NET 10 is the baseline, but repository configuration wins.
- Use the latest C# language features supported by the selected SDK and repository.
- Use primary constructors where appropriate.
- Use async/await for asynchronous behavior added by later skills.
- Never generate underscore-prefixed identifiers.
- Keep Contract projects pure and free of implementation leakage.
- Keep generated implementations `public sealed` unless a framework requires otherwise.
- Do not create speculative dependencies or placeholder business types.
- Do not overwrite valid existing developer artifacts.

## Completion

After generation:

1. Update the selected `.slnx` with all generated/reused projects.
2. Add required project references.
3. Run restore.
4. Build generated projects.
5. Build the selected solution when practical.
6. Validate only artifacts and references created or modified by this skill.
7. Report created, reused, conflicting, and unresolved artifacts.

Do not roll back generated files after a build failure. Preserve the artifacts for diagnosis and report the failure precisely.
