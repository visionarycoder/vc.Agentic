---
name: "sdlc-review"
description: "Review Kanban handoffs and route verified outcomes."
metadata:
  metadata-version: "1.0.0"
  title: "SDLC Review Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# SDLC Review Skill

Independently verify work handed from a Kanban implementation run to the review lane, then approve it, request changes, or escalate. This skill reviews the deliverable and its evidence; it does not take over the implementer's work.

## When to Use

Use this skill when all of the following are true:

- the dispatcher spawned you for a task claimed from the `review` lane;
- an implementer submitted a `review_requested` handoff;
- the task needs an independent verdict before it can be completed.

Do not use it for a separate downstream review card. A downstream card is ordinary implementation work with a review-oriented specification and completes through its own lifecycle.

## Prerequisites

- A Kanban worker context with the current task and run identifiers.
- Native Kanban tools: `kanban_show`, `kanban_comment`, `kanban_complete`, `kanban_request_changes`, and `kanban_block`.
- Workspace access through `read_file`, `search_files`, and `terminal` when the deliverable is code.
- The task's original specification, acceptance criteria, handoff summary, and prior run history must be available through `kanban_show`.

## How to Run

This skill is loaded automatically by the review dispatcher. Start with `kanban_show` before inspecting files or choosing a verdict.

1. Read the task specification and the latest `review_requested` handoff.
2. Inspect the actual deliverable and run relevant verification.
3. Choose exactly one verdict: approve, request changes, or escalate.
4. Record concrete evidence in the terminal Kanban transition.

## Quick Reference

| Verdict | When | Final action |
|---|---|---|
| Approve | Acceptance criteria and verification pass | `kanban_complete` |
| Request changes | Correctable implementation defects remain | `kanban_comment`, then `kanban_request_changes` |
| Escalate | A human decision or external prerequisite is required | `kanban_block` |

A requested-changes transition returns the task to its original implementer. When that implementer requests review again without naming a reviewer, the persisted reviewer provenance routes the re-review back to the same reviewer profile.

## Review Lenses

Vary the lens each round. Count the `changes_requested` entries in "Prior attempts on this task" (also visible as prior runs in `kanban_show`); the current round is that count plus one.

| Round | Lens | How to apply it |
|---|---|---|
| 1 | Artifact | Read the diff or deliverable cold, before the implementer's summary. Form an independent judgment, then investigate every mismatch with the handoff narrative. |
| 2 | Execution | Check out the work and run it via `terminal`: build, test, and exercise the reported behavior. |
| 3+ | Contract | Re-read the ORIGINAL task body and acceptance criteria and audit strictly against them. Verify every item from every prior `kanban_request_changes` round landed. |

For ad-hoc parallel reviewers via `delegate_task`, give each a different lens (diff-only, full-context, checkout-and-run) rather than identical briefs.

## Procedure

1. Call `kanban_show`; read the task body, acceptance criteria, latest handoff, and prior review findings. Treat the handoff as a claim to verify.
2. Map every acceptance criterion to evidence. For code, inspect changed paths and run the project's existing focused checks; confirm tests assert behavior. For non-code work, inspect the complete deliverable.
3. Choose one verdict and record concrete, non-secret evidence.

- Approve: `kanban_complete(summary="Reviewed and approved. <checks inspected>", metadata={"review_outcome": "approved", "reviewer_checks": [...]})`.
- Request changes: `kanban_comment(task_id=..., body="Changes requested:\n1. <file + defect>\n2. <required correction>")`, then `kanban_request_changes(reason=...)`. State where the defect is, how it reproduces, and what outcome resolves it.
- Escalate: `kanban_block(reason="escalation: <decision or prerequisite required>")`, only for a human decision or external prerequisite.

Do not edit the implementation as reviewer. On re-review, confirm both the requested corrections and preservation of previously passing behavior.

## Pitfalls

- Rubber-stamping a passing handoff summary.
- Vague findings or style-only blocking.
- Using `kanban_block` for ordinary rework.
