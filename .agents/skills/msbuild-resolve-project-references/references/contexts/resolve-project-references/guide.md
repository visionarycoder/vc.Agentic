---
metadata-version: "1.0.0"
title: "Misleading ResolveProjectReferences Time"
description: "Preserve scoped source guidance for msbuild-resolve-project-references."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Misleading ResolveProjectReferences Time

This skill explains why `ResolveProjectReferences` often looks expensive even when it is only waiting.
This skill redirects optimization effort to true self-time hotspots.

## Interpretation Table

| Observation | Meaning | Agent action |
|---|---|---|
| `ResolveProjectReferences` dominates a summary view | Reported time includes dependent build wait time | Agent inspects task self-time and downstream targets before changing project references. |
| Dependent project compile tasks dominate | The real hotspot lives in downstream compilation or packaging work | Agent optimizes the downstream target instead. |
| Reference graph is large but idle | Wait time, not reference resolution, dominates | Agent avoids speculative project-reference rewrites. |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Inspect | Agent reads the performance summary or binlog hotspot list. | Surface symptom |
| 2. Verify | Agent checks task self-time and dependent target activity. | Root-cause classification |
| 3. Redirect | Agent targets the true expensive project, target, or task. | Focused optimization plan |
| 4. Re-measure | Agent reruns the performance view after the real fix. | Updated timing evidence |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Self-time review | Inspect task self-time in the chosen diagnostic surface. | Optimization decisions use real work, not wait time alone. |
| Change targeting | Review proposed edits. | Changes land in the actual hotspot, not in speculative churn. |
| Re-measurement | Compare before and after timing views. | The chosen hotspot metric improves or the analysis clearly explains why it does not. |
