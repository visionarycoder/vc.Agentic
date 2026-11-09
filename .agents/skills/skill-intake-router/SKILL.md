---
name: "skill-intake-router"
description: "Route repository requests to the minimum correct domain router and execution skill set to reduce token burn, avoid conflicting instructions, and keep AI activation deterministic."
metadata:
  metadata-version: "1.0.0"
  title: "Skill Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Skill Intake Router

Agent uses this skill first when request scope is unclear or when multiple skill families overlap.

## When to Use

| User prompt | Use |
|---|---|
| Scope spans multiple suites or the correct suite is unclear | Agent uses this skill |
| Request mixes domain, technology, and remediation concerns | Agent uses this skill |
| User asks for the right skill or workflow to load | Agent uses this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is already clearly inside one known suite | Agent uses the suite router directly |
| Request is already narrowed to one concrete execution skill | Agent uses that execution skill directly |

## Routing Rules

| Topic | Rule |
|---|---|
| Ownership | Global intake belongs here, not in execution skills |
| Domain precedence | Agent uses the domain suite when domain and generic `.NET` scopes overlap |
| Technology precedence | Agent uses the technology suite after domain scope is known unless the user asks for technology-first work |
| Skill count | Load one router, one primary execution skill, and only concrete secondaries |
| Alias use | Alias or bundle skills stay compatibility-focused and do not compete as independent global routers |

## Verification

- [ ] Agent chose one router before loading detailed skills
- [ ] Agent chose one primary execution skill
- [ ] Agent avoided loading multiple same-phase peer skills without cause
- [ ] Agent used secondary skills only for explicit missing concerns

## Goal

Agent chooses the smallest correct routing surface before loading execution skills.

## Global Routing Matrix

| Request shape | Domain router | Primary concern |
|---|---|---|
| Decomposition, Manager, Engine, Access, component boundaries | `vbd-intake-router` | VBD architecture and authoring |
| Controllers, endpoints, authorization, request/response API behavior | `webapi-intake-router` | Web API design and remediation |
| Markdown, instructions, prompts, skills, links, front matter | `documentation-intake-router` | Documentation governance and remediation |
| Test quality, coverage, assertions, gaps, smells | `testing-intake-router` | Test analysis and remediation |
| Broad hardening, CWE families, multi-theme vulnerability cleanup | `security-intake-router` | Security routing and remediation |
| Project files, SDK-style migration, props/targets, build graph, binlogs | `msbuild-intake-router` | Build and MSBuild routing |
| Azure Functions, Key Vault, App Configuration, Entra ID, Storage | `azure-intake-router` | Azure technology routing |
| EF Core DbContext, migrations, EF testing, query tuning | `efcore-intake-router` | EF Core routing |
| Angular, Vue, web app, or WPF work | `frontend-intake-router` | Frontend routing |
| Roslyn analyzers, code fixes, source generators, Ifx authoring | `roslyn-intake-router` | Roslyn and Ifx routing |
| Fabric, KQL, Lakehouse, pipelines, semantic models, data quality | `data-intake-router` | Data and Fabric routing |
| Narrow .NET implementation detail after domain is known | `dotnet-intake-router` | Generic .NET specialization |

## Load Rules

1. Agent loads one router first.
2. Agent loads one primary execution skill after routing.
3. Agent loads a secondary execution skill only for a concrete missing concern.
4. Agent keeps routing ownership in routers, not in deep execution skills.
5. Agent uses domain-specific skills over generic technology skills inside domain scope.

## Conflict Rules

| Risk | Resolution |
|---|---|
| Multiple skills fit the request | Agent routes by dominant intent and lifecycle phase |
| Generic skill conflicts with domain rule | Agent uses the domain execution skill inside domain scope |
| Two peer execution skills cover the same phase | Agent loads one primary skill and references the other only when the primary lacks a required rule |
