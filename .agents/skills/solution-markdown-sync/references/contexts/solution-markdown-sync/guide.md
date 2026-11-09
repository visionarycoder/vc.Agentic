---
metadata-version: "1.0.0"
title: "Solution Markdown Sync Skill"
description: "Preserve scoped source guidance for solution-markdown-sync."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Solution Markdown Sync Skill

This skill keeps solution metadata aligned with repository markdown conventions when the repository expects markdown inclusion.
This skill acts only inside the affected solution scope.

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Inventory | Agent lists changed markdown files and the solution files that track them. | Sync scope |
| 2. Compare | Agent compares markdown paths to current `.slnx` entries or equivalent repository conventions. | Delta list |
| 3. Update | Agent adds, removes, or renames solution entries only when the convention requires it. | Synchronized solution |
| 4. Validate | Agent verifies the solution file still loads and references the intended markdown assets. | Verified sync |

## Decision Rules

Agent updates only the solution entries that correspond to changed markdown assets.
Agent does not add unrelated files to a solution.
Agent keeps markdown assets in canonical `.agents/**` or `docs/**` locations before updating solution metadata.

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Scope control | Review changed solution entries. | Only markdown-related entries in scope changed. |
| Path accuracy | Compare solution entries to actual file paths. | Every changed entry points to an existing markdown file. |
| Convention fit | Review repository guidance for markdown inclusion. | The solution reflects the documented convention. |
