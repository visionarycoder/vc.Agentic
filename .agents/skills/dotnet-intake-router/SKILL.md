---
name: "dotnet-intake-router"
description: "Route generic .NET requests to the minimum correct implementation skill after domain routing is resolved, separating DI, validation, logging, performance, contracts, and resilience concerns."
metadata:
  metadata-version: "1.0.0"
  title: ".NET Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# .NET Intake Router

Agent routes generic .NET work to one primary implementation skill after domain scope is known.

## When to Use

| User prompt | Use |
|---|---|
| Domain scope is already known and the remaining question is a generic .NET implementation concern | Use this skill |
| User asks for DI, validation, logging, performance, DTO, mapping, resilience, or caching guidance outside a narrower suite | Use this skill |
| User asks which generic .NET skill owns the work | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Domain scope is not resolved yet | Use the correct domain or technology router first |
| Request is clearly inside VBD, WebAPI, Azure, EF Core, or another narrower suite | Use that suite instead |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Generic implementation routing belongs here only after domain routing is known |
| Domain precedence | Narrower domain or technology suites win before this router loads |
| Specialist loading | Choose one generic .NET primary first, then only concrete secondaries |
| Scope control | Keep this router free of domain-specific ownership rules |

## Verification

- [ ] Agent used this router only after domain routing was resolved
- [ ] Agent chose one primary .NET skill
- [ ] Agent avoided loading multiple generic .NET peers for one narrow concern

## Routing Table

| Intent | Primary skill | Optional secondary |
|---|---|---|
| Dependency injection or lifetime design | `dotnet-dependency-injection-standards` | none |
| Validation flow or validators | `dotnet-validation-standards` | `dotnet-exception-handling-standards` |
| Structured logging or log design | `dotnet-logging-standards` | `dotnet-telemetry-standards` |
| Performance-sensitive implementation | `dotnet-performance-standards` | `dotnet-analyzing-performance` |
| Generic DTO design outside VBD scope | `dotnet-dto-standards` | `dotnet-mapping-standards` |
| Mapping design | `dotnet-mapping-standards` | `dotnet-dto-standards` |
| Resilience and retries | `dotnet-resilience-standards` | `dotnet-api-client-resilience` |
| Caching design | `dotnet-caching-patterns` | none |
| Channel-based concurrency | `dotnet-channels-patterns` | `dotnet-cancellation-token-standards` |
| Source-generated regex (.NET 7+) | `dotnet-source-generated-regex` | none |
| Compiled regex (legacy) | `dotnet-compiled-regex-patterns` | none |
