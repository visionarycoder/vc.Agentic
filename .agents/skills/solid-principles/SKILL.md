---
name: "solid-principles"
description: "Apply SOLID design principles when creating or refactoring code, especially when a change needs clearer responsibilities, smaller abstractions, easier substitution, or better dependency boundaries."
metadata:
  metadata-version: "1.0.0"
  title: "SOLID Principles"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "core"
---

# SOLID Principles

Use this skill when code needs better structure, lower coupling, or clearer extension points.

Pair with [token-efficient-implementation](../token-efficient-implementation/SKILL.md) when you are making the actual code changes.

## Workflow

1. Identify the main responsibility under change.
2. Check whether the type or module has more than one reason to change.
3. Split responsibilities before adding new behavior.
4. Prefer interfaces or abstractions only where they reduce coupling.
5. Keep dependencies pointing toward stable contracts.
6. Verify the result with the smallest possible code change and focused tests.

## Principle Check

- Single Responsibility: one reason to change per type.
- Open/Closed: extend behavior without rewriting stable code.
- Liskov Substitution: derived types must honor the base contract.
- Interface Segregation: keep interfaces small and role-focused.
- Dependency Inversion: depend on abstractions, not concrete details.

## Guardrails

- Remove duplicated responsibilities before adding new abstractions.
- Avoid speculative patterns; use the simplest structure that solves the change.
- Preserve existing behavior unless the user asked for a breaking refactor.
- Prefer constructor injection and explicit contracts for new dependencies.
- If the change is mostly duplication removal, use [dry-principles](../dry-principles/SKILL.md) instead.

## Output Expectation

- Explain the design issue briefly.
- Make the smallest coherent refactor.
- Add or update tests for happy path, bad inputs, and edge cases where relevant.
