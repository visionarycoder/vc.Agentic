---
name: "documentation-intake-router"
description: "Route documentation requests to the minimum documentation workflow by separating general remediation, link repair, front matter, placement, governance, and agent-asset concerns."
metadata:
  metadata-version: "1.0.0"
  title: "Documentation Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Documentation Intake Router

Agent routes markdown and instruction work to one primary documentation skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for markdown cleanup, front matter, links, or documentation governance | Use this skill |
| The correct documentation execution skill is not yet narrowed | Use this skill |
| The request includes instruction, prompt, or skill governance concerns | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Documentation scope is already narrowed to one known execution skill | Use that execution skill |
| Request is code-focused and docs are only a small follow-on concern | Use the primary code/domain skill first |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad documentation routing belongs here |
| Mixed remediation | Use bundle or broad remediation only when one narrow skill is not enough |
| Governance precedence | Agent-asset governance outranks generic documentation cleanup when both apply |
| Skill count | Load one documentation primary first, then only necessary specialists |

## Verification

- [ ] Agent chose one primary documentation skill
- [ ] Agent used bundle only for mixed or unclear documentation remediation
- [ ] Agent avoided loading multiple narrow documentation skills unless change scope required them

## Routing Table

| Intent | Primary skill | Optional secondary |
|---|---|---|
| Broad documentation cleanup | `documentation-fixes` | none |
| Unsure / mixed documentation remediation | `documentation-fixes-bundle` | none |
| Link breakage only | `documentation-link-repair` | none |
| Front matter only | `documentation-frontmatter` | none |
| File placement or move decision | `documentation-file-placement` | `documentation-link-repair` |
| Agent instructions, prompts, skills governance | `agent-instruction-governance` | `documentation-governance` |
