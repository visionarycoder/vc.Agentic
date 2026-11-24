---
name: "roslyn-ca1860-solution-fix"
description: "Apply CA1860 (prefer Count/Length/IsEmpty over Enumerable.Any()) safely across a full .NET solution."
metadata:
  metadata-version: "1.0.0"
  title: "CA1860 Solution Fix Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# CA1860 Solution Fix Skill

Use this skill to remediate CA1860 findings at scale while preserving behavior.

## Intent

Replace parameterless `Any()` calls with direct collection size checks when the target type already exposes efficient members like `Count`, `Length`, or `IsEmpty`.

## Safe Replacement Rules

Apply replacements only when semantics are equivalent and the receiver has a direct size API.

- `collection.Any()` -> `collection.Count > 0`
- `!collection.Any()` -> `collection.Count == 0`
- `array.Any()` -> `array.Length > 0`
- `!array.Any()` -> `array.Length == 0`
- `immutableArray.Any()` -> `immutableArray.Length > 0`
- `!immutableArray.Any()` -> `immutableArray.Length == 0`
## Do Not Rewrite

Do not rewrite `Any()` when the expression has side effects that a rewrite would duplicate, or when null semantics would change.

## Notes for Roslyn Projects

For analyzers/code fixes/generators, prefer conservative changes and keep transformations deterministic.
