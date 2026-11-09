---
metadata-version: "1.0.0"
title: "VBD Access Vault Skill"
description: "Preserve scoped source guidance for vbd-access-components."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# VBD Access Vault Skill

Use [vbd-service-model](../../../../vbd-service-contracts/SKILL.md) first, then use this skill for the access-specific vault shape and boundary mapping rules. Pair with [vbd-rules](../../../../vbd-rules/SKILL.md). Read [../vbd-rules/references/service-model-default-path.md](../../../../vbd-rules/references/service-model-default-path.md) for the shared default path.

When the work is a small implementation slice, pair this skill with [token-efficient-implementation](../../../../token-efficient-implementation/SKILL.md).

This skill builds access vaults. It must apply every rule in [.agents/skills/vbd-rules/SKILL.md](../../../../vbd-rules/SKILL.md).

## Vault Purpose

An access vault owns external integration behavior that changes with infrastructure volatility (datastores, APIs, protocols, auth mechanisms).

## Volatility Axis

Access vault volatility axis: infrastructure and integration detail.

If a concern is business orchestration or algorithmic strategy, it does not belong here.

## Boundary Rules

1. Access vault isolates protocol, persistence, auth, and endpoint specifics.
2. Access vault presents stable contracts to manager/engine vaults.
3. Access vault maps external schemas to internal contracts at the boundary.
4. Access vault does not contain business policy decisions.
5. Access vault hides vendor SDKs and transport details behind abstractions.
6. When using the ServiceModel default path, public access contracts belong in the `Contract` project and provider-specific adapters remain in the `Service` project.

## Analyzer Mapping

Use canonical VBD0001-VBD0006 plus access-specific checks:

| Rule ID | Default Severity | Summary |
|---|---|---|
| VBD3001 | Error | Access vault exposes external schema types across boundary |
| VBD3002 | Warning | Access vault contains business policy branching |
| VBD3003 | Warning | Access vault contract is provider-specific without abstraction |

## Code Fix Guidance

1. Introduce DTO/entity mappers at the boundary.
2. Move policy branches to manager vault.
3. Introduce provider-neutral contracts and adapter implementations.

## Generator Guidance

When generating access vault components:

1. Start from ServiceModel contract semantics and the `Contract`/`Service` split.
2. Generate boundary mapper interfaces and adapter stubs.
3. Generate provider-specific implementations behind stable abstractions.
4. Keep DI registration at the composition root and avoid container access in access logic.
5. Keep HTTP `ProblemDetails` or other transport error projections in the adapter layer instead of the shared contract.
6. Emit diagnostics metadata for VBD3001-VBD3003 when inputs couple to vendor types.
