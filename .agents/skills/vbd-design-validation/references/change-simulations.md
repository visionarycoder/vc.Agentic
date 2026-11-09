---
title: VBD Change Simulations
doc_type: reference
status: active
last_updated: 2026-09-28
---

# VBD change simulations

## Simulation format

| Field | Content |
| --- | --- |
| Scenario | Plausible change with source or business evidence. |
| Changed components | Components that change for this scenario. |
| Unchanged contracts | Contracts that remain stable for callers. |
| Failure path | Error or fallback behavior affected by the change. |
| Regression check | Test or inspection that proves containment. |
| Classification | Rule class and source. |

## Pass conditions

- A credible change changes the expected component set.
- Unrelated contracts remain unchanged.
- The simulation includes one failure path when errors cross the boundary.
- The result does not depend on a fixed component count.
