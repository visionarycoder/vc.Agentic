---
metadata-version: "1.0.0"
title: "VBD Service Model"
description: "Preserve scoped source guidance for vbd-service-contracts."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# VBD Service Model

Use this skill to build VBD components around a shared System.ServiceModel-style boundary instead of repeating local wiring, metadata, and validation conventions.

Use this skill first for manager, engine, and access vault work; treat it as the default starting point, not an add-on.

This skill defines the architectural boundary shape. It does not require a network hop, and it does not require CoreWCF unless you are actually hosting ServiceModel contracts over CoreWCF.

Pair with [../solid-principles/SKILL.md](../../../../solid-principles/SKILL.md) for responsibility and dependency-shape refactors, and [../dry-principles/SKILL.md](../../../../dry-principles/SKILL.md) for repeated-code cleanup after the boundary shape is set.

Read [references/service-model-vbd.md](../../service-model-vbd.md) when you need the component checklist or the vault-specific mapping rules. Use [../vbd-rules/references/service-model-default-path.md](../../../../vbd-rules/references/service-model-default-path.md) for the default sequencing and shared shape.

Pair this skill with:

- [../vbd-rules/SKILL.md](../../../../vbd-rules/SKILL.md) for boundary and volatility rules.
- [../vbd-manager-vault/SKILL.md](../../../../vbd-manager-components/SKILL.md), [../vbd-engine-vault/SKILL.md](../../../../vbd-engine-components/SKILL.md), or [../vbd-access-vault/SKILL.md](../../../../vbd-access-components/SKILL.md) for vault-specific shape.
- [../token-efficient-implementation/SKILL.md](../../../../token-efficient-implementation/SKILL.md) when the task is a focused implementation slice.
- [../roslyn-analyzer-rule-composition/SKILL.md](../../../../roslyn-analyzer-rule-composition/SKILL.md) and [../roslyn-codefix-rule-composition/SKILL.md](../../../../roslyn-codefix-rule-composition/SKILL.md) when adding guardrails.

## Workflow

1. Start with the default path reference.
2. Identify the vault type and its single volatility axis.
3. Define the `Contract`/`Service` boundary before writing implementation code.
4. Map the component to manager, engine, or access responsibilities.
5. Reuse the canonical VBD rules from [../vbd-rules/SKILL.md](../../../../vbd-rules/SKILL.md) for every decision.
6. Keep the generated or authored surface deterministic, explicit, and easy to test.
7. Prefer the smallest code shape that preserves the boundary and testability.

## Guardrails

- Keep one volatility axis per vault.
- Keep service-model contracts stable and explicit.
- Keep the `Contract` project public and the `Service` project hidden.
- Treat CoreWCF as a hosting/runtime concern, not as the definition of the boundary.
- Avoid leaking transport, storage, or framework types across the boundary.
- Keep transport-specific error models, including HTTP `ProblemDetails`, in adapters instead of universal contracts unless the contract is explicitly HTTP-native.
- Prefer constructor-injected dependencies and deterministic composition.
- Add validation for null, empty, whitespace, or unsupported configuration before generating code.
- For generated implementations, keep `ILogger<T> logger` as the first constructor argument.
- For public async methods, keep `CancellationToken ct` as the trailing parameter when cancellation is supported.
- Preserve the manager/engine/access separation:
  - manager = orchestration and policy flow
  - engine = pure capability and strategy
  - access = external integration and schema mapping

## Component Shape

Use the smallest shape that satisfies the vault:

- manager vault
  - expose business intent, not infrastructure detail
  - compose stable contracts, not concrete dependencies
- engine vault
  - expose pure capability contracts
  - inject nondeterminism explicitly
- access vault
  - isolate protocol and provider specifics
  - map external schema at the boundary

When a component is service-facing, prefer explicit service contracts and data contracts in the `Contract` project. When a component remains in-process only, preserve the same boundary discipline even if no remote host is introduced.

## Tests And Checks

- Verify the happy path for the vault type you are building.
- Verify bad inputs fail early and clearly.
- Verify boundary leakage does not occur.
- Verify ordering and composition are deterministic.
- Verify code fixes or generators preserve the intended vault shape.
- Verify generated constructors and async method signatures follow the shared conventions.

## Use The Reference

- Read the reference when choosing component shape, boundary responsibilities, or test coverage.
- Keep this file as the short operational guide.
