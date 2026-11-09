---
title: VBD Contract Ownership
doc_type: reference
status: active
last_updated: 2026-09-28
---

# VBD contract ownership

## Contract record

| Field | Required content |
| --- | --- |
| Boundary | Caller and callee component IDs. |
| Owner | Component that owns the caller-facing contract. |
| Reason hidden | Volatility hidden from callers. |
| Payload | Names and stability rules for values crossing the boundary. |
| Failure | Errors, retry ownership, and partial result behavior. |
| Compatibility | Additive, breaking, versioned, or internal-only rule. |
| Mapper | Mapping component or function at the immediate boundary. |
| Source classification | Primary guidance, Secondary interpretation, Team policy, Repository rule, or Heuristic/Unknown. |

## DTO guidance

Duplicate DTOs only when independent evolution evidence exists.
Do not require a DTO for every boundary.
Do not share downstream DTOs when the caller needs an independently stable shape.
In Financial IDL, keep the local immediate contract and mapping service rule.
