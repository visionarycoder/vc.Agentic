---
title: REST Route Standardization Playbook
doc_type: reference
status: active
last_updated: 2026-08-14
---

# REST Route Standardization

Normalize controller routes and HTTP verbs to follow REST conventions and repository patterns.

## Patterns

| Pattern | Issue | Fix |
|---|---|---|
| Non-RESTful verbs in routes | `/api/users/create`, `/api/users/delete/{id}` | Use HTTP method + resource noun: `POST /api/users`, `DELETE /api/users/{id}` |
| Mixed route prefixes | Some routes use `/api/v1`, others `/api` | Standardize on one prefix pattern per controller |
| Inconsistent parameter naming | `{userId}`, `{user_id}`, `{id}` | Use consistent camelCase: `{userId}` |
| Missing HTTP method attributes | `[Route("users/{id}")]` without verb | Add explicit `[HttpGet]`, `[HttpPost]`, etc. |
| Overly broad catch-all routes | `[Route("*")]` or `[Route("")]` | Make routes specific to intended endpoints |

## Verification

Test: Run existing endpoint tests or inspect attribute declarations.
Pass: Every changed endpoint uses one HTTP verb + clear resource path pattern.
