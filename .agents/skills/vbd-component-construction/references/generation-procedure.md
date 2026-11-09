---
title: Generation Procedure
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Generation Procedure

Use this procedure after the developer approves the proposed project graph.

## 1. Resolve names

Resolve:

- vault type
- normalized capability name
- public interface name
- implementation name
- module name
- symbolic resource names
- selected optional projects

## 2. Create project folders and projects

Use `dotnet new` templates consistent with `project-topology.md` and repository conventions.

Delete default placeholder source files such as `Class1.cs` or meaningless generated test files.

## 3. Add project references

Required internal references:

```text
Service -> Contract
UnitTests -> Service
UnitTests -> Contract
IntegrationTests -> Service
IntegrationTests -> Contract
```

For Access ORM:

```text
Service -> ORM.<Resource>
ORM.<Resource>.IntegrationTests -> ORM.<Resource>
```

For Simulator/Emulator:

```text
Simulator -> Contract
Emulator -> Contract
```

For Host:

```text
Host -> Service
```

Do not add speculative references.

## 4. Generate minimal source artifacts

Use templates from `templates/`.

Keep the public Contract empty.

## 5. Update `.slnx`

Add all generated or reused projects to the selected `.slnx` in hierarchical solution folders.

## 6. Package management

Add only required packages and follow CPM when present.

## 7. Reconcile README

Create or update the capability-level README without overwriting existing architectural intent.

## 8. Validate and build

Apply `validation.md` and report results.
