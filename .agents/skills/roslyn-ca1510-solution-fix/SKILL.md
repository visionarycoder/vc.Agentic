---
name: "roslyn-ca1510-solution-fix"
description: "Apply CA1510 (use ArgumentNullException.ThrowIfNull) safely across a full .NET solution."
metadata:
  metadata-version: "1.0.0"
  title: "CA1510 Solution Fix Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# CA1510 Solution Fix Skill

Use this skill to remediate CA1510 findings at scale while preserving behavior.

## Intent

Replace explicit null-guard throws with `ArgumentNullException.ThrowIfNull(...)` where semantics are equivalent.

## Safe Replacement Rules

Apply only when behavior remains the same.

- `if (x is null) throw new ArgumentNullException(nameof(x));` -> `ArgumentNullException.ThrowIfNull(x);`
- `if (x == null) throw new ArgumentNullException(nameof(x));` -> `ArgumentNullException.ThrowIfNull(x);`

Generated-code emitters may be updated similarly if they produce these exact patterns.

## Do Not Rewrite

Do not rewrite when any of the following is true:

- The throw includes a custom message or non-standard constructor arguments.
- The null check is part of a compound condition that changes behavior if simplified.
- The expression is a throw-expression in assignment/initializer (for example `x ?? throw ...`) unless explicitly required.
- Rewriting would alter nullability flow, side effects, or evaluation order.

## Execution Workflow

1. Build the solution to capture baseline diagnostics.
2. Search for explicit `ArgumentNullException` guard patterns.
3. Filter to safe one-to-one CA1510 transformations.
4. Apply minimal deterministic edits.
5. Rebuild the full solution.
6. Run relevant tests for touched projects.

## Validation Checklist

- Build succeeds.
- No semantic changes beyond guard modernization.
- Updated generated-output tests (if generator strings changed) pass.
- No new analyzer or nullable regressions introduced.

## Notes for Analyzer/Generator Repos

Keep changes conservative and deterministic. If guard strings are emitted by generators, update corresponding expected-output tests in lockstep.
