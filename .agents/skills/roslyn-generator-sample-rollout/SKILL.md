---
name: "roslyn-generator-sample-rollout"
description: "Implement generator-family sample slices in compact family batches. Use this for attribute-input samples, generated contract consumption examples, and runnable documentation for vc.Generators."
metadata:
  metadata-version: "1.0.0"
  title: "Generator Sample Rollout"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Generator Sample Rollout

## Purpose

Use this skill to implement one generator family sample at a time with stable attribute inputs and contract-focused consumer examples.

## Scope

- `samples/FeatureGuides/Generators/*`
- related guide index updates

## Required Rules

### GSR0001: One Family Per Slice

Each run covers one generator family only:
- `Api`
- `CrossCutting`
- `Data`
- `Design`
- `Distributed`
- `Domain`
- `Dx`
- `Governance`
- `Observability`
- `Packs`
- `Resilience`
- `Security`

### GSR0002: Attribute-to-Contract Pattern

Each sample must show:
1. annotated input source,
2. expected generated contract surface,
3. consumer usage that depends on contract, not formatting.

### GSR0003: Deterministic Assertions

Document member/API expectations, not generated file header or whitespace assumptions.

### GSR0004: Runnable Verification

Every slice must be verifiable via:
- `dotnet build samples/FeatureGuides/FeatureGuides.csproj`
- `dotnet test tests/vc.Generators.Tests`

### GSR0005: Anti-Pattern Inclusion

Each family sample must show at least one misuse to avoid, such as relying on generated file layout or shadowing generated names.

## Token-Efficient Workflow

1. Pick one family from the rollout plan.
2. Extend the existing `FeatureGuides` project instead of creating a new app.
3. Add one input file, one consumer example, and one short README section.
4. Prefer grouped family examples rather than one file per generator when the contract pattern is shared.
5. Stop after one family is validated.

## Output Contract

1. Family implemented.
2. Attributes and generated contracts covered.
3. Files added/updated.
4. Validation commands run.
5. Next family recommended.
