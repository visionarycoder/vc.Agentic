---
metadata-version: "1.0.0"
title: "Documentation Maintenance"
description: "Preserve scoped source guidance for documentation-maintenance."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Documentation Maintenance

Agent treats documentation as part of the code change.

Every observable code change requires matching documentation review.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Documentation Maintenance work | Use this skill |
| Request falls inside the documentation suite and needs this specific surface | Use this skill |
| The routed catalog needs a single current-state owner for this concern | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is broader than this skill and suite routing is still unclear | Use `documentation-intake-router` first |
| Request belongs to a narrower specialist than this skill | Use that narrower specialist |
| Request is outside this skill's suite or concern | Use the correct suite router or execution skill |

## Workflow

| Step | Agent Action | Output |

|---|---|---|

| 1. Detect | Agent identifies observable code changes and affected document surfaces. | Documentation impact list |

| 2. Search | Agent finds references to changed names, paths, routes, flags, and config keys. | Reference inventory |

| 3. Update | Agent edits only the surfaces that assert the changed behavior. | Synchronized docs |

| 4. Validate | Agent checks front matter, links, and code-comment coverage. | Validation results |

| 5. Report | Agent returns changed surfaces and unresolved follow-up items. | Completion summary |

## Documentation Surface Map

| Surface | Location | Typical Trigger |

|---|---|---|

| Copilot instructions and skills | `.github/**` | Agent behavior, prompts, skill updates |

| Long-form guidance | `docs/instructions/**` | Plans, reports, standards, migration notes |

| Operations | `docs/ops/**` | Flags, schedules, dependencies, runbooks |

| Architecture | `docs/architecture/**`, `docs/adr/**` | Design changes and durable decisions |

| READMEs | `README.md`, `<project>/README.md` | Build, run, purpose, local usage changes |

| API comments | C# XML docs, TS JSDoc | Public API or exported symbol changes |

## Trigger Map

| Change Type | Agent Update |

|---|---|

| New feature or endpoint | Agent updates API comments, READMEs, and long-form guidance that documents the changed behavior. |

| Behavior change | Agent updates docs that state the old behavior. |

| Rename or move | Agent updates references, paths, and links. |

| Deletion | Agent removes or rewrites stale documentation in the same change. |

| Ops or security change | Agent updates runbooks, matrices, and configuration guidance. |

## Required Rules

Agent updates documentation in the same change as the code.

Agent uses repository-relative paths for code references.

Agent keeps one canonical document per topic and replaces duplicates with links.

Agent keeps Copilot-discoverable assets inside supported `.github/**` locations.

Agent keeps long-form guidance inside canonical `docs/**` locations.

## Quality Gate

| Check | Test | Pass Criteria |

|---|---|---|

| Public API comments | Review changed public C# and exported TS symbols. | Every changed public or exported symbol includes current docs when the surface requires comments. |

| Behavior references | Search docs for old names, routes, flags, scopes, and config keys. | Zero stale references remain in changed scope. |

| Ops guidance | Review `docs/ops/**` when operational behavior changes. | Every affected operational contract is documented. |

| Link and front matter quality | Run link review and `npm run frontmatter:validate` when tooling exists. | Zero broken local links and zero front matter validation errors remain in changed files. |
