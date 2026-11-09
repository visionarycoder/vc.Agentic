---
title: Manager Scaffold
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Manager Scaffold

## Required projects

```text
Manager.<Capability>.Contract
Manager.<Capability>.Service
Manager.<Capability>.Service.UnitTests
Manager.<Capability>.Service.IntegrationTests
```

## Contract artifact

Create:

```text
I<Capability>Manager.cs
```

The interface is intentionally empty during construction.

## Service artifacts

Create:

```text
<Capability>Manager.cs
<Capability>ManagerModule.cs
```

The implementation:

- is `public sealed`
- inherits `ComponentBase<<Capability>Manager>`
- implements `I<Capability>Manager`
- implements `IHealthCheck`
- receives `ILogger<<Capability>Manager>` first

## Responsibility

Manager owns workflow/orchestration volatility. Do not generate substantive independent business algorithms into the Manager scaffold.
