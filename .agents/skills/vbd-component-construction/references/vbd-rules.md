---
title: VBD Rules
doc_type: reference
status: active
last_updated: 2026-08-14
---
# VBD Rules

## Mission of the decomposition

A component isolates one independently changing area of behavior, workflow, or external resource behind a stable public contract.

The component README must explain both what the component owns and what it does not own. Boundary definition is more important than project count.

## Vault meanings

### Manager

Owns workflow and orchestration volatility.

A Manager may coordinate Engines and Access components. It should not become the home for substantive business algorithms that can vary independently.

### Engine

Owns business capability, rule, algorithm, calculation, transformation, validation, or other behavior volatility.

Only Engine capabilities use the gerund naming rule.

### Access

Owns external resource and integration volatility. The caller sees the capability contract, not the storage technology, protocol, vendor schema, ORM entity, or remote topology.

An Access component may hide multiple physical databases only when they are collectively part of one external capability and exposing them separately would leak the remote system's implementation complexity.

## Allowed dependency directions

Create dependencies only in these directions:

```text
Client  -> Manager
Manager -> Engine
Manager -> Access
Engine  -> Access
```

Do not create lateral vault-to-vault references by default:

```text
Manager -> Manager
Engine  -> Engine
Access  -> Access
```

Do not create reverse dependencies:

```text
Engine -> Manager
Access -> Engine
Access -> Manager
```

A Service references another component's **Contract**, never its Service implementation.

## Contract purity

The Contract is the black-box boundary.

A Contract project must not reference or expose:

- its Service project
- ORM projects
- EF Core types
- provider SDK types
- module-registration infrastructure
- hosting infrastructure
- configuration infrastructure
- implementation helpers
- another component's private model

Each component/layer owns its own data representation. Do not introduce cross-component `Models`, `Shared.Models`, `Common.Contracts`, or similar convenience assemblies.

## Access privacy

ORM entities, EF Core configuration types, and resource contexts are private to the Access component.

They may be used by:

- the matching Access Service
- the matching ORM project
- the matching ORM integration tests

They must not cross the Contract boundary.

## Host is not a vault

`Host` is a deployment/composition technology detail, not a fourth vault type. It owns startup, runtime composition, configuration, observability, and hosting only.

## Scaffold-only rule

Do not invent activities or business APIs while constructing a component. The initial public interface is intentionally empty.
