---
name: "data-intake-router"
description: "Route data and Fabric requests to the minimum correct data skill by separating KQL diagnostics, ingestion, pipeline issues, semantic models, and data-quality concerns."
metadata:
  metadata-version: "1.0.0"
  title: "Data Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Data Intake Router

Agent routes data and Fabric work to one primary data skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Fabric, KQL, ingestion, pipeline, semantic model, or data-quality work and the exact concern is unclear | Use this skill |
| Request spans more than one data-oriented specialist | Use this skill |
| User asks which data skill owns the work | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is already narrowed to one data specialist | Use that specialist |
| Request is application-domain design and data tooling is only a supporting detail | Use the domain skill first |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad data and Fabric routing belongs here |
| Fabric split | KQL, ingestion, pipelines, and semantic models stay separated unless the request explicitly combines them |
| Quality split | Data-quality work loads lineage or contract specialists only when the primary concern requires them |
| Specialist loading | Choose one primary data skill first, then only concrete secondaries |

## Verification

- [ ] Agent chose one primary data skill
- [ ] Agent kept Fabric routing specific to the observed failure or authoring mode
- [ ] Agent added a secondary data skill only when the primary scenario required it

## Routing Table

| Intent | Primary skill | Optional secondary |
|---|---|---|
| KQL failure or performance diagnosis | `fabric-kql-diagnostics` | none |
| Lakehouse ingestion shape or file landing | `fabric-lakehouse-ingestion` | `data-quality-reporting` |
| Fabric pipeline failure or orchestration issue | `fabric-pipeline-diagnostics` | none |
| Semantic model authoring | `fabric-semantic-model-builder` | `data-contract-frontmatter` |
| Data-quality reporting or rule evaluation | `data-quality-reporting` | `data-lineage` |
