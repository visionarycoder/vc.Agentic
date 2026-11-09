---
name: "documentation-file-placement"
description: "Place documentation files in canonical locations and preserve valid navigation."
metadata:
  metadata-version: "1.0.0"
  title: "Documentation File Placement Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Documentation File Placement Skill

Agent classifies document purpose and places each file in a canonical location.

## Canonical Location Map

| Content Type | Canonical Location |

|---|---|

| Copilot instructions, prompts, skills | `.agents/**` |

| Architecture decisions | `docs/adr/**` |

| Developer guidance | `docs/developer-guide/**` |

| Plans, internal/working documentation, scratch reports | `.sandbox/**` |
| Retired content | `docs/archive/**` |

## Workflow

| Step | Agent Action | Output |

|---|---|---|

| 1. Classify | Agent identifies document purpose and lifecycle. | Content classification |

| 2. Map | Agent selects the canonical destination path. | Target path |

| 3. Move | Agent renames or relocates the file with minimal content edits. | Moved file |

| 4. Repair | Agent updates inbound and outbound links. | Corrected navigation |

| 5. Verify | Agent checks indexes, nearby READMEs, and references. | Placement confirmation |

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

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [documentation-file-placement-alternative-1](references/contexts/documentation-file-placement-alternative-1/guide.md)
- [documentation-file-placement-alternative-2](references/contexts/documentation-file-placement-alternative-2/guide.md)
- [documentation-file-placement-alternative-3](references/contexts/documentation-file-placement-alternative-3/guide.md)
