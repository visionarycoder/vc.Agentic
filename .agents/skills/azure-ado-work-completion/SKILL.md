---
name: "azure-ado-work-completion"
description: "Apply authorized Azure DevOps state transitions. Agents do not close work items. Only a human sets Closed or Resolved."
metadata:
  metadata-version: "1.0.0"
  title: "Complete ADO work items"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "azure"
---

# Complete ADO work items

## When to use

Use this skill to move an existing work item through the SDLC workflow.
This skill wins on the state transitions in the table below.

## Human close rule

Only a human closes a work item.
An agent does not set `System.State` to `Closed` or `Resolved`.
This rule covers Epic, Feature, User Story, Task, and Bug.
`intake`, `architect`, `builder`, `tester`, `reviewer`, and the session agent follow this rule.
Stop when a request asks an agent to close a work item. Report the human-close rule. Do not change that state.

## Authorized transitions

| Type | From | To | Evidence required | Actor |
| --- | --- | --- | --- | --- |
| Task | New | Active | Builder session started on that Task ID. | `builder` |
| Bug | New | Active | Builder session started on that Bug ID. | `builder` |

No row ends at `Closed` or `Resolved`.
Do not delete an item. Do not assign an agent identity.

## Procedure

1. Read the item, its revision, its children, and the evidence named in the table.
2. Stop when the target state is `Closed` or `Resolved`. Return the human-close rule. Do not change state.
3. Stop when any required evidence is missing. Return the missing evidence. Do not change state.
4. Patch `System.State` only for a row in the table. Use a revision test.
5. Read the saved item. Return type, ID, URL, old state, new state, and revision.

## Rollup

An agent does not close a child or a parent.
A human closes a Feature after every child User Story is `Closed`.
A human closes an Epic after every child Feature is `Closed`.
An update that does not ask for completion leaves state unchanged.
