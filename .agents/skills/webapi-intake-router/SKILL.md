---
name: "webapi-intake-router"
description: "Route Web API requests to the minimum correct WebAPI skill surface by separating new implementation, remediation, authorization, validation, route design, and error-contract concerns."
metadata:
  metadata-version: "1.0.0"
  title: "WebAPI Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# WebAPI Intake Router

Agent routes Web API work to one primary execution skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Web API implementation or remediation and several WebAPI skills apply | Use this skill |
| The request mixes routes, validation, auth, and error-contract concerns | Use this skill |
| User asks which WebAPI workflow owns the work | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User already narrowed the request to one specific WebAPI specialist | Use that specialist |
| Request is not primarily about API behavior or API surface | Use the correct non-WebAPI suite |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad WebAPI routing belongs here |
| New implementation | Use `dotnet-webapi` for new API implementation |
| Mixed remediation | Use `webapi-fixes-bundle` for multi-concern cleanup |
| Specialist loading | Use one narrow WebAPI skill first when the dominant concern is explicit |

## Verification

- [ ] Agent chose one primary WebAPI skill
- [ ] Agent loaded bundle only for multi-concern remediation
- [ ] Agent avoided stacking narrow WebAPI skills without explicit need

## Routing Table

| Intent | Primary skill | Optional secondary |
|---|---|---|
| New endpoint or API implementation | `dotnet-webapi` | `webapi-input-validation` |
| Multi-concern endpoint cleanup | `webapi-fixes-bundle` | none |
| Route normalization only | `webapi-rest-route-standardization` | none |
| Validation behavior only | `webapi-input-validation` | none |
| Authorization hardening only | `webapi-authz-hardening` | none |
| Error contract shaping only | `webapi-error-contract-hardening` | none |
| Legacy endpoint migration | `webapi-compatibility-migration` | `webapi-error-contract-hardening` |
