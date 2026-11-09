---
title: Access Scaffold
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Access Scaffold

## Required projects

```text
Access.<Capability>.Contract
Access.<Capability>.Service
Access.<Capability>.Service.UnitTests
Access.<Capability>.Service.IntegrationTests
```

## Contract artifact

Create:

```text
I<Capability>Access.cs
```

The interface is intentionally empty during construction.

## Service artifacts

Create:

```text
<Capability>Access.cs
<Capability>AccessModule.cs
```

The implementation:

- is `public sealed`
- inherits `ComponentBase<<Capability>Access>`
- implements `I<Capability>Access`
- implements `IHealthCheck`
- receives `ILogger<<Capability>Access>` first
- receives private resource contexts after the logger when ORM resources exist

## Multiple resource contexts

Multiple contexts are valid only when they are private implementation details of one external capability.

Document the rationale in the component README so the edge case does not become a general license to combine unrelated databases.
