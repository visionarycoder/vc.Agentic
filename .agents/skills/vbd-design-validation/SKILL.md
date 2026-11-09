---
name: "vbd-design-validation"
description: "Validate VBD designs with change simulations, anti-examples, role checks, and acceptance-to-test evidence."
metadata:
  metadata-version: "1.0.0"
  title: "VBD design validation"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "vbd"
---

# VBD design validation

## When to use

Use this skill for Principal Engineer validation, code review, QA, and documentation checks of VBD work.
Use `vbd-method` for source classification.
Use `vbd-boundary-design` for boundary and contract creation.

## Validation procedure

1. Select at least two credible change scenarios.
2. For each scenario, record changed components and unchanged contracts.
3. Verify that each unchanged caller keeps the same contract.
4. Search for entity, folder, service-count, and mandatory DTO anti-patterns.
5. Verify that each role applies its required VBD obligation.
6. Record source classification and evidence limits for each conclusion.

## Role obligations

| Role | VBD obligation |
| --- | --- |
| Business Analyst | Provide needs, business invariants, and credible change evidence. |
| Principal Engineer | Own decomposition authority, contract boundaries, and accepted exceptions. |
| Technical Researcher | Provide evidence only. Do not execute, write files, or assign owners. |
| Software Engineer | Implement only the assigned component and preserve approved contracts. |
| Code Reviewer | Check independent rule evidence, change containment, and local rule precedence. |
| QA | Test behavior, failure paths, and change simulation effects. |
| Technical Writer | Document accepted behavior and limits after validation. |

## Negative tests

- Reject decomposition by entity when change evidence differs from noun boundaries.
- Reject decomposition by folder when authority and contracts are absent.
- Reject a target component count when no change evidence supports it.
- Reject mandatory DTO creation when no independent evolution evidence exists.
- Reject an Open/Closed Principle answer when it omits volatility evidence.

## References

- [Change simulations](references/change-simulations.md)
- [Worked examples](references/worked-examples.md)
- [Reviewer and QA checks](references/reviewer-qa-checks.md)
