---
name: "release-management"
description: "Promote builds through environments with readiness checks, release notes, rollback plans, human production approval, and post-release verification."
metadata:
  metadata-version: "1.0.0"
  title: "Release Management"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Release Management

`release-manager` applies this skill at Gate 6.

## Process

| Step | Action | Pass criteria |
|---|---|---|
| 1. Scope | List the merged work items in the release. | Each item passed Gates 0 to 5. |
| 2. Notes | Write release notes: changes, mapping or schema changes, known issues. | Every work item appears once. |
| 3. Rollback | Write the rollback plan: previous version, data steps, owner. | A person other than the author can follow it. |
| 4. Promote | Deploy to each environment in order and run smoke tests. | Each environment passes before the next. |
| 5. Approve | Request production approval through `administrative-assistant`. | A human approved. |
| 6. Verify | Observe health, errors, and latency for the window set by the non-functional requirements. | Values meet the targets. |
| 7. Close out | Update the release work item. | The state matches the evidence. |

## Rules

- Release a database or schema change only with a tested rollback or forward-fix plan.
- Treat a failed smoke test as a stop; roll back or fix before promotion.
- Keep secrets out of release artifacts.
