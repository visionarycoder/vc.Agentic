---
name: "fabric-notebooks-spark"
description: "Build Microsoft Fabric notebooks and Spark jobs for PySpark engineering, interactive analysis, and scheduled execution when data work centers on notebook code."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric Notebooks and Spark"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric Notebooks and Spark

Agent authors and operates Fabric notebooks for Spark-based data work. Agent aligns language choice, job orchestration, and lakehouse integration with the execution goal.

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for low-code ingestion only | Use `fabric-data-factory-patterns` |

| User asks for semantic model design only | Use `fabric-powerbi-integration` |

| User asks for warehouse-only T-SQL serving | Use warehouse guidance |

## Required Inputs

| Input | Required | Description |

|---|---|---|

| Notebook objective | Yes | State exploration, ETL, feature engineering, or ML training. |

| Runtime language | Yes | State PySpark, Spark SQL, Scala, or SparkR. |

| Data attachment | Yes | State lakehouse, warehouse, KQL, or file source. |

| Execution mode | Yes | State interactive, pipeline-triggered, or scheduled job. |

| Parameter set | Recommended | State runtime parameters and environment differences. |

## Notebook structure

Structure each production notebook into setup, transform, validate, and publish cells. Give each stage one observable purpose.
