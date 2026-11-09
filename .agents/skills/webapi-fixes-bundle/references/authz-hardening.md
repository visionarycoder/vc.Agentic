---
title: Authorization Hardening Playbook
doc_type: reference
status: active
last_updated: 2026-08-14
---

# Authorization Hardening

Enforce role and permission checks consistently; ensure protected endpoints return intended 401/403 responses.

## Patterns

| Pattern | Issue | Fix |
|---|---|---|
| Missing `[Authorize]` attribute | Endpoint accessible without authentication | Add `[Authorize]` or equivalent middleware check |
| Overly permissive roles | `[Authorize(Roles = "Admin, User, Guest")]` on sensitive operations | Restrict to minimal required roles |
| No permission check on resource | Authenticated user can access any resource ID | Verify user owns or has permission to access the resource |
| Hardcoded user checks | `if (userId == 1) { ... }` | Use role claims or explicit permission service |
| Missing 401/403 responses | Endpoint returns 500 or redirects instead of 401/403 | Configure authentication/authorization middleware to return correct status |

## Verification

Test: Request endpoint as anonymous, as authorized user, as user without permission.
Pass: Anonymous returns 401. Unauthorized returns 403. Authorized user succeeds.
