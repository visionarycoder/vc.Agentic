---
title: Reconciliation
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Reconciliation

The skill is idempotent and safely rerunnable.

## Existing artifacts

```text
present + valid -> reuse
missing         -> create
conflicting     -> report and preserve
```

Do not silently overwrite developer code.

## Duplicate component invocation

If the vault/capability already exists:

- tell the developer that duplication was detected
- reconcile missing scaffold artifacts
- reuse valid projects
- reuse valid `.slnx` entries
- reuse valid project references
- report conflicts

## README preservation

If the component README already has `Mission`, `Responsibilities`, or `Out of Scope`, do not silently rewrite those architectural decisions.

Add a missing section only when it can be done without changing existing intent.

## Git safety

Inspect Git status before generation.

Never automatically:

- reset
- clean
- revert
- discard unrelated changes
- commit

Avoid touching unrelated modified files.
