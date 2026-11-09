---
metadata-version: "1.0.0"
title: "Documentation Refactor Review"
description: "Preserve scoped source guidance for documentation-refactor-review."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Documentation Refactor Review

Agent reviews documentation for drift, duplication, and clarity.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Documentation Refactor Review work | Use this skill |
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

| 1. Inventory | Agent lists documentation areas and source-of-truth code artifacts. | Scope inventory |

| 2. Detect | Agent identifies drift, redundancy, stale paths, and missing coverage. | Findings list |

| 3. Plan | Agent selects canonical files and consolidation actions. | Refactor plan |

| 4. Apply | Agent updates, consolidates, retires, or relinks documentation. | Refactored docs |

| 5. Validate | Agent checks references, placement, front matter, and navigation. | Validation results |

## Objectives

Agent aligns documentation with current repository structure.

Agent reduces duplicate or conflicting guidance.

Agent preserves one canonical document per topic.

Agent improves navigation and task-focused readability.

## Canonicalization Rules

| Topic | Canonical Home |

|---|---|

| Onboarding and quick reference | `docs/start-here/**`, `docs/ref/**` |

| Operations | `docs/operations/**`, `docs/ops/**` |

| Architecture and decisions | `docs/architecture/**`, `docs/adr/**` |

| Plans and findings | `docs/instructions/**` |

| Copilot assets | `.github/**` |

## Quality Gate

| Check | Test | Pass Criteria |

|---|---|---|

| Duplicate guidance | Compare related documents for repeated procedures. | One canonical procedure remains for each topic. |

| Drift | Validate paths, project names, scripts, routes, and config keys against repository files. | No known stale references remain in changed scope. |

| Navigation | Review index files and cross-links after consolidation. | Readers reach canonical docs from prior entry points. |
| Front matter and links | Run front matter validation and link review when tooling exists. | Zero validation errors and zero broken local links remain in changed files. |
