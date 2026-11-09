---
metadata-version: "1.0.0"
title: "Documentation Fixes Skill"
description: "Preserve scoped source guidance for documentation-fixes."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Documentation Fixes Skill

Agent runs documentation remediation from one entry point.

## Coverage Map

| Area | Primary Skill | Result |

|---|---|---|

| Documentation governance | `documentation-governance` | Placement, links, front matter stay consistent |

| Documentation maintenance | `documentation-maintenance` | Code changes ship with matching docs |

| Documentation refactor | `documentation-refactor-review` | Duplicate or stale guidance is reduced |

| Documentation tone | `documentation-style-collaboration` | Wording stays clear and collaborative |

| Agent asset placement | `agent-instruction-governance` | Instruction assets stay in approved locations |

## Workflow

| Step | Agent Action | Output |

|---|---|---|

| 1. Classify | Agent maps the request to one or more coverage areas and reads `references/instruction-location-governance.md` when asset placement or instruction-location drift is in scope. | Scope list |

| 2. Inventory | Agent lists affected markdown files and source-of-truth files. | File inventory |

| 3. Select | Agent loads only the supporting skills that match the request category. | Focused skill set |

| 4. Remediate | Agent applies minimal edits, moves, or consolidations and reads `references/add-and-maintain-docs.md` for feature-linked updates, `references/refactor-and-consolidate-docs.md` for duplicate reduction, and `references/post-implementation-cleanup-docs.md` for cleanup after validated implementation. | Updated files |

| 5. Validate | Agent runs front matter, link, and placement checks. | Validation results |

| 6. Report | Agent returns files changed and follow-up items. | Completion summary |

## Reference Files

| File | Covers | Agent Reads |
|---|---|---|
| `references/add-and-maintain-docs.md` | Feature-linked doc synchronization for behavior, contract, config, and symbol changes. | Agent reads it during remediation when code changes need current-state docs. |
| `references/instruction-location-governance.md` | Canonical locations for agent assets and long-form guidance. | Agent reads it during classification and placement validation when instruction-like files move or drift. |
| `references/post-implementation-cleanup-docs.md` | Archive, delete, and manifest workflow for post-implementation documentation cleanup. | Agent reads it during remediation when validated implementation work leaves cleanup artifacts. |
| `references/refactor-and-consolidate-docs.md` | Canonical-file selection and duplicate-reduction workflow for overlapping docs. | Agent reads it during inventory and remediation when duplicate or stale guidance appears. |

## Decision Rules

Agent keeps one canonical document per topic.

Agent moves discoverable Copilot assets only inside `.agents/**` surfaces.

Agent places long-form guidance in `docs/instructions/**` or another canonical `docs/**` area.

Agent updates related indexes and links after every move or rename.

## Quality Gate

| Check | Test | Pass Criteria |

|---|---|---|

| Front matter | Run `npm run frontmatter:validate` when repository tooling exists. | Command returns zero validation errors. |

| Local links | Check changed markdown links and anchors. | Zero unresolved local links remain in changed files. |

| File placement | Compare each changed file to the canonical location map. | Every changed file matches its canonical location. |

| Change scope | Review changed files against request scope. | No unrelated documentation files change. |

## Output Contract

Agent reports coverage areas executed.

Agent reports files updated, moved, archived, or deleted.

Agent reports validation results.

Agent reports deferred follow-up items.
