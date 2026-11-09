---
title: Health Checks
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Health Checks

Every consumer-visible implementation supports Microsoft's `IHealthCheck`:

- real Service implementation
- Simulator implementation
- Emulator implementation

## Do not leak health infrastructure into Contract

The VBD interface does not inherit `IHealthCheck`.

Correct:

```text
ITransformingEngine
    <- TransformingEngine : ITransformingEngine, IHealthCheck
```

Incorrect:

```text
ITransformingEngine : IHealthCheck
```

`IHealthCheck` is runtime/implementation infrastructure, not part of the business capability contract.

## ORM does not own public health

Resource contexts and ORM projects do not implement `IHealthCheck`.

The Access Service implementation is responsible for reporting the health of the capability and its private dependencies.

## Initial scaffold behavior

An empty component has no substantive dependency checks yet and may return `Healthy`:

```csharp
public Task<HealthCheckResult> CheckHealthAsync(
    HealthCheckContext context,
    CancellationToken cancellationToken = default)
{
    return Task.FromResult(HealthCheckResult.Healthy());
}
```

Later activity/resource work may return `Degraded` or `Unhealthy` based on the component's ability to fulfill its mission.

## Substitute health

An intentionally selected Simulator or Emulator reports `Healthy` when it is functioning as configured.

Make the active implementation observable through logs/telemetry. Do not mark a functioning fake unhealthy merely because it is a fake.

## Standard tags

When the repository's health-registration infrastructure supports tags, use:

```text
vbd
manager
engine
access
simulator
emulator
```

Use the applicable subset for each registration.

## Registration mechanism

If the repository already has centralized health registration, use that convention. This scaffold must not invent a second health subsystem.

If no convention exists, leave health registration as an explicit runtime-composition concern while still implementing `IHealthCheck` on the component implementation.
