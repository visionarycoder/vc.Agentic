---
name: "repo-reconciliation"
description: "Audit and reconcile repository guidance across .agents, .github, docs, and workflows when architecture, project layout, release packaging, or canonical ownership changes. Use when project consolidation creates doc drift, workflows reference removed projects, or skills/prompts no longer match the repo's true structure."
metadata:
  metadata-version: "1.0.0"
  title: "Repository Reconciliation"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "core"
---

# Repository Reconciliation

Use this skill to keep repository guidance internally consistent after structural change.

## Use This Skill For

- project consolidation follow-up
- stale workflow package targets
- roadmap completion vs repo reality drift
- prompt, instruction, or skill references to removed projects
- canonical ownership changes such as moving functionality into `vc.ServiceModel`

## Audit Surface

Check these surfaces together, not one at a time:

1. `docs/`
2. `.github/`
3. `.agents/skills/`
4. solution and project file references
5. release and packaging workflow targets

## Workflow

1. Identify the canonical project set from the current `src/` tree.
2. Compare it with roadmap claims, recommendation matrices, README package guidance, and workflow packaging targets.
3. Prefer one canonical decision statement for architectural ownership and reuse that wording across docs.
4. Group changes into:
   - architecture ownership alignment
   - agent guidance alignment
   - release workflow alignment
   - roadmap lifecycle/status alignment
5. Validate with the narrowest relevant check:
   - `dotnet build main`
   - `dotnet test main`
   - release packaging commands when release docs change

## Guardrails

- Do not preserve contradictory historical wording without clearly labeling it as historical.
- Do not keep removed projects in workflow/package lists.
- Do not let prompts or skills refer to old project homes when a canonical home exists.
- Keep milestone docs and evergreen reference docs distinct.

## Deliverables

- a findings list ordered by severity
- a reconciliation plan grouped into workstreams
- any required new or updated skills/instructions
- explicit decision points when repo intent is ambiguous
