---
name: "efcore-intake-router"
description: "Route EF Core requests to the minimum correct EF Core skill by separating DbContext design, migrations, testing, and query optimization concerns."
metadata:
  metadata-version: "1.0.0"
  title: "EF Core Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# EF Core Intake Router

Agent routes EF Core work to one primary EF Core skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for EF Core design, migrations, testing, or query tuning and the exact concern is unclear | Use this skill |
| Request maps to multiple EF Core skills | Use this skill |
| User asks which EF Core skill owns the work | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is already narrowed to one EF Core specialist | Use that specialist |
| Request is broader architectural or VBD authoring work with EF only as a detail | Use the domain skill first |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad EF Core routing belongs here |
| Schema change precedence | Migration work routes to `efcore-migrations` first |
| Design precedence | `DbContext` structure routes to `efcore-dbcontext-design` first |
| Performance split | Query tuning stays separate from model and migration work unless the request explicitly combines them |

## Verification

- [ ] Agent chose one primary EF Core skill
- [ ] Agent avoided stacking EF Core peers for one narrow concern
- [ ] Agent used a secondary EF Core skill only when the primary workflow required it

## Routing Table

| Intent | Primary skill | Optional secondary |
|---|---|---|
| `DbContext` design or model structure | `efcore-dbcontext-design` | `optimizing-ef-core-queries` |
| Migration authoring or migration review | `efcore-migrations` | none |
| EF-specific test design | `efcore-testing-patterns` | `efcore-dbcontext-design` |
| Query performance tuning only | `optimizing-ef-core-queries` | none |
