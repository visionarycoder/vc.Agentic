---
name: "fabric-realtime-analytics"
description: "Implement Microsoft Fabric real-time analytics with eventstreams, KQL databases, and streaming ingestion when low-latency data drives dashboards or actions."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric Real-Time Analytics"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric Real-Time Analytics

Agent designs Fabric real-time analytics flows for data in motion. Agent combines eventstreams, Eventhouse or KQL databases, KQL query paths, and downstream visuals with low-latency objectives.

## When to Use

Use for streaming ingestion, KQL database or Eventhouse design, event-driven dashboards, and Eventstream routing in Fabric.

## When Not to Use

- Long-cycle warehouse modeling only: use lakehouse or warehouse guidance.

## Required Inputs

Gather before designing: event source, latency target, query pattern, destination. Retention scope (hot data window and archival path) is recommended.

## Design Choices

- Eventstream for continuous input, routing, and simple transformations; KQL database or Eventhouse for time-series and log storage.
- Real-time detection that drives actions: Real-Time Analytics.
- Raw data landing once and serving many consumers: prefer the OneLake-connected real-time pattern, because unified storage and shared access reduce duplicate pipelines.
- Add explicit field management and validation checkpoints for schema drift.
## Workflow

| Step | Agent action | Test | Pass |

|---|---|---|---|

| 1 | Agent maps the streaming source, schema, and latency target. | Review event contract and freshness target. | Source and service choice align with the required latency. |

| 2 | Agent defines Eventstream ingestion and routing. | Review inputs, transformations, and outputs. | Events arrive at the intended destinations. |

| 3 | Agent defines KQL database or Eventhouse tables and retention. | Review table mappings and retention settings. | Query surfaces match expected volume and history. |

| 4 | Agent writes KQL queries for operational insight. | Execute sample queries. | Queries return the expected aggregates or event slices. |

| 5 | Agent connects downstream visuals or triggers. | Review report, dashboard, or action bindings. | Consumers receive fresh data from the live query path. |

| 6 | Agent validates throughput, failure visibility, and freshness. | Monitor ingest lag and query response. | Ingestion, query, and output paths meet the stated target. |

Pass: Ingestion, query, and output paths meet the stated latency target; at least one live KQL query ran against ingested data.
