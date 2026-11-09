---
title: Module Registration
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Module Registration

The repository runtime owns module discovery through its existing `IModule` / `ModuleRegistry` mechanism.

Do not redesign module discovery in this skill.

## Module name

```text
<Capability><VaultType>Module
```

Examples:

```text
PortalManagerModule
TransformingEngineModule
AdvantageAccessModule
```

## Real implementation registration

Register the public contract to the real implementation by default.

Default lifetime when repository convention does not specify otherwise:

```csharp
services.TryAddScoped<ITransformingEngine, TransformingEngine>();
```

The real Service is the default runtime implementation.

## Keep the scaffold module minimal

Generate only:

- module logging structure consistent with repository modules
- contract-to-real-implementation registration
- clearly marked stubs for later resource/provider setup when needed

Do not add speculative:

- mapping
- caching
- validation libraries
- options
- EF Core provider binding
- connection strings
- messaging
- external SDK clients

## Failure behavior

The architectural goal is to avoid unnecessary runtime startup failure for unavailable remote dependencies.

Therefore:

- do not establish remote connections merely to register a component
- let runtime dependency availability be reported by the component's health check where practical
- structural DI errors remain build/startup defects and should not be disguised as dependency-health failures

Follow the repository's existing module exception/logging convention unless the task explicitly includes redesigning module infrastructure.

## Simulator and Emulator modules

Each substitute gets its own `Module` class.

The runtime/composition layer is responsible for selecting which implementation module is present/active. Do not make consumer business code choose implementations.

Do not rely on registration order as the selection mechanism.

If all implementations must be remotely exposed at once, treat that as separate hosting/runtime composition for the same public contract.
