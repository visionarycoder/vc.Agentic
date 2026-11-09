---
name: "contract-testing"
description: "Verify cross-layer and external-system contracts with consumer-driven checks, schema comparison, and mapping tests."
metadata:
  metadata-version: "1.0.0"
  title: "Contract Testing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Contract Testing

Load this skill when `integration-tester` writes tests in `tests/contract/**`. Also load `vbd-boundary-contract-mapping`.

## When to use

## Procedure

1. Identify the boundary and both parties from the detailed design. Record the contract source: OpenAPI document, JSON Schema, XSD, flat-file layout, or the public C# interface.
2. Write the **provider check**: the real provider produces output that validates against the contract source.
3. Write the **consumer check**: the real consumer accepts every example in the contract, including optional-field omissions and unknown extra fields.
5. Write **compatibility tests**: compare the current contract to the last released one. Removing a field, narrowing a type, or adding a required field fails the test. Adding an optional field passes.
6. Store golden files (contract examples, expected outputs) in `tests/data/contracts/`. Change a golden file only with a matching contract change in the same work item.
7. Cover error contracts: the response carries RFC 9457 Problem Details with no stack trace or internal path.

## Layer Checks

| Boundary | Verify |
|---|---|
| Client → Manager | Request and response schema, status codes, error contract |
| Manager → Engine / Access | Method signature and argument semantics match the surface map |
| Message | Schema, required fields, ordering and duplicate tolerance stated in the contract |
| File interface | Field offsets, lengths, padding, and encoding |

## Rules

- A contract test fails on any difference the contract forbids.
- Never derive the expected result from the implementation. Derive it from the contract source.
- A contract change without a surface-map update is a defect. Report it to `application-architect`.
