---
title: Engine Scaffold
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Engine Scaffold

## Required projects

```text
Engine.<GerundCapability>.Contract
Engine.<GerundCapability>.Service
Engine.<GerundCapability>.Service.UnitTests
Engine.<GerundCapability>.Service.IntegrationTests
```

Normalize the capability to a gerund before naming projects or types.

## Contract artifact

Create:

```text
I<GerundCapability>Engine.cs
```

The interface is intentionally empty during construction.

## Service artifacts

Create:

```text
<GerundCapability>Engine.cs
<GerundCapability>EngineModule.cs
```

The implementation:

- is `public sealed`
- inherits `ComponentBase<<GerundCapability>Engine>`
- implements `I<GerundCapability>Engine`
- implements `IHealthCheck`
- receives `ILogger<<GerundCapability>Engine>` first

## Responsibility

Engine owns business behavior volatility. Do not turn the Engine into a workflow orchestrator for unrelated capabilities.
