---
name: "vbd-rules"
description: "Canonical Juval Lowy volatility-based decomposition rules shared by analyzers, code fixes, generators, and human-authored components."
metadata:
  metadata-version: "1.0.0"
  title: "VBD Canonical Rules"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "vbd"
---

# VBD Canonical Rules

Use this skill as the single source of truth for all VBD checks and generation.

## Intent

Apply Juval Lowy's volatility-based decomposition (VBD) to model components around change drivers. A component boundary is valid only when all members of the boundary change for the same reason and at the same cadence.

## ServiceModel Default Path

For manager, engine, and access vault work, start with [references/service-model-default-path.md](references/service-model-default-path.md). Treat the service model as the default boundary shape, not an optional add-on.

In this repository, "ServiceModel" means `System.ServiceModel` contract semantics and the explicit `Contract`/`Service` split. CoreWCF is a valid hosting/runtime option for those contracts, but it is not the architectural source of truth.

## Core Principles

1. Decompose by volatility, not by technical layer.
2. Keep stable policies separate from volatile implementation details.
3. Minimize cross-boundary coupling and transitive knowledge.
4. Make boundaries explicit, enforceable, and testable.
5. Prefer dependency inversion from volatile areas toward stable contracts.

## ServiceModel Boundary Rules

Apply these rules when a component uses the shared ServiceModel pattern:

1. The boundary spans the `Contract` and `Service` projects.
2. Only the `Contract` project exposes public abstractions, data contracts, and service contracts.
3. The `Service` project keeps implementation details internal or private.
4. Callers reference the contract only; DI or hosting binds the contract to the service implementation.
5. Managers do not call sibling managers directly; they use the shared message bus wrapper.
6. All vaults may reference `Utilities` and `Ifx` when needed, but not as a shortcut around boundary rules.
7. Transport-specific projections such as HTTP `ProblemDetails` belong in adapters or hosts, not in the canonical boundary rule set.

## Universal Rules (Apply To All Vault Types)

1. Single Volatility Axis Rule
- Each vault owns exactly one primary volatility axis.
- If two unrelated change drivers are found, split the vault.

2. Stable Contract Rule
- Public contracts must be stable relative to the vault's volatility axis.
- Breaking changes require explicit versioning/migration.

3. Inbound/Outbound Rule
- Inbound dependencies may target stable contracts only.
- Outbound dependencies must not create cyclic coupling.

4. No Leakage Rule
- Internal data models, persistence concerns, and protocol details do not cross the vault boundary.
- Contract-project public types are the only supported boundary surface for ServiceModel components.
- Service-project implementation details remain hidden behind DI and must not leak outward.

5. Boundary Outcome Rule
- Boundary failures must be expressed as explicit, contract-safe outcomes.
- Use declared faults, result envelopes, or host-specific error projections as appropriate to the contract.
- Do not treat any single transport mapping as universal VBD law.

6. Deterministic Composition Rule
- Construction and wiring must be deterministic and side-effect free.
- Runtime behavior can be dynamic, but graph shape must be explicit.

7. Testability Rule
- Every rule must map to testable analyzer diagnostics and generator preconditions.
- Code fixes must be semantics-preserving unless marked breaking.

## Analyzer/CodeFix/Generator Alignment Contract

All tooling tracks the same rule IDs and severities.

| Rule ID | Default Severity | Summary |
|---|---|---|
| VBD0001 | Error | Multiple volatility axes inside one vault |
| VBD0002 | Error | Boundary leakage of internal implementation detail |
| VBD0003 | Warning | Unstable public contract without versioning |
| VBD0004 | Error | Cyclic dependency across vault boundaries |
| VBD0005 | Warning | Non-deterministic vault composition |
| VBD0006 | Warning | Missing explicit boundary contract |

## Required Tooling Behavior

1. Analyzer
- Detect violations of VBD0001-VBD0006.
- Report location at declaration and all usage sites where practical.

2. Code Fix
- Offer non-breaking fix first.
- If only breaking fix exists, mark as breaking in title and preview.
- Never silently remove behavior.

3. Generator
- Refuse generation when error-level rules are violated.
- Generate explicit boundaries and contracts, never inferred hidden coupling.
- Emit traceable comments/metadata linking output to rule IDs.

## Decision Checklist

Before accepting any vault definition, answer all:

1. What is the single volatility axis?
2. Which contracts are stable, and what is their versioning strategy?
3. What can cross the boundary, and what cannot?
4. Which dependencies are allowed directions?
5. Which diagnostics and code fixes are expected if violated?
