---
name: "fabric-data-activator"
description: "Configure Microsoft Fabric Activator rules, objects, and triggers when monitored data streams need near-real-time alerts or automated actions."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric Data Activator"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric Data Activator

Agent configures Fabric Activator for rule-based monitoring and action. Agent models objects, event conditions, and trigger paths that convert streaming changes into notifications or flows.

## Routing

Streaming storage and query design: `fabric-realtime-analytics`. Batch notifications from pipeline jobs: `fabric-data-factory-patterns`. Incident tooling outside Fabric: the owning platform guidance.

## Required Inputs

- Event source: Eventstream, dashboard, or report.
- Object key: identifier that groups events into monitored objects.
- Trigger condition: threshold, range exit, increase, decrease, or state change.
- Action path: email, Teams, Power Automate, or downstream endpoint.
- Noise tolerance (recommended): debounce, cooldown, or duplicate suppression.

## Rules

- Use a direct rule for stateless thresholds; object-based grouping for per-device or per-asset state; add Power Automate when a human workflow follows.
- Include object identity and rule intent in alert payloads.
- Validate before go-live by replaying or observing sample events (matching fire, nonmatching stay silent) and checking alert history or run output for operator traceability.
