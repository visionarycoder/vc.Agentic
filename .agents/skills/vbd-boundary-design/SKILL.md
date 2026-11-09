---
name: "vbd-boundary-design"
description: "Design VBD boundaries, contracts, role authority, and team relationship policy without false canonical claims."
metadata:
  metadata-version: "1.0.0"
  title: "VBD boundary design"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "vbd"
---

# VBD boundary design

## When to use

Use this skill when architecture work needs component authority, contracts, call policy, or design packets.
Load `vbd-method` first when source classification is absent.
Use `vbd-design-validation` for simulation, review, or QA checks.

## Boundary contract

A boundary hides one reason to change from its callers.
The caller depends on a stable contract, not downstream data types.
The contract states owner, payload, failure behavior, compatibility rule, and mapper location.
A local repository rule takes precedence when it requires a stricter immediate contract.

## Team relationship policy

This matrix is team policy. It is not a verified complete Lowy standard.

| Caller | Allowed target | Rule |
| --- | --- | --- |
| Client | Manager | Use a Manager for activity invocation and presentation boundary separation. |
| Manager | Engine | Use this path when Manager orchestration needs business policy or calculation. |
| Manager | Resource Access | Use this path when no Engine policy is present. Do not force pass-through Engine use. |
| Engine | Resource Access | Use this path when policy needs mechanism data or persistence. |
| Resource Access | Resource | Keep mechanism and provider mapping in Access. |
| Any component | Utility | Use Utility for crosscutting infrastructure only. |

Review direct peer Manager chains and queued interactions separately.
Do not treat asynchronous syntax as automatic mediation.
Reject dependency cycles unless an explicit architecture exception owns the risk.
Inspect upward calls and callbacks by dependency effect. Do not use an unverified universal claim.

## Design packet procedure

1. List activities, triggers, results, and likely changes.
2. Select component roles from authority, not from folders or entities.
3. Define the caller-facing contract for each boundary.
4. Assign mapping at the immediate boundary transition.
5. Record the relationship policy used for each call.
6. Record exceptions with source, scope, rationale, and owner.

## Required output

- Activity map with credible change evidence.
- Authority matrix with Client, Manager, Engine, Resource Access, Resource, or Utility roles.
- Contract ownership table with payload and failure behavior.
- Relationship matrix with allowed calls and exceptions.
- Change simulation table that points to responsible components.

## References

- [Relationship policy](references/relationship-policy.md)
- [Contract ownership](references/contract-ownership.md)
- [Design packet](references/design-packet.md)
