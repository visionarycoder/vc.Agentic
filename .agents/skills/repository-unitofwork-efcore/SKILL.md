---
name: "repository-unitofwork-efcore"
description: "Apply repository and unit-of-work patterns over EF Core with hand-rolled abstractions, explicit transaction boundaries, and guidance on repository use versus direct DbContext."
metadata:
  metadata-version: "1.0.0"
  title: "Repository and Unit of Work for EF Core"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Repository and Unit of Work for EF Core

Agent applies focused repository and unit-of-work patterns where aggregate boundaries and transaction ownership need explicit shape.

## When to Use

| Condition | Use |
|---|---|
| Aggregate roots need explicit persistence contracts | Use this skill |
| One write use case coordinates several repositories in one transaction | Use this skill |
| Team needs consistent save, concurrency, and transaction rules across handlers | Use this skill |
| Work asks when repository abstraction adds value over raw `DbContext` | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Small feature reads one table with one short query | Use direct `DbContext` query flow |
| Repository abstraction mirrors every `DbSet` member with no domain meaning | Keep `DbContext` direct access |
| Work asks only for reusable predicates | Use `specification-pattern-dotnet` |
| Work asks only for read-side query optimization | Use `optimizing-ef-core-queries` |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Aggregate map | Yes | Tie repositories to aggregate roots, not tables only. |
| Transaction boundaries | Yes | Record save scope and rollback expectations. |
| Concurrency rules | Yes | Record row version or conflict handling needs. |
| Query-shape needs | Yes | Record where direct `DbContext` reads stay simpler. |
| VBD ownership | No | Align repository location with the boundary that owns persistence policy. |

## Rules

- Keep `DbContext` direct when a repository would only mirror `DbSet` members or a feature reads one table with one short query.
- Centralize `SaveChangesAsync`, transaction start, and concurrency handling in the unit of work; run targeted conflict tests when concurrency tokens exist.
- Do not expose `IQueryable` from repositories.

## Outputs

- Aggregate-focused repository contracts
- EF Core repository implementations
- Unit-of-work contract and save flow
- Transaction-boundary guidance
- Repository-versus-`DbContext` decision record
- Verification steps for persistence behavior

## Reference Files

- [Repository and unit-of-work examples](references/examples.md)
