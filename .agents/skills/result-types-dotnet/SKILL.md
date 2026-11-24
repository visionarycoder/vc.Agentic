---
name: "result-types-dotnet"
description: "Model success, failure, absence, and decision unions in .NET with hand-rolled result types and railway-oriented flow instead of exception-driven control."
metadata:
  metadata-version: "1.0.0"
  title: "Result Types for .NET"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Result Types for .NET

Model expected outcomes with explicit result types, option types, and union shapes instead of exception-driven branching.

## When to Use

| Prompt or Code Shape | Use |
|---|---|
| Business validation failures are common and expected | Use this skill |
| Command or query flow needs explicit success and failure states | Use this skill |
| Caller logic needs absence handling without null-driven ambiguity | Use this skill |
| Team asks for railway-oriented composition without third-party libraries | Use this skill |

## When Not to Use

| Prompt or Code Shape | Route |
|---|---|
| Runtime fault is exceptional and aborts the operation | Keep exception flow for the fault path |
| API contract already standardizes RFC problem details at the edge only | Map internal results to that edge contract |
| Work item asks only for domain event design | Use `domain-events-dotnet` |
| Work item asks only for command-query split | Use `cqrs-patterns-dotnet` |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Outcome categories | Yes | Agent distinguishes success, validation failure, not found, conflict, and fault. |
| Consumer expectations | Yes | Record what each caller needs to branch on. |
| Composition points | Yes | Record where flows chain through map and bind steps. |
| Nullability rules | Yes | Agent avoids mixed null and result signaling. |
| Boundary mapping | No | Record HTTP, message, or UI mapping at the outer edge. |

## Rules

- Expected, caller-correctable outcomes are results; faults and broken assumptions stay exceptions.
- Hand-roll `Result`, `Result<T>`, `Option<T>`, and unions with `Map`, `Bind` (`BindAsync`), and `Match`; avoid FluentResults, OneOf, LanguageExt, and Optional.
- Errors carry a stable domain error code (for example `timesheet.not_found`); message text is secondary.
- Name union cases in domain vocabulary, not HTTP statuses; map to HTTP or UI at the outer edge.
- Avoid `Result<Option<T>>` unless absence and failure must both be distinguished.
- Verify with targeted `dotnet build` and tests.

## Outputs

- Shared result and option types
- Domain error vocabulary
- Boundary mapping guidance
- Verification steps for outcome flow
