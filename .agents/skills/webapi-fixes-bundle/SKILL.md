---
name: "webapi-fixes-bundle"
description: "Bundled remediation workflow for Web API route design, input verification, authorization hardening, error contracts, and compatibility migration."
metadata:
  metadata-version: "1.0.0"
  title: "WebAPI Fixes Bundle"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# WebAPI Fixes Bundle

Agent uses this bundle for one-prompt Web API hardening and modernization. Agent reads only the matching reference playbooks.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Webapi Fixes Bundle work | Use this skill |
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
| 1. Classify scope | Agent identifies controllers, endpoints, and tracks in scope. | Agent lists endpoint-to-track mapping. | Every changed endpoint maps to at least one track. |
| 2. Read playbooks | Agent reads only the playbooks for mapped tracks. | Agent records one playbook path per track. | Every mapped track has one recorded playbook path. |
| 3. Write minimal fixes | Agent writes the smallest contract-safe fix per track. | Agent reviews diff for unrelated framework or endpoint churn. | Diff stays inside mapped tracks. |
| 4. Verify build and tests | Agent runs existing build and API tests for touched projects. | Run existing build and test commands in scope. | Zero build errors and zero failing tests in scope. |
| 5. Report contract impact | Agent lists changed endpoints and compatibility effects. | Agent records changed endpoint summary. | Every changed endpoint appears once in the summary. |

## Bundle Coverage Matrix

| Track | Specialized Skill Source | Bundle Reference | Agent Uses When |
|---|---|---|
| REST route standardization | `.github/skills/webapi-rest-route-standardization/SKILL.md` | `references/rest-route-standardization.md` | Route cleanup or normalization is in scope |
| Input verification standardization | `.github/skills/webapi-input-validation/SKILL.md` | `references/input-validation-hardening.md` | Request verification behavior is in scope |
| Authorization hardening | `.github/skills/webapi-authz-hardening/SKILL.md` | `references/authz-hardening.md` | Authorization posture is in scope |
| Error contract hardening | `.github/skills/webapi-error-contract-hardening/SKILL.md` | `references/error-contract-hardening.md` | Error payload or status semantics are in scope |
| Compatibility migration | `.github/skills/webapi-compatibility-migration/SKILL.md` | `references/compatibility-migration.md` | Legacy endpoint migration or deprecation is in scope |

## Activation

| Prompt Scope | Use This Bundle | Route Detail |
|---|---|---|
| Clean up or normalize controller routes | Yes | Agent uses route standardization track |
| Improve request verification behavior | Yes | Agent uses input verification track |
| Tighten endpoint authorization posture | Yes | Agent uses authorization track |
| Standardize error payloads or status semantics | Yes | Agent uses error contract track |
| Migrate legacy endpoints with compatibility shims | Yes | Agent uses compatibility track |
| New endpoint implementation only | No | Agent routes to scope-specific Web API skill |

## Track Verification Matrix

| Track | Agent Verifies | Test | Pass |
|---|---|---|---|
| Routes | Route templates and verbs match the intended contract. | Run existing endpoint tests or inspect route attributes in changed scope. | Each changed endpoint exposes one intentional route pattern. |
| Input verification | Caller defects return deterministic 4xx responses. | Run existing API tests with invalid input in changed scope. | Invalid input returns an intentional 4xx response. |
| Authorization | Anonymous and unauthorized calls return intended auth results. | Run existing authorization tests in changed scope. | Protected endpoints return intended `401` or `403` results. |
| Error contracts | Error responses use one contract shape. | Run existing API tests or inspect serialized error response. | Changed error responses use the intended status code and one Problem Details contract shape. |
| Compatibility | Preserved legacy contracts remain callable until retirement. | Run existing compatibility tests in changed scope. | Legacy route or contract passes until the retirement step is recorded. |

## Non-Goals

| Out-of-Scope Prompt | Agent Route |
|---|---|
| Generic C# style refactor | Route to code-quality skill |
| New endpoint implementation planning | Route to scope-specific Web API skill |
| Broad vulnerability sweep | Route to dedicated CWE or security skill |
