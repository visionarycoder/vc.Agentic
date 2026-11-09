---
name: "documentation-fixes"
description: "Route documentation remediation through a single STE-compliant workflow."
metadata:
  metadata-version: "1.0.0"
  title: "Documentation Fixes Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Documentation Fixes Skill

Agent runs documentation remediation from one entry point.

Agent acts as the primary execution skill after `documentation-intake-router` selects broad documentation remediation.

## When to Use

| User prompt | Use |
|---|---|
| User asks for broad documentation cleanup or remediation | Use this skill |
| Multiple documentation issues are corrected together | Use this skill |
| Intake identified documentation remediation as the primary concern | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User only needs front matter normalization | Use `documentation-frontmatter` |
| User only needs link repair | Use `documentation-link-repair` |
| User only needs file placement guidance | Use `documentation-file-placement` |
| User is authoring a new documentation workflow rather than fixing docs | Use the matching authoring or governance skill |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad documentation remediation belongs here after `documentation-intake-router` |
| Specialist loading | Load only the specific support skill needed for the observed issue |
| Placement | Agent-governance or file-placement skills load only when the issue includes placement or asset location |
| Scope control | Keep edits limited to the docs directly involved in the remediation request |

## Workflow

| Step | Agent Action | Output |

|---|---|---|

| 1. Classify | Agent maps the request to one or more coverage areas. | Scope list |

| 2. Inventory | Agent lists affected markdown files and source-of-truth files. | File inventory |

| 3. Select | Agent loads only the supporting skills that match the changed markdown scope. | Focused skill set |

| 4. Remediate | Agent applies minimal edits, moves, or consolidations. | Updated files |

| 5. Validate | Agent runs front matter, link, and placement checks. | Validation results |

| 6. Report | Agent returns files changed and follow-up items. | Completion summary |

## Verification

| Check | Test | Pass Criteria |

|---|---|---|

| Front matter | Run `npm run frontmatter:validate` when repository tooling exists. | Command returns zero validation errors. |

| Local links | Check changed markdown links and anchors. | Zero unresolved local links remain in changed files. |

| File placement | Compare each changed file to the canonical location map. | Every changed file matches its canonical location. |

| Change scope | Review changed files against request scope. | No unrelated documentation files change. |

## Coverage Map

| Area | Primary Skill | Result |

|---|---|---|

| Documentation governance | `documentation-governance` | Placement, links, front matter stay consistent |

| Documentation maintenance | `documentation-maintenance` | Code changes ship with matching docs |

| Documentation refactor | `documentation-refactor-review` | Duplicate or stale guidance is reduced |

| Documentation tone | `documentation-style-collaboration` | Wording stays clear and collaborative |

| Agent asset placement | `agent-instruction-governance` | Instruction assets stay in approved locations |

## Decision Rules

Agent keeps one canonical document per topic.

Agent moves discoverable Copilot assets only inside `.github/**` surfaces.

Agent places long-form guidance in `docs/instructions/**` or another canonical `docs/**` area.

Agent updates related indexes and links after every move or rename.

## Output Contract

Agent reports coverage areas executed.

Agent reports files updated, moved, archived, or deleted.

Agent reports validation results.

Agent reports deferred follow-up items.

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [documentation-fixes-alternative-1](references/contexts/documentation-fixes-alternative-1/guide.md)
