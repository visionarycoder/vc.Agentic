---
name: "fabric-shortcuts-mirroring"
description: "Choose Microsoft Fabric shortcuts or mirroring when external data needs virtualization or continuous replication into OneLake."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric Shortcuts and Mirroring"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric Shortcuts and Mirroring

Agent selects shortcuts or mirroring for external data access in Fabric. Agent balances zero-copy access, continuous replication, schema behavior, and read-only analytics expectations.

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for full pipeline orchestration and transformations | Use `fabric-data-factory-patterns` |

| User asks for medallion zone design after ingestion | Use `fabric-medallion-architecture` |

| User asks for workspace governance and ownership | Use `fabric-workspaces-governance` |

## Required Inputs

| Input | Required | Description |

|---|---|---|

| Source type | Yes | State OneLake, ADLS Gen2, AWS, SQL database, or SaaS source. |

| Freshness target | Yes | State on-demand, scheduled, or continuous expectation. |

| Copy tolerance | Yes | State whether duplicate storage is acceptable. |

| Write requirement | Yes | State read-only analytics or writable target expectation. |

| Schema behavior | Recommended | State whether schema drift or source evolution is expected. |

## Routing rule

Route workloads that need transformations before serving to copy jobs or pipelines, not mirroring.
