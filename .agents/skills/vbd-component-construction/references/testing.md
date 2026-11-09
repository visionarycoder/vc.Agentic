---
title: Testing
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Testing

Create unit and integration test projects for every component by default.

## Service test projects

```text
<VaultType>.<Capability>.Service.UnitTests
<VaultType>.<Capability>.Service.IntegrationTests
```

References:

```text
Service.UnitTests
    -> Service
    -> Contract

Service.IntegrationTests
    -> Service
    -> Contract
```

Do not generate meaningless placeholder tests such as `Test1`.

## ORM integration tests

For each Access ORM project:

```text
Access.<Capability>.Orm.<Resource>.IntegrationTests
    -> Access.<Capability>.Orm.<Resource>
```

Do not reference the Service project from ORM integration tests.

## Framework choice

Follow repository convention when it is clear.

If the repository contains both legacy and modern test conventions, ask which one should be used for the new component.

## Fakes in tests

Tests may explicitly register the Simulator or Emulator in an isolated `IServiceCollection` without using runtime `ModuleRegistry` discovery.

The real implementation remains the default outside explicit test/runtime substitution.
