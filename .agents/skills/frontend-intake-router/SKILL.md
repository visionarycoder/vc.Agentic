---
name: "frontend-intake-router"
description: "Route frontend requests to the minimum correct frontend skill by separating webapp consolidation and WPF concerns before specialized work starts."
metadata:
  metadata-version: "1.0.0"
  title: "Frontend Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Frontend Intake Router

Agent routes frontend work to one primary frontend skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for frontend work and multiple framework families overlap | Agent uses this skill |
| Request involves webapp consolidation or WPF | Agent uses this skill |
| User asks which frontend skill owns the work | Agent uses this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is already narrowed to one frontend framework specialist | Agent uses that specialist |
| Request is backend or domain-first and UI is only a minor follow-on concern | Agent uses the primary non-frontend skill first |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad frontend routing belongs here |
| Framework split | Keep the selected frontend frameworks separated unless the request is explicitly migratory |
| Migration precedence | Migration and cutover work outrank standalone framework optimization when both appear |
| Specialist loading | Choose one frontend primary first, then only concrete follow-on specialists |

## Verification

- [ ] Agent chose one primary frontend skill
- [ ] Agent avoided mixing framework suites without a migration or consolidation scope
- [ ] Agent added secondary frontend skills only for explicit follow-on concerns

## Routing Table

| Intent | Primary skill | Optional secondary |
|---|---|---|
| Web app consolidation or cutover planning | `webapp-consolidation-strategy` | `webapp-cutover-strategy` |
| WPF application setup | `wpf-project-setup` | `wpf-mvvm-implementation` |
