---
name: "dependency-maintenance"
description: "Keep packages, frameworks, and licenses current with a scheduled work item, vulnerability triage, central package versions, and normal gate review."
metadata:
  metadata-version: "1.0.0"
  title: "Dependency Maintenance"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Dependency Maintenance

`developer` (layer `tooling`) applies this skill when `project-manager` issues the scheduled maintenance work item.

## Process

| Step | Action | Pass criteria |
|---|---|---|
| 1. Inventory | List package versions in the central package file. | Every project uses central versions. |
| 2. Scan | Check each package for vulnerabilities and license changes. | Findings listed by severity. |
| 3. Triage | Order fixes: vulnerable first, then major-version gaps, then minor. | Each finding has an action. |
| 4. Update | Change versions in small, separate changes. | Build has zero analyzer warnings. |
| 5. Verify | Run the unit and integration tests. | All pass. |
| 6. Review | Submit through Gates 2 to 5. | `security-reviewer` approves vulnerability fixes. |

## Rules

- Update only through the central package file.
- Treat a license change that conflicts with policy as a block; escalate to `security-reviewer`.
- Keep each package update a separate change so a failure points to one cause.
