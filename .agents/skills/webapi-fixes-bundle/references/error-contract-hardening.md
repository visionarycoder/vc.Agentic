---
title: Error Contract Hardening Playbook
doc_type: reference
status: active
last_updated: 2026-08-14
---

# Error Contract Hardening

Standardize error responses to RFC 9457 Problem Details; ensure all error paths return consistent shape.

## Patterns

| Pattern | Issue | Fix |
|---|---|---|
| Mixed error shapes | Some endpoints return `{ error: "..." }`, others `{ message: "..." }` | Use Problem Details for all errors: `{ type, title, status, detail }` |
| Status code misuse | 400 for not found, 500 for validation error | Use correct status: 404 for not found, 400 for invalid input, 500 for server failure |
| Exposed internal details | Stack traces, SQL, connection strings in error response | Log sensitive details server-side only; return safe detail message to client |
| No error instance tracking | No way to correlate error to logs | Include `instance` field with correlation ID |
| Missing content-type | Error responses not marked as `application/problem+json` | Set `Content-Type: application/problem+json` in error responses |

## Verification

Test: Trigger validation error, not-found, and server error.
Pass: All errors return Problem Details with correct status and safe detail text.
