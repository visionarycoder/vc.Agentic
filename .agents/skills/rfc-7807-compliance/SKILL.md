---
name: "rfc-7807-compliance"
description: "Preserve legacy RFC 7807 Problem Details contracts while defaulting all new work to RFC 9457."
metadata:
  metadata-version: "1.0.0"
  title: "RFC 7807 Problem Details (Legacy/Obsolete)"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# RFC 7807 Problem Details (Legacy/Obsolete)

Agent uses this skill only for preserved legacy contracts. Agent uses RFC 9457 for new or modernized endpoints.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Rfc 7807 Compliance work | Use this skill |
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

| 1. Classify scope | Agent identifies preserved legacy endpoints and shared handlers. | Agent lists legacy endpoints or states none exist. | Every changed legacy endpoint appears once. |

| 2. Preserve contract | Agent keeps canonical fields and media type stable for legacy clients. | Inspect changed error response shape. | Legacy payload shape stays stable. |

| 3. Block new legacy spread | Agent avoids new RFC 7807-only behavior outside preserved scope. | Review changed files for new legacy-only helpers. | Zero new legacy-only helpers appear outside preserved scope. |

| 4. Verify migration safety | Agent adds or updates tests for preserved clients and forward migration paths. | Run existing API tests in scope. | Zero failing tests in scope. |

## Activation

| Condition | Agent Action |

|---|---|

| Existing client contract depends on RFC 7807 behavior | Use this skill |

| Endpoint migration moves toward current Problem Details semantics | Pair with `rfc-9457-compliance` |

| New endpoint or new shared error handler | Do not use this skill |

## Legacy Rules

| Rule | Agent Verifies | Fix |

|---|---|---|

| LEGACY-7807-001 | Legacy scope is documented | Record client or contract reason |

| LEGACY-7807-002 | Canonical members stay stable | Preserve `type`, `title`, `status`, `detail`, `instance` |

| LEGACY-7807-003 | No new RFC 7807-only extension appears | Move new work to RFC 9457-compatible fields |

| LEGACY-7807-004 | Payload stays sanitized | Remove stack traces, SQL text, and secrets |

| LEGACY-7807-005 | Migration path stays visible | Record endpoint or handler target for RFC 9457 |

## Verification Matrix

| Test | Run | Pass |

|---|---|---|

| Build verification | Run existing build command for the touched API project. | Zero build errors. |

| Legacy contract verification | Run existing legacy API or contract tests in scope. | Legacy clients still receive the preserved Problem Details shape. |

| Security verification | Inspect changed payloads or tests for exception detail leaks. | Zero sensitive details appear in client payloads. |

## Guardrails

- Agent records a compatibility reason before using RFC 7807 guidance.

- Agent keeps new endpoint work on RFC 9457.

- Agent centralizes legacy behavior in one handler path when practical.
