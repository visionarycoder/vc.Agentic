---
title: Validation
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Validation

Validate only the component artifacts and references created or modified by this skill. Repository-wide VBD validation belongs to a separate skill.

## Contract purity

Fail generated architecture validation if the new Contract:

- references Service
- references ORM
- exposes EF Core types
- exposes provider SDK types
- exposes module infrastructure
- exposes hosting infrastructure
- exposes another component's private model

## Dependency direction

Fail if generated project references violate the allowed VBD directions.

A Service may reference another component's Contract. It must not reference another component's Service.

## Access privacy

Verify ORM models and EF Core configuration remain private to the Access component.

## Naming

Verify:

- Engine capability is gerund-normalized
- module types use `Module`
- resource contexts use symbolic names and omit `DbContext` from the class name
- no generated identifiers use underscore prefixes
- implementation classes are `public sealed` unless a framework requires otherwise

## Substitutes

Verify Simulator and Emulator:

- reference Contract
- implement the same public VBD interface
- implement `IHealthCheck`
- inherit `ComponentBase<T>`
- are not implicit production defaults

## Host

Verify Host is composition/deployment infrastructure only.

## Build

Run restore, then build generated projects, then build the selected solution when practical.

Treat failure of generated projects as a scaffold failure.

If the selected solution fails for unrelated pre-existing reasons, report those separately.

Do not roll back generated artifacts after a build failure.
