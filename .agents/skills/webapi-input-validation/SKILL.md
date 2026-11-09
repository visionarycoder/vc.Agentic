---
name: "webapi-input-validation"
description: "Agent standardizes request validation behavior for DTOs, route/query parameters, model-state failures."
metadata:
  metadata-version: "1.0.0"
  title: "WebAPI Input Validation"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# WebAPI Input Validation

Agent standardizes request validation behavior for DTOs, route/query parameters, model-state failures.

## Use For

Use when:
- Hardening DTO constraints, request guards
- Ensuring predictable 400 responses for invalid input
- Normalizing validation behavior across endpoints

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

## Outputs

Agent produces:
- Validation guard changes
- Predictable invalid-input response behavior
- Test impact summary

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [webapi-input-validation-alternative-1](references/contexts/webapi-input-validation-alternative-1/guide.md)
