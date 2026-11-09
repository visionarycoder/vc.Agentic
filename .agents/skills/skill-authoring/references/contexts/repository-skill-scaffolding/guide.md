---
metadata-version: "1.0.0"
title: "Create Skill"
description: "Preserve scoped source guidance for skill-authoring."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Create Skill

Agent scaffolds a new repository skill using STE wording, required frontmatter, token-budget rules, and routed-suite ownership rules.

## When to Use

| User prompt | Use |
|---|---|
| User asks for a new skill | Use this skill |
| User asks for a new `SKILL.md` scaffold | Use this skill |
| User asks for STE-compliant skill structure | Use this skill |
| User asks to add a router, primary execution skill, or specialist skill | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User asks to edit an existing skill | Edit the file directly |
| User asks for broad suite cleanup | Use `skill-suite-optimization` |
| User asks for non-skill markdown | Use the matching documentation skill |
| User asks only where a skill belongs | Use `skill-intake-router` first |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Skill name | Yes | Use lowercase letters, numbers, and hyphens |
| Skill purpose | Yes | State the outcome in one short paragraph |
| Entry conditions | Yes | State when the agent uses the skill |
| Suite role | Yes | Choose `router`, `primary execution`, `secondary specialist`, or `alias/bundle` |
| Owning suite | Yes | Choose the narrowest suite that owns the concern |
| Optional assets | No | List `references`, `scripts`, or `assets` only when needed |

## Required Frontmatter

| Field | Value |
|---|---|
| `name` | Directory name |
| `title` | Human-readable title |
| `description` | One sentence with scope and trigger |
| `doc_type` | `skill` |
| `status` | `active` |
| `last_updated` | Current date |
| `prerequisites` | Include `ste-agent-writing-standard` and `terminology-dictionary` |
| `related_skills` | Include the owning router when the skill is not itself the router |

## Routed-Suite Rules

| Topic | Rule |
|---|---|
| Suite ownership | Agent assigns one owning suite before writing the skill. |
| Router role | Router skills classify broad intake and choose one primary execution skill. |
| Primary execution role | Primary execution skills own the main workflow for one concern inside a suite. |
| Secondary specialist role | Secondary specialists load only when a concrete missing concern remains after the primary skill is chosen. |
| Alias or bundle role | Alias or bundle skills exist only when they reduce ambiguity, preserve compatibility, or lower token cost. |
| Generic `.NET` scope | Generic `.NET` skills load only after domain routing resolves scope. |
| Conflict prevention | Agent avoids creating a new broad peer that competes with an existing router or primary skill. |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent verifies `skill-name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`. | Read the planned directory name. | Name matches the pattern. |
| 2 | Agent assigns the suite role and owning suite before writing content. | Read the planned routing notes. | Exactly one suite role and one owning suite are chosen. |
| 3 | Agent checks whether a router, primary skill, or specialist already owns the concern. | Search related skills in the owning suite. | New skill does not duplicate an existing broad owner. |
| 4 | Agent writes `.github/skills/<skill-name>/SKILL.md`. | Read the target directory. | Directory contains `SKILL.md`. |
| 5 | Agent writes required frontmatter. | Run `rg "^(name|title|description|doc_type|status|last_updated):" .github\skills\<skill-name>\SKILL.md`. | Six required fields exist. |
| 6 | Agent writes sections for use, inputs, routing or workflow, verification, and pitfalls. | Run `rg "^## (When to Use|When Not to Use|Required Inputs|Routed-Suite Rules|Workflow|Verification|Common Pitfalls)$" .github\skills\<skill-name>\SKILL.md`. | All required headings exist. |
| 7 | Agent adds router alignment in `related_skills` when the skill is not itself a router. | Read the frontmatter. | Owning router is present or the skill itself is the router. |
| 8 | Agent applies STE wording from `ste-agent-writing-standard`. | Run the repository STE violation grep on the new file. | Zero modal or prohibited phrase matches exist. |
| 9 | Agent moves verbose examples to `references/` when the main file exceeds the token budget. | Read `estimated_tokens` in frontmatter. | `estimated_tokens < 2000`. |
| 10 | Agent updates `.github/CODEOWNERS` when the repository uses skill ownership entries. | Run `rg -n "<skill-name>" .github\CODEOWNERS`. | Match exists or repository has no skill entry pattern. |
| 11 | Agent registers the skill in repository inventories. | Search `.github/copilot-instructions.md`, `.github/skills-index.md`, and `.github/skills-index.txt`. | All required inventories contain the skill. |
| 12 | Agent runs frontmatter verification. | Run `npm run frontmatter:validate`. | Zero validation errors. |

## Structure Rules

| Topic | Rule |
|---|---|
| Main file size | Keep `estimated_tokens < 2000` |
| Decision logic | Use tables, not prose lists |
| Examples | Write large examples under `references/` |
| Terminology | Use approved terms from `terminology-dictionary` |
| Suite alignment | Keep `related_skills` aligned with the owning router and nearest primary skill |
| Broad intake | Create broad intake logic only in routers or approved mixed-entry bundles |
| Ownership text | State whether the skill is a router, primary execution skill, secondary specialist, or alias |

## Verification

- [ ] Agent wrote the skill under `.github/skills/<skill-name>/`.
- [ ] Agent assigned one suite role and one owning suite.
- [ ] Agent wrote required frontmatter fields.
- [ ] Agent added STE prerequisites.
- [ ] Agent aligned `related_skills` with the owning router.
- [ ] Agent used tables for workflow and decision logic.
- [ ] Agent kept the main file under the token budget.
- [ ] Agent registered the skill in repository inventories.
- [ ] Agent ran frontmatter verification.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Name uses uppercase or spaces | Agent rewrites the name with lowercase hyphenated text. |
| Description hides the trigger | Agent states what the skill does and when the agent uses it. |
| New skill competes with an existing router | Agent narrows the scope or converts the new skill into a secondary specialist. |
| New skill duplicates a primary execution skill | Agent merge-refactors the concern into the existing primary skill. |
| Generic `.NET` skill absorbs domain rules | Agent moves domain rules into the owning domain suite and keeps the `.NET` skill generic. |
| Main file grows too large | Agent moves examples to `references/`. |
| Workflow uses prose only | Agent rewrites the workflow as a table. |
| STE rules are missing | Agent adds subjects, tests, and pass criteria. |
