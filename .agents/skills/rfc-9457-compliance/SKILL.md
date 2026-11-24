---
name: "rfc-9457-compliance"
description: "Standardize RFC 9457 Problem Details contracts, handlers, and tests across HTTP APIs."
metadata:
  metadata-version: "1.0.0"
  title: "HTTP Problem Details RFC 9457 Compliance"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# HTTP Problem Details RFC 9457 Compliance

Agent uses this skill for HTTP error contracts, centralized handlers, and validation or exception responses.

## When to Use

| Condition | Agent Action |

|---|---|

| Endpoint error payload shape changes | Use this skill |

| Shared exception or validation handler changes | Use this skill |

| Preserved legacy RFC 7807 client contract blocks full migration | Pair with `rfc-7807-compliance` |

| Stream already started | Pair with `rfc-8091-compliance` for post-start failure handling |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is broader than this skill and suite routing is still unclear | Use `webapi-intake-router` first |
| Request belongs to a narrower specialist than this skill | Use that narrower specialist |
| Request is outside this skill's suite or concern | Use the correct suite router or execution skill |

## Contract

- Error responses use media type `application/problem+json` with `type`, `title`, and `status` present.
- Keep formatting in shared middleware, a filter, or a central exception handler, with type URIs mapped centrally per error category.
- `detail` must not contain stack traces, SQL text, or secrets.
- Return validation Problem Details before the first stream byte; later failures need `rfc-8091-compliance` handling.
- Keep stable machine-readable extensions that clients already depend on; record compatibility reasons when RFC 7807 behavior stays.
- Verify by running existing build and API tests for changed error paths.
