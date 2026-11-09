---
metadata-version: "1.0.0"
title: "Post-Implementation Cleanup"
description: "Preserve scoped source guidance for post-implementation-cleanup."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Post-Implementation Cleanup

This skill removes low-value implementation debris after a task is complete.
This skill preserves durable docs, current-state guidance, and operational knowledge.

## Classification Table

| Artifact type | Default action | Notes |
|---|---|---|
| Current-state documentation | Keep and update | Agent keeps discoverable docs accurate. |
| Durable runbooks or guidance | Keep | Agent moves files only when placement is wrong. |
| Planning scratch notes | Archive or delete | Agent keeps them only when they retain audit value. |
| Generated investigation logs | Archive when traceability matters, otherwise delete | Agent avoids clutter in active folders. |
| Duplicate summaries | Delete after canonical doc verification | Agent keeps one source of truth. |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Verify | Agent confirms implementation and validation are complete. | Cleanup gate |
| 2. Inventory | Agent lists task-created artifacts in scope. | Artifact inventory |
| 3. Classify | Agent marks each artifact as keep, archive, or delete. | Cleanup plan |
| 4. Remediate | Agent archives or deletes low-value artifacts and updates any remaining references. | Reduced clutter |
| 5. Validate | Agent verifies canonical docs still describe current behavior. | Clean final state |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Completion gate | Review build, test, or validation state. | Cleanup begins only after the implementation work is validated. |
| Canonical docs | Review remaining documentation surfaces. | Current-state docs remain accurate and discoverable. |
| Clutter reduction | Review artifact inventory after cleanup. | Low-value task debris is removed or archived. |
| Link safety | Review references from kept files. | Kept files do not point to deleted artifacts. |
