---
name: "fabric-lakehouses"
description: "Design Microsoft Fabric lakehouses with Delta tables, OneLake layout, and lakehouse-versus-warehouse choices when analytics needs open data storage."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric Lakehouses"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric Lakehouses

Agent designs Fabric lakehouses for open-format analytics. Agent aligns Delta tables, Files and Tables layout, and OneLake access with the workload shape.

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for warehouse-only SQL serving | Use warehouse guidance |

| User asks for pipeline orchestration only | Use `fabric-data-factory-patterns` |

| User asks for medallion zone design across domains | Use `fabric-medallion-architecture` |

## Required Inputs

| Input | Required | Description |

|---|---|---|

| Data shape | Yes | State structured tables, semi-structured files, or mixed assets. |

| Primary engine | Yes | State Spark, SQL, Power BI, or mixed access. |

| Data latency | Yes | State batch, near-real-time, or mixed refresh targets. |

| Governance scope | Yes | State workspace, domain, and access boundaries. |

| Open-format requirement | Recommended | State Delta or Iceberg interoperability needs. |
