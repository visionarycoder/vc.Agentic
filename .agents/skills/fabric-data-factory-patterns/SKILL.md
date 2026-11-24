---
name: "fabric-data-factory-patterns"
description: "Build Microsoft Fabric Data Factory pipelines, copy jobs, and orchestration patterns when batch ingestion or ETL spans multiple systems."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric Data Factory Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric Data Factory Patterns

Agent designs Fabric Data Factory solutions for movement, transformation, and orchestration. Agent chooses copy jobs, pipelines, dataflows, or event-driven starts from the workload shape.

## Routing

Zero-copy OneLake virtualization: `fabric-shortcuts-mirroring`. Notebook-centric Spark engineering: `fabric-notebooks-spark`. Low-latency event routing: `fabric-realtime-analytics`.

## Required Inputs

- Source and destination list: systems, formats, and Fabric targets.
- Transformation scope: copy only, low-code shaping, or custom compute.
- Orchestration depth: dependencies, branching, retries, event triggers.
- Refresh cadence: one-time, scheduled, incremental, or CDC.
- Connection model (recommended): Fabric connections and any linked-service migration mapping.

## Rules

- Choose Copy job for simple ingestion, Pipeline for orchestration, Dataflow Gen2 for low-code shaping, Eventstream for streaming.
- Map every copy output to a bronze, silver, or gold purpose.
- Parameterize environment values; define run history, alerts, and safe reruns up front.
