---
name: "framework-migration-guidelines"
description: "Collection of framework-to-framework migration rules and transformation patterns (e.g., Struts→Spring MVC, JSP→Thymeleaf, EJB→Spring Boot). Triggers: \"check migration guidelines\", \"look up transformation rules\", \"find Struts-to-Spring patterns\", \"apply migration conventions\", \"conversion rules for X→Y\". Also consumed automatically by breaking-down-tasks and implementing-code during migration workflows. NOT for: direct execution — other skills scan this directory."
metadata:
  metadata-version: "1.0.0"
  title: "Framework Migration Guidelines"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Framework Migration Guidelines

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

Guidelines are curated, domain-specific knowledge bases providing:
- **Migration patterns**: Technology-to-technology recipes
- **Transformation rules**: Concrete mappings and conversion templates
- **Checklists**: Step-by-step validation criteria

## Directory Structure

```
.agents/skills/framework-migration-guidelines/
├── SKILL.md                      # This file - lookup mechanism
├── struts-to-spring/           # Struts 2 → Spring Boot 3.x
│   └── CONTEXT.md
└── {domain}/                   # Future guideline domains
    └── CONTEXT.md
```

## Lookup Mechanism

When other skills need guideline lookup:

1. **Context Analysis**: Extract technology keywords from spec/plan/code.
2. **Guideline Discovery**: Search `.agents/skills/framework-migration-guidelines/` subdirectories for matching patterns.
3. **Application**: Load matching CONTEXT.md, extract applicable rules for current phase.

## Integration Points

| Workflow Step | Guideline Application |
|---------------|----------------------|
| Specification | Domain constraints, scope boundaries |
| Planning | Technology decisions, architecture patterns |
| Tasks | Transformation tasks, file-by-file changes |
| Implementation | Code transformation rules, test patterns |
| Completeness | Validation checklists, coverage criteria |

## Creating New Guidelines

1. Create directory: `.agents/skills/framework-migration-guidelines/{domain}/`
2. Create `CONTEXT.md` with:
   - Metadata header (name, description, triggers)
   - Rules organized by migration step
   - Concrete transformation examples (before/after)
   - Validation checklist

## Documenting Applied Guidelines

When guidelines are applied, document in the relevant artifact:

```markdown
## Applied Guidelines
- **Guideline**: struts-to-spring
- **Rules Used**: convert-action-to-controller, convert-validation
- **Reference**: .agents/skills/framework-migration-guidelines/struts-to-spring/CONTEXT.md
```

## Project and host prerequisites

References labeled as consuming-project or host files are not bundled assets. Resolve them in the assigned project or connected host and verify them before a dependent step. If required context is absent, report it and limit the work to a supported draft. Optional external skills are not installed by this library; use an available authorized capability or identify the unmet prerequisite. Do not recreate owner-deleted skills.
