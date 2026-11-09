---
name: "dry-principles"
description: "Apply DRY guidance when code repeats logic, rules, or structure and should be consolidated without overengineering. Use when refactoring duplication, extracting helpers, standardizing patterns, or deciding whether shared code is worth introducing."
metadata:
  metadata-version: "1.0.0"
  title: "DRY Principles"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "core"
---

# DRY Principles

Use this skill when repeated code or repeated decisions are making maintenance harder.

Pair with [token-efficient-implementation](../token-efficient-implementation/SKILL.md) when you are turning the extraction into code.

## Workflow

1. Find the repeated behavior, not just the repeated text.
2. Decide whether the duplication is accidental or intentional.
3. Extract the smallest shared unit that removes the repetition.
4. Keep shared code close to the callers when reuse is narrow.
5. Stop extracting once the abstraction starts hiding intent.
6. Verify that the new shape still reads clearly in each call site.

## Guardrails

- Prefer one source of truth for rules, constants, mappings, and branching logic.
- Do not force shared code when the duplication is superficial or likely to diverge.
- Keep abstractions explicit and easy to test.
- Preserve readability; fewer lines is not a win if the code becomes opaque.
- If the main issue is responsibility or dependency shape, use [solid-principles](../solid-principles/SKILL.md) instead.

## Output Expectation

- Point out the duplicated concern and the tradeoff.
- Make the smallest safe extraction or consolidation.
- Add or update tests for the shared path and any affected edge cases.
