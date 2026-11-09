---
metadata-version: "1.0.0"
title: "Documentation Governance Skill"
description: "Preserve scoped source guidance for documentation-governance."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Documentation Governance Skill

Agent reviews documentation quality and placement.

## Primary Objectives

Agent performs:
- Documentation consistency, discoverability review
- Local markdown link, reference repair
- Front matter normalization based on repository standards
- Documentation relocation to canonical paths

## Canonical Location Map

| Content Type | Location |
|---|---|
| Copilot-discoverable assets | `.github/copilot-instructions.md`, `.github/instructions/**`, `.github/prompts/**`, `.github/skills/**` |
| Architecture decisions | `docs/adr/**` |
| Developer guidance | `docs/developer-guide/**` |
| Long-form reports, plans | `docs/instructions/**` |
| Retired content | `docs/archive/**` |

## Workflow

Agent follows these steps:

1. Agent inventories markdown files, classifies each file by purpose
2. Agent identifies broken links, stale relative references
3. Agent verifies and normalizes front matter for changed markdown files
4. Agent relocates files to canonical paths when placement is incorrect
5. Agent updates inbound, outbound links after relocations
6. Agent verifies style uses collaborative language
Test: Grep for commanding phrases (must, shall, you should)
Pass: Zero commanding phrases in collaborative sections

## Decision Rules

| Content Classification | Target Location |
|---|---|
| Historical, no longer active | `docs/archive/**` |
| Records architecture decision | `docs/adr/**` |
| Reusable developer how-to | `docs/developer-guide/**` |
| Implementation plan or findings report | `docs/instructions/**` |

## Quality Gate

Agent verifies:
- [ ] Zero broken local links in changed markdown files
Test: Run link checker on changed files
Pass: Zero 404 errors
- [ ] Changed markdown files include valid front matter
Test: Run `npm run frontmatter:validate`
Pass: Zero validation errors
- [ ] File placement matches canonical location map
- [ ] Headings, prose are clear, concise, non-commanding

## Related Skills

- `documentation-link-repair`
- `documentation-frontmatter`
- `documentation-file-placement`
