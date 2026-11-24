---
name: "fabric-synapse-analytics"
description: "Plan Microsoft Fabric and Synapse Analytics interoperability across workspaces, SQL pools, Spark pools, and notebooks when workloads span both platforms."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric and Synapse Analytics"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric and Synapse Analytics

Agent plans interoperable analytics designs across Microsoft Fabric and Azure Synapse Analytics. Agent aligns SQL pools, Spark pools, notebooks, and OneLake or ADLS access with workload boundaries.

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for Fabric-only lakehouse design | Use `fabric-lakehouses` |

| User asks for Fabric-only notebook authoring | Use `fabric-notebooks-spark` |

| User asks for Power BI semantic modeling only | Use `fabric-powerbi-integration` |

## Required Inputs

| Input | Required | Description |

|---|---|---|

| Platform boundary | Yes | State which workloads stay in Synapse and which move to Fabric. |

| Compute pattern | Yes | State SQL pool, Spark pool, notebook, or mixed execution. |

| Storage path | Yes | State OneLake, ADLS Gen2, warehouse, or lakehouse location. |

| Migration posture | Yes | State coexistence, phased cutover, or Fabric-first greenfield. |

| Consumer expectations | Recommended | State BI, data science, or engineering outcomes. |

## Pattern rule

Use a hybrid pattern when dedicated Synapse SQL or Spark pool capabilities remain central: platform-specific compute stays where its strengths matter.
