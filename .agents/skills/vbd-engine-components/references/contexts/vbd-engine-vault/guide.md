---
metadata-version: "1.0.0"
title: "VBD Engine Vault Skill"
description: "Preserve scoped source guidance for vbd-engine-components."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# VBD Engine Vault Skill

Use [vbd-service-model](../../../../vbd-service-contracts/SKILL.md) first, then use this skill for the engine-specific vault shape and rules. Pair with [vbd-rules](../../../../vbd-rules/SKILL.md). Read [../vbd-rules/references/service-model-default-path.md](../../../../vbd-rules/references/service-model-default-path.md) for the shared default path.

When the work is a small implementation slice, pair this skill with [token-efficient-implementation](../../../../token-efficient-implementation/SKILL.md).

This skill builds engine vaults. It must apply every rule in [.agents/skills/vbd-rules/SKILL.md](../../../../vbd-rules/SKILL.md).

## Vault Purpose

An engine vault owns algorithmic and computational behavior that changes with strategy, optimization, and calculation volatility.

## Volatility Axis

Engine vault volatility axis: algorithm and computational strategy.

If a concern is orchestration policy or infrastructure integration detail, it does not belong here.

## Boundary Rules

1. Engine vault contracts are pure capability contracts (compute, evaluate, transform).
2. Engine vault avoids direct storage or transport dependencies.
3. Engine vault is deterministic for same input unless nondeterminism is explicit and injectable.
4. Engine vault does not encode workflow policy sequencing.
5. Engine vault methods should stay narrow and prefer explicit inputs over ambient state.
6. When exposed through the ServiceModel default path, capability contracts belong in the `Contract` project and algorithmic implementation remains in the `Service` project.

## Analyzer Mapping

Use canonical VBD0001-VBD0006 plus engine-specific checks:

| Rule ID | Default Severity | Summary |
|---|---|---|
| VBD2001 | Error | Engine vault references access transport or persistence APIs |
| VBD2002 | Warning | Engine output shape leaks orchestration policy state |
| VBD2003 | Warning | Hidden nondeterminism without explicit dependency injection |

## Code Fix Guidance

1. Introduce interfaces for random/time/environment dependencies.
2. Move policy-state branching to manager vault.
3. Replace concrete infrastructure references with abstractions.

## Generator Guidance

When generating engine vault components:

1. Start from ServiceModel contract semantics and the `Contract`/`Service` split.
2. Generate capability-first interfaces and pure operation contracts.
3. Generate injectable strategy points for nondeterministic behavior.
4. Keep DI at the boundary and avoid service locator patterns inside engine code.
5. Treat CoreWCF as a hosting option only when the engine contract is actually exposed remotely.
6. Emit diagnostics metadata for VBD2001-VBD2003 when input models are ambiguous.
