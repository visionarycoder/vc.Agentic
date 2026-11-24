---
name: "msbuild-intake-router"
description: "Route build-system requests to the minimum correct MSBuild skill by separating modernization, diagnostics, organization, parallelism, output clashes, and binary-log analysis."
metadata:
  metadata-version: "1.0.0"
  title: "MSBuild Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# MSBuild Intake Router

Agent routes MSBuild and build-system work to one primary build skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Msbuild Intake Router work | Use this skill |
| Request falls inside the msbuild suite and needs this specific surface | Use this skill |
| The routed catalog needs a single current-state owner for this concern | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is already narrowed to one execution skill | Use that execution skill |
| Request belongs to a different suite | Use the correct suite router |
| Request is not skill-catalog routing work | Use the matching domain skill |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad msbuild routing belongs here. |
| Current-state rule | Agent treats this skill catalog as the only valid current state. |
| Scope control | Agent keeps this skill focused on one clear concern. |
| Skill loading | Agent loads one primary surface first and adds only concrete secondary support. |

## Verification

- [ ] Agent chose one primary MSBuild skill
- [ ] Agent used secondary skill only when the primary workflow required it
- [ ] Agent avoided loading multiple MSBuild peers for one narrow concern

## Routing Table

| Intent | Primary skill | Optional secondary |
|---|---|---|
| Output or intermediate path clash | `check-bin-obj-clash` | none |
