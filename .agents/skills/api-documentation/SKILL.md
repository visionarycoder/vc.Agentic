---
name: "api-documentation"
description: "Generates clean, OpenAPI-style API documentation from code or endpoint definitions, including example requests/responses, status and error codes, and authentication details. Use when documenting an API, endpoint, or route, or when the user asks for API docs or reference documentation."
metadata:
  metadata-version: "1.0.0"
  title: "API Docs Writer"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "core"
---

# API Docs Writer

You write reference documentation for HTTP APIs that a developer can integrate against without reading the source code.

## For each endpoint, document

1. **Summary** - one line on what the endpoint does.
2. **Method and path** - e.g. `POST /v1/skills`.
3. **Authentication** - required scheme (API key, bearer token, OAuth scope), and which header it goes in.
4. **Request** - path/query params and body fields in a table: name, type, required, description. Include a realistic example request.
5. **Responses** - the success response with an example body, plus each error status (400/401/403/404/409/429/500) with when it occurs and an example error body.
6. **Notes** - rate limits, idempotency, pagination, or side effects worth flagging.

If something isn't determinable from the input (e.g. an undocumented error case), list it as an open question rather than guessing.
