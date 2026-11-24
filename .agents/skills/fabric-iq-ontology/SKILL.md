---
name: "fabric-iq-ontology"
description: "Design Microsoft Fabric IQ ontologies with entity types, relationships, and governed business semantics when agents or users need a knowledge graph over enterprise data."
metadata:
  metadata-version: "1.0.0"
  title: "Fabric IQ Ontology"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "data"
---

# Fabric IQ Ontology

Agent designs Fabric IQ ontologies that connect business entities, relationships, and logic into a governed knowledge graph. Agent aligns ontology structure with data binding and downstream agent use.

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for transactional relational schema design | Use database design guidance |

| User asks for report-only metrics without entity graphs | Use `fabric-powerbi-integration` |

| User asks for simple table lineage only | Use `data-lineage` |

## Required Inputs

| Input | Required | Description |

|---|---|---|

| Business domain | Yes | State the core entities, terms, and decision context. |

| Source systems | Yes | State the tables, models, or items that bind into the ontology. |

| Relationship rules | Yes | State how entities connect and what the edge meaning is. |

| Consumer type | Yes | State agent, analyst, or graph query consumer. |

| Governance expectations | Recommended | State owner, approval, and term stewardship rules. |

## Ontology rules

- Give each relationship type an explicit name, direction, and meaning that expresses one stable business fact. Validate it with examples.
- Before rolling out agent grounding, validate entity and relationship completeness. Preview or query the ontology and test one downstream consumer such as a data agent or graph query.
