---
name: "fabric-copilot-studio"
description: "Connect Microsoft Fabric data agents and Microsoft Copilot Studio agents when chatbot experiences need grounded access to governed enterprise data."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric Copilot Studio Integration"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric Copilot Studio Integration

Agent connects Fabric data agents with Microsoft Copilot Studio agent experiences. Agent grounds chatbot responses in governed Fabric data and checks tenant, publication, and compliance boundaries.

## Routing

Report creation only: `fabric-powerbi-integration`. Ontology design only: `fabric-iq-ontology`. Notebook or model training only: `fabric-data-science`.

## Required Inputs

- Agent goal: question answering, task routing, or guided workflow.
- Fabric data source: lakehouse, warehouse, KQL database, mirrored database, semantic model, or ontology.
- Tenant alignment, Fabric capacity, and Copilot licensing.
- Compliance boundary (recommended): cross-geo or external processing constraints.

## Rules

- Connect a Fabric data agent to Copilot Studio only after it is published, clearly described, and reachable from the same tenant.
- Prefer a Fabric IQ (ontology)-backed data agent when the source already models business semantics.
- Report-only embedding needs the Power BI integration path, not a chat agent.
- Review compliance and geo boundaries before rollout; narrow source bindings to the target audience; test with representative, ambiguous, and out-of-scope questions.
