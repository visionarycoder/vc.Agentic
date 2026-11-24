---
name: "cqrs-patterns-dotnet"
description: "Implement command and query separation in .NET with hand-rolled handlers, validation, DI-based dispatch, and VBD-aligned boundaries."
metadata:
  metadata-version: "1.0.0"
  title: "CQRS Patterns for .NET"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# CQRS Patterns for .NET

Agent separates write behavior from read behavior with hand-rolled contracts and VBD-owned boundaries.

Skip this skill for trivial, stable CRUD.

## Workflow

1. Classify requests as commands or queries by side effects and ownership.
2. Place each handler in the boundary that owns the change driver.
3. Add hand-rolled handler interfaces, validators, and DI dispatch registrations.
4. Add validation before command execution and before expensive query work.
5. Return explicit result types or read DTOs.
6. Run targeted build and tests.

## Rules

| Topic | Rule |
|---|---|
| MediatR | Avoid MediatR packages, pipeline behaviors, and notification abstractions. |
| AutoMapper | Use hand-written mapping and projection only. |
| Query purity | Keep queries side-effect free. |
| Command result shape | Return identifiers, version markers, or explicit result types. |
| Transaction scope | Commit once per write use case unless the use case defines a larger boundary. |
| Boundary ownership | Keep handlers in the scope that owns volatility. |

## Verification Checklist

- Search the changed scope for MediatR symbols; expect none.
- Search the changed scope for AutoMapper symbols; expect none.
- Confirm each handler sits in the scope that owns the change driver.
- Run targeted build and tests.
