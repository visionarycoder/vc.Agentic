---
metadata-version: "1.0.0"
title: "VBD Manager Vault Skill"
description: "Preserve scoped source guidance for vbd-manager-components."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# VBD Manager Vault Skill

Use [vbd-service-model](../../../../vbd-service-contracts/SKILL.md) first, then use this skill for the manager-specific vault shape and orchestration rules. Pair with [vbd-rules](../../../../vbd-rules/SKILL.md). Read [../vbd-rules/references/service-model-default-path.md](../../../../vbd-rules/references/service-model-default-path.md) for the shared default path.

When the work is a small implementation slice, pair this skill with [token-efficient-implementation](../../../../token-efficient-implementation/SKILL.md).

This skill builds manager vaults. It must apply every rule in [.agents/skills/vbd-rules/SKILL.md](../../../../vbd-rules/SKILL.md).

## Vault Purpose

A manager vault coordinates business policies and orchestration logic that changes with workflow and policy volatility.

## Volatility Axis

Manager vault volatility axis: policy orchestration and use-case flow.

If a concern is primarily algorithmic runtime strategy or infrastructure access detail, it does not belong here.

## Boundary Rules

1. Manager vault may depend on stable domain contracts.
2. Manager vault may call engine and access vault contracts, but must not embed their internals.
3. Manager vault must not contain transport, serialization, or storage-specific code.
4. Manager vault APIs express intent in business terms, not technical protocol terms.
5. Managers communicate with sibling managers only through the shared message bus wrapper.
6. When using the ServiceModel default path, public manager contracts belong in the `Contract` project and orchestration logic remains in the `Service` project.

## Analyzer Mapping

Use canonical VBD0001-VBD0006 plus manager-specific checks:

| Rule ID | Default Severity | Summary |
|---|---|---|
| VBD1001 | Error | Manager vault contains access implementation detail |
| VBD1002 | Warning | Manager API exposes engine tuning knobs |
| VBD1003 | Warning | Manager method mixes multiple policy axes |

## Code Fix Guidance

1. Extract access detail into access vault contract.
2. Extract algorithm tuning into engine vault contract.
3. Split manager methods by policy axis when VBD1003 is triggered.

## Generator Guidance

When generating manager vault components:

1. Start from ServiceModel contract semantics and the `Contract`/`Service` split.
2. Generate business-intent interfaces first.
3. Generate orchestration methods that compose contracts, not concrete dependencies.
4. Keep DI in the composition root; do not let manager code resolve services ad hoc.
5. Treat CoreWCF as a hosting option only when the manager contract is actually hosted remotely.
6. Emit diagnostics metadata for VBD1001-VBD1003 where generation input is ambiguous.
