---
name: "migrate-to-shoehorn"
description: "Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data."
metadata:
  metadata-version: "1.0.0"
  title: "Migrate to Shoehorn"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Migrate to Shoehorn

## Purpose

Replace `as` assertions in test files with `@total-typescript/shoehorn` helpers (`npm i @total-typescript/shoehorn`). Test code only; never use it in production code.

## Migration

- `as Type` on partial data becomes `fromPartial(...)`.
- `as unknown as Type` becomes `fromAny(...)`. The double assertion bypasses type checking and needs the target type named manually; `fromAny` infers it from the parameter position and keeps autocomplete.
- `fromExact()` forces a full object and can be swapped for `fromPartial` later.

## Workflow

1. Find assertions: `grep -r " as [A-Z]" --include="*.test.ts" --include="*.spec.ts"`
2. Replace them and add imports from `@total-typescript/shoehorn`.
3. Run the type check.
