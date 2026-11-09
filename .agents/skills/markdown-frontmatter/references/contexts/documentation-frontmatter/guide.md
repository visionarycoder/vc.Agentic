---
metadata-version: "1.0.0"
title: "Documentation Front Matter Skill"
description: "Preserve scoped source guidance for markdown-frontmatter."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Documentation Front Matter Skill

Agent normalizes markdown metadata with the repository front matter standard.

## Standard Fields

| Field | Requirement |

|---|---|

| `title` | Agent sets a human-readable document title. |

| `doc_type` | Agent uses an allowed repository classifier. |

| `status` | Agent uses an allowed lifecycle value. |

| `last_updated` | Agent records the current edit date in `YYYY-MM-DD` format. |

## Workflow

| Step | Agent Action | Output |

|---|---|---|

| 1. Inspect | Agent checks changed markdown files for missing or malformed front matter. | Metadata findings |

| 2. Normalize | Agent adds or corrects required fields. | Updated front matter |

| 3. Preserve | Agent keeps valid existing metadata that matches repository rules. | Stable metadata |

| 4. Validate | Agent runs repository front matter validation when tooling exists. | Validation result |

## Quality Gate

| Check | Test | Pass Criteria |

|---|---|---|

| Required fields | Review changed markdown front matter. | Every changed markdown file contains required fields. |

| Allowed values | Compare values to `.agents/instructions/frontmatter-standard.instructions.md`. | Every value matches the allowed schema. |

| Repository validation | Run `npm run frontmatter:validate` when repository tooling exists. | Command returns zero validation errors. |
