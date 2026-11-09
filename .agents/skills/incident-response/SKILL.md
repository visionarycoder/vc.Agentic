---
name: "incident-response"
description: "Detect, stabilize, diagnose, and learn from production incidents with severity, rollback-first mitigation, and follow-up work items."
metadata:
  metadata-version: "1.0.0"
  title: "Incident Response"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Incident Response

`release-manager` applies this skill.

## Severity

| Level | Condition | Action |
|---|---|---|
| 1 | Outage or data corruption | Notify `administrative-assistant` immediately and stabilize |
| 2 | Major function degraded | Stabilize, then notify |
| 3 | Minor defect, workaround exists | Open a Bug work item |

## Process

| Step | Action | Pass criteria |
|---|---|---|
| 1. Detect | Confirm the signal in telemetry. | Evidence recorded. |
| 2. Stabilize | Roll back or mitigate before diagnosing. | Impact stops or shrinks. |
| 3. Diagnose | Find the root cause from logs, traces, and changes. | A cause is stated with evidence. |
| 4. Record | Send the timeline and root cause to `scribe`. | Record exists. |
| 5. Follow up | Open Bug work items for `project-manager`. | Every defect has a work item and a requirement trace. |

## Rules

- Never fix code. Route fixes through the normal gates.
- Keep secrets and personal data out of incident records.
