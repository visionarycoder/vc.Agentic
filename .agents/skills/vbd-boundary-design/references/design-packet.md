---
title: VBD Design Packet
doc_type: reference
status: active
last_updated: 2026-09-28
---

# VBD design packet

| Section | Required content |
| --- | --- |
| Activity map | Trigger, result, actor, and credible change evidence. |
| Volatility table | Business invariant, proposed solution, time axis, customer axis, and source. |
| Component table | Component ID, role, authority, reason to change, and contract. |
| Contract table | Owner, payload, failure behavior, compatibility, and mapper. |
| Relationship table | Caller, callee, policy source, and exception rationale. |
| Simulation table | Change scenario, changed components, unchanged contracts, and test effect. |
| Decision log | Split, merge, and exception decisions with classification and source. |

## Minimal acceptance checks

- Each component has one independent reason to change.
- Each boundary lists the reason that the contract hides.
- Each architecture conclusion lists source, section, scope, and exceptions.
- Local repository rules remain stronger than this global guidance.
