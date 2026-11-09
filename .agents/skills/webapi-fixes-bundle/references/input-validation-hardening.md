---
title: Input Validation Hardening Playbook
doc_type: reference
status: active
last_updated: 2026-08-14
---

# Input Validation Hardening

Ensure all request data is validated before processing; return deterministic 4xx responses for invalid input.

## Patterns

| Pattern | Issue | Fix |
|---|---|---|
| No model validation | Controller accepts request without checking bound properties | Add data annotations or fluent validation; use `[ApiController]` with auto-validation |
| Silent null coercion | Null values accepted without verification | Add `required` keyword or explicit `if (value == null)` check with 400 response |
| Unbounded string/array input | No length or count limits | Add `[StringLength]`, `[MaxLength]`, or explicit bounds checks |
| Missing range validation | Numeric values accepted without min/max check | Add `[Range]` attribute or equivalent bounds verification |
| Type mismatch ignored | String input coerced to type without feedback | Validate format before deserialization; return 400 with reason |

## Verification

Test: Send invalid input (null, oversized, wrong type, empty) to each endpoint.
Pass: Endpoint returns 400 with predictable error contract for all invalid cases.
