---
metadata-version: "1.0.0"
title: "Documentation File Placement Skill"
description: "Preserve scoped source guidance for documentation-file-placement."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Documentation File Placement Skill

Agent classifies document purpose and places each file in a canonical location.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Documentation File Placement work | Use this skill |
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

| 1. Classify | Agent identifies document purpose and lifecycle. | Content classification |

| 2. Map | Agent selects the canonical destination path. | Target path |

| 3. Move | Agent renames or relocates the file with minimal content edits. | Moved file |

| 4. Repair | Agent updates inbound and outbound links. | Corrected navigation |

| 5. Verify | Agent checks indexes, nearby READMEs, and references. | Placement confirmation |

## Canonical Location Map

| Content Type | Canonical Location |

|---|---|

| Copilot instructions, prompts, skills | `.github/**` |

| Architecture decisions | `docs/adr/**` |

| Developer guidance | `docs/developer-guide/**` |

| Long-form plans, reports, governance | `docs/instructions/**` |

| Retired content | `docs/archive/**` |

## Naming Rules

Agent uses sibling naming patterns first.

Agent uses descriptive kebab-case names when no local pattern exists.

Agent keeps abbreviations limited to established project terms.

## Quality Gate

| Check | Test | Pass Criteria |

|---|---|---|

| Canonical placement | Compare each moved file to the location map. | Every moved file matches the classified content type. |

| Navigation | Review parent indexes and related READMEs. | Every moved file remains discoverable from nearby navigation. |

| Links | Check changed local links after the move. | Zero broken local links remain in changed files. |
