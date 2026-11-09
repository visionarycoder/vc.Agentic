---
metadata-version: "1.0.0"
title: "WebAPI Input Validation"
description: "Preserve scoped source guidance for webapi-input-validation."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# WebAPI Input Validation

Agent standardizes request validation behavior for DTOs, route/query parameters, model-state failures.

## When to Use

| User prompt | Use |
|---|---|
| User asks to harden DTO constraints or request guards | Use this skill |
| User asks for predictable invalid-input behavior | Use this skill |
| User asks to normalize validation behavior across endpoints | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is broader multi-concern WebAPI remediation | Use `webapi-fixes-bundle` via `webapi-intake-router` |
| Request is primarily auth or authorization hardening | Use `webapi-authz-hardening` |
| Request is primarily route shaping or compatibility migration | Use the matching WebAPI specialist |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | This skill owns input-validation concerns after `webapi-intake-router` resolves scope. |
| Scope control | Keep the skill focused on request validation and invalid-input behavior. |
| Error contract | Validation failures align with the repository WebAPI error-contract rules. |
| Specialist loading | Add other WebAPI specialists only when the request clearly expands beyond validation. |

## Workflow

Agent performs:

1. Agent identifies DTO, route, query inputs per endpoint
2. Agent applies explicit validation rules, guard clauses
3. Agent aligns invalid-input responses to consistent error contracts
Test: POST invalid payload
Pass: Status = 400. Response body = RFC 9457 Problem Details.
4. Agent adds or updates targeted tests for invalid, boundary payloads
Test: Run `dotnet test [ValidationTests].csproj`
Pass: All validation tests pass.

## Verification

- [ ] Agent used this skill only for input-validation concerns.
- [ ] Agent aligned invalid-input responses to the current WebAPI error-contract rules.
- [ ] Agent kept broader WebAPI concerns routed to the correct current-state skill.

## Outputs

Agent produces:
- Validation guard changes
- Predictable invalid-input response behavior
- Test impact summary
