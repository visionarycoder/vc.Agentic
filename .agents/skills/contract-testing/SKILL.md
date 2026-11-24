---
name: "contract-testing"
description: "Verify cross-layer and external-system contracts with consumer-driven checks, schema comparison, and mapping tests."
metadata:
  metadata-version: "1.0.0"
  title: "Contract Testing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Contract Testing

Load this skill when `integration-tester` writes tests in `tests/contract/**`. Also load `vbd-boundary-contract-mapping`.

## When to use

## Procedure

1. Identify the boundary and both parties from the detailed design. Record the contract source.
2. Write provider, consumer, and compatibility checks against that source. Compatibility compares the current contract to the last released one.
3. Store golden files (contract examples, expected outputs) in `tests/data/contracts/`. Change a golden file only with a matching contract change in the same work item.
4. Cover error contracts: the response carries RFC 9457 Problem Details with no stack trace or internal path.

## Rules

- Derive expected results from the contract source, never from the implementation.
- A contract change without a surface-map update is a defect. Report it to `application-architect`.
