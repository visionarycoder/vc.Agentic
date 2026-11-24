---
name: "fabric-medallion-architecture"
description: "Implement Microsoft Fabric bronze, silver, and gold data zones when lakehouse data quality and reuse need clear progressive refinement."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric Medallion Architecture"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric Medallion Architecture

Agent implements medallion architecture in Fabric lakehouses and OneLake. Agent keeps raw truth, validated enrichment, and curated serving data in separate zones with explicit quality boundaries.

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for one-off table creation only | Use `fabric-lakehouses` |

| User asks for report-only semantic modeling | Use `fabric-powerbi-integration` |

| User asks for operational replication without transformation | Use `fabric-shortcuts-mirroring` |

## Required Inputs

| Input | Required | Description |

|---|---|---|

| Source inventory | Yes | State raw feeds, operational systems, and inbound cadence. |

| Quality gates | Yes | State validation, standardization, and conformance checks. |

| Consumer groups | Yes | State engineering, analytics, and reporting consumers. |

| Zone retention | Yes | State history, replay, and cleanup expectations. |

| Serving targets | Recommended | State semantic models, reports, or ML feature outputs. |
