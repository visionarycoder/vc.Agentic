---
title: VBD Component Roles
doc_type: reference
status: active
last_updated: 2026-09-28
---

# VBD component roles

| Role | Authority | Common change driver | Limit |
| --- | --- | --- | --- |
| Client | Presents behavior or invokes an activity boundary. | Presentation, trigger shape, or user workflow entry changes. | A Client does not own core orchestration policy. |
| Manager | Owns sequence, workflow policy, and business orchestration. | Process order, retry choice, authorization flow, or coordination rule changes. | Do not create a Manager with no business logic. |
| Engine | Owns activity policy or calculation rules. | Business rule, validation policy, allocation rule, or calculation changes. | An Engine is not only a pure calculator. |
| Resource Access | Maps mechanisms and providers. | Storage, protocol, vendor, transport, or query mechanism changes. | Access does not own business orchestration. |
| Resource | Owns real state or capability. | Data store, queue, service, device, or external capability changes. | A Resource is not a logical policy owner. |
| Utility | Provides crosscutting infrastructure. | Logging, serialization, clock, metrics, or security helper changes. | Utility does not own business engine rules. |

## Role selection checks

- If a proposed Manager only forwards a call, merge it or record the reason.
- If an Engine depends on a resource mechanism, add Access or explain the stable dependency.
- If a Resource Access component decides business workflow, move that policy to Manager or Engine.
- If a Utility contains business terms, review the boundary for hidden policy.
