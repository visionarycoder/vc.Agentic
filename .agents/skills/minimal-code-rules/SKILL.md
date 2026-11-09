---
name: "minimal-code-rules"
description: "Apply Karpathy's coding rules (think before coding, simplicity first, surgical changes, goal-driven execution) to design and code so the team writes the minimum that fulfills the requirements and no more."
metadata:
  metadata-version: "1.0.0"
  title: "Minimal Code Rules"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Minimal Code Rules

Four rules, from Andrej Karpathy's observations on how coding agents go wrong. `developer` and `application-architect` follow them. `solution-architect` (critic mode) and `code-critic` enforce them.

## Rules

| Rule | Meaning | Violation |
|---|---|---|
| 1. Think before coding | State assumptions. When a requirement is ambiguous, ask or list the interpretations. Do not pick one silently. | Code built on an unstated assumption |
| 2. Simplicity first | Write the minimum code that fulfills the requirement. Nothing speculative. | An abstraction used once, a configuration option nobody asked for, error handling for a case that cannot occur, a feature beyond the requirement |
| 3. Surgical changes | Touch only what the requirement needs. Match the existing style. Remove only what your change made unused. | A drive-by refactor, reformatting, or an unrelated fix in the same change |
| 4. Goal-driven execution | Turn each requirement into a verifiable success criterion and loop until it passes. | Work with no test or check that proves the requirement is met |

## Simplicity Test

Ask of every type, method, parameter, option, layer, and line: which requirement needs this? When none does, delete it. A component that has no stated axis of volatility is also a violation.

Rule of thumb: when a senior engineer would call the change overcomplicated, simplify it.

## What Is Not Gold Plating

- Unit and tier tests that the test plan requires.
- Controls that the non-functional requirements, security review, or the layer rules require.
- A mapped value that the mapping specification lists.

## Review Checks

| Check | Test | Pass criteria |
|---|---|---|
| Traceability | Map each type, method, and option to a requirement or stated volatility. | Every element traces to one. |
| Speculation | Search for unused parameters, single-use abstractions, extension points, and options. | None exist without a requirement. |
| Diff size | Compare the changed lines to the work item. | Every changed line serves the work item. |
| Adjacent edits | Look for formatting, renames, or refactors outside the requirement. | None. |
| Verification | Find the test or check for each success criterion. | Each criterion has one that passes. |

A violation is a rejection reason. The rejection names each element, the requirement it lacks, and the deletion that fixes it.
