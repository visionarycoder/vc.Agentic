---
name: "roslyn-ca1860-solution-fix"
description: "Apply CA1860 (prefer Count/Length/IsEmpty over Enumerable.Any()) safely across a full .NET solution."
metadata:
  metadata-version: "1.0.0"
  title: "CA1860 Solution Fix Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
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
- For types with `IsEmpty`, prefer `!x.IsEmpty` / `x.IsEmpty` where this is the native idiom.

## Do Not Rewrite

Do not rewrite `Any()` when any of the following is true:

- `Any(predicate)` overload is used.
- The receiver is a deferred `IEnumerable<T>` without a direct size member.
- The expression has side effects that would be duplicated by a rewrite.
- Null semantics would change (for example null-conditional or nullable flow differences).

## Execution Workflow

1. Build the solution and capture CA1860 locations.
2. Search for parameterless `.Any()` usages.
3. Filter to safe call sites with direct size members.
4. Apply minimal deterministic replacements.
5. Rebuild the solution.
6. Re-run tests relevant to touched projects.

## Validation Checklist

- No behavioral change beyond CA1860 compliance.
- No new nullable warnings or analyzer regressions.
- Build succeeds for the full solution.
- Touched tests pass.

## Notes for Roslyn Projects

For analyzers/code fixes/generators, prefer conservative changes and keep transformations deterministic.
