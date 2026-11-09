# VBD Service Model Reference

Use this reference with [../SKILL.md](../SKILL.md) when building VBD components around a shared service model.

## Service-Model Purpose

- Remove repeated wiring, metadata, and validation code.
- Keep component boundaries explicit and deterministic.
- Make the default implementation path align with Juval Lowy VBD rules.
- Keep the generated implementation path small enough to reuse across manager, engine, and access vaults.

## Contracts And Decorators

Use decorators to declare the vault role and the service-model shape.

- contract decorators define the intended vault type and boundary intent
- member decorators mark required contracts, optional extension points, and boundary-mapped behavior
- generator or refactor inputs should derive shape from decorators instead of ad hoc conventions

Keep contracts narrow:

- one contract for the vault role
- one contract for the stable external surface
- one set of decorators for rules that the generator or refactor must enforce
- one generated implementation shape per vault type

## Required Inputs

Before creating or updating a component, identify:

- vault type
- single volatility axis
- stable contract surface
- allowed dependencies
- expected diagnostics or guardrails
- sibling skill to use for the vault shape and for token-efficient implementation

## Vault Mapping

### Manager vault

- Model orchestration and policy flow.
- Keep technical infrastructure out of the public surface.
- Use intent-first names.
- Keep manager-to-manager communication on the shared message bus wrapper.

### Engine vault

- Model capability and strategy.
- Keep the implementation pure unless nondeterminism is explicit and injectable.
- Avoid workflow sequencing or access concerns.
- Inject time, randomness, and environment dependencies explicitly.

### Access vault

- Model external integration and schema translation.
- Keep provider-specific details behind a stable contract.
- Avoid policy branching in the access boundary.
- Keep the contract surface provider-neutral.

## ServiceModel Rules

1. Keep the service model small.
2. Keep contracts explicit and stable.
3. Prefer typed members over stringly configuration.
4. Reject invalid inputs before component generation.
5. Preserve deterministic ordering, naming, and file shape.
6. Do not let the model blur vault responsibilities.
7. Generated implementations should use `ILogger<T> logger` as the first constructor argument.
8. Public async methods should use a trailing `CancellationToken ct` when cancellation is supported.

## Implementation Checklist

- define the vault role
- define the service contract
- define allowed dependencies
- define validation rules
- define emitted tests or diagnostics
- verify the final shape against the canonical VBD rules

## Test Checklist

- happy path for the vault role
- null and empty input rejection
- dependency-boundary checks
- deterministic output or registration order
- failure behavior for unsupported combinations
- generated constructor and async method conventions
