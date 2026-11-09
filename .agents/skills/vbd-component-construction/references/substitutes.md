---
title: Simulator and Emulator
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Simulator and Emulator

Simulator and Emulator are optional executable substitutes that look like the real implementation from the consumer's perspective.

## Shared requirements

Each substitute:

- references the component Contract
- implements the same VBD interface as the real Service
- implements `IHealthCheck`
- inherits `ComponentBase<T>`
- receives logger first
- has its own `Module` class

## Simulator

Use for controlled/artificial behavior such as:

- predefined responses
- deterministic scenarios
- latency scenarios
- failure scenarios
- controlled testing

Naming:

```text
<VaultType>.<Capability>.Simulator
<Capability><VaultType>Simulator
<Capability><VaultType>SimulatorModule
```

## Emulator

Use when consumers need realistic component behavior before the real implementation is complete or while the real dependency is unavailable.

Naming:

```text
<VaultType>.<Capability>.Emulator
<Capability><VaultType>Emulator
<Capability><VaultType>EmulatorModule
```

## Runtime composition

The real Service is the default.

Simulator or Emulator requires explicit runtime/test composition.

Do not put implementation-selection conditionals into consumers.

Do not depend on DI registration order to choose an implementation.

## Simultaneous cloud exposure

When Service, Simulator, and Emulator must all be available simultaneously, expose them through explicit runtime/hosting topology so the caller can intentionally select an endpoint/instance that implements the same logical Contract.

That selection is a deployment/composition concern, not a Contract concern.
