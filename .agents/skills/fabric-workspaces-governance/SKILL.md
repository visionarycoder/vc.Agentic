---
name: "fabric-workspaces-governance"
description: "Configure Microsoft Fabric workspaces, capacities, security, and Git-backed governance when teams need controlled collaboration and release flow."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric Workspaces and Governance"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric Workspaces and Governance

Agent configures Fabric workspace structure, capacity placement, and governance controls. Agent aligns collaboration, security, lifecycle management, and Git integration with operating boundaries.

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for item-level lakehouse modeling only | Use `fabric-lakehouses` |

| User asks for notebook implementation only | Use `fabric-notebooks-spark` |

| User asks for ontology modeling only | Use `fabric-iq-ontology` |

## Required Inputs

| Input | Required | Description |

|---|---|---|

| Team topology | Yes | State owners, contributors, and consumers. |

| Environment model | Yes | State dev, test, prod, or equivalent stage layout. |

| Capacity plan | Yes | State region, SKU, and workload isolation needs. |

| Security model | Yes | State workspace roles, item security, and data controls. |

| Release process | Recommended | State Git, deployment pipeline, and approval expectations. |
