---
name: "rfc-fixes-bundle"
description: "Routes RFC-focused fixes for Problem Details, JSON, JSON sequence, and JWT security by using RFC 9457, RFC 7807, RFC 8259, RFC 8091, and RFC 8725 references."
metadata:
  metadata-version: "1.0.0"
  title: "RFC Fixes Bundle"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# RFC Fixes Bundle

Agent uses this bundle for RFC-focused contract, payload, streaming, and JWT fixes. Agent reads only matching reference files.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Rfc Fixes Bundle work | Use this skill |
| Request falls inside the webapi suite and needs this specific surface | Use this skill |
| The routed catalog needs a single current-state owner for this concern | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is broader than this skill and suite routing is still unclear | Use `webapi-intake-router` first |
| Request belongs to a narrower specialist than this skill | Use that narrower specialist |
| Request is outside this skill's suite or concern | Use the correct suite router or execution skill |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Classify scope | Agent maps each changed file to Problem Details, JSON, JSON sequence, or JWT. | Agent lists one or more tracks for each changed file. | Every changed file maps to at least one track. |
| 2. Read references | Agent reads only the reference files for mapped tracks. | Agent records one reference path per mapped track. | Every mapped track has one recorded reference path. |
| 3. Write fixes | Agent writes the smallest RFC-compliant fix per track. | Agent reviews diff for conflicting contract patterns. | Changed scope contains one contract pattern per track. |
| 4. Verify build and tests | Agent runs existing build and test commands for touched projects. | Run the existing build and test commands in scope. | Zero build errors and zero failing tests in scope. |

## Activation

| Prompt Scope | Use This Bundle | Route Detail |
|---|---|---|
| Problem Details contract fixes | Yes | Agent uses RFC 9457 by default |
| Legacy Problem Details compatibility | Yes | Agent uses RFC 7807 only for preserved client contracts |
| JSON syntax or serializer contract fixes | Yes | Agent uses RFC 8259 |
| JSON text sequence media type or framing fixes | Yes | Agent uses RFC 8091 |
| JWT issuance or verification fixes | Yes | Agent uses RFC 8725 |
| Non-RFC API implementation work | No | Agent routes to scope-specific skill |

## Coverage Matrix

| Track | Primary Reference | Secondary Reference | Agent Uses When |
|---|---|---|---|
| Problem Details | `references/rfc-9457.md` | `references/rfc-7807.md` | Error payload contract changes are in scope |
| JSON | `references/rfc-8259.md` | - | External JSON payload syntax or interoperability is in scope |
| JSON sequence | `references/rfc-8091.md` | `references/rfc-8259.md` | Streaming JSON text sequences are in scope |
| JWT | `references/rfc-8725.md` | - | Token issuance or token verification is in scope |

## Decision Order

| Decision | Agent Action |
|---|---|
| Problem Details on new or updated endpoints | Agent uses RFC 9457 |
| Problem Details on preserved legacy contracts | Agent uses RFC 7807 and records compatibility reason |
| JSON sequence framing in scope | Agent uses RFC 8091 and RFC 8259 |
| JWT logic in scope | Agent uses RFC 8725 |
| Two references conflict | Agent applies the row above this row first |

## Track Verification Matrix

| Track | Agent Verifies | Test | Pass |
|---|---|---|---|
| Problem Details | Error responses use Problem Details fields and media type. | Run existing API tests or inspect serialized response in changed scope. | Error responses use `application/problem+json` and include `type`, `title`, and `status`. |
| JSON | External JSON remains standards-compliant. | Run parser or serializer tests in changed scope. | Changed payloads parse without comments, trailing commas, or duplicate framing bytes. |
| JSON sequence | Streaming responses use correct framing and media type. | Run existing streaming tests in changed scope. | Response media type is `application/json-seq` and each frame is one complete JSON text. |
| JWT | Token logic keeps explicit verification rules. | Run existing authentication tests in changed scope. | Algorithm, issuer, audience, and lifetime verification remain explicit. |

## Guardrails

| Do Not Use | Agent Uses |
|---|---|
| RFC 7807 as default for new endpoints | RFC 9457 |
| Ad hoc error payloads beside Problem Details | One Problem Details contract |
| Non-standard JSON constructs in external contracts | RFC 8259 JSON |
| Relaxed JWT verification rules | Explicit algorithm, issuer, audience, and lifetime verification |

## Outputs

Agent generates:
- RFC-aligned code and documentation in changed scope
- One recorded reference path per affected RFC track
- Build and test evidence for touched projects

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [rfc-fixes-bundle-alternative-1](references/contexts/rfc-fixes-bundle-alternative-1/guide.md)
