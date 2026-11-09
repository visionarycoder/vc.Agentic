---
name: "mapping-crosswalk-governance"
description: "Build, review, and change value mappings and crosswalks between systems with traceable sources, conflict logging, and reverse-mapping limits."
metadata:
  metadata-version: "1.0.0"
  title: "Mapping Crosswalk Governance"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Mapping Crosswalk Governance

`application-architect` applies this skill for every component that maps values. `product-owner` approves the business meaning of each row. `solution-architect` verifies at Gate 1 that the mapping respects the ontology.

## Crosswalk Row

| Field | Content |
|---|---|
| Source system and field | System, field, and source value |
| Target system and field | System, field, and target value |
| Direction | Forward only, or reversible |
| Information loss | Source values that collapse to the same target value |
| Source document | Document name and version that fixes the value |

## Process

| Step | Test | Pass criteria |
|---|---|---|
| 1. Collect sources | List every document that states the mapping. | Each has a name and version. |
| 2. Compare | Diff the values across documents. | Each disagreement appears in the conflict log. |
| 3. Rule | Pick a value from the evidence, or ask `product-owner` when meaning decides. | Each conflict has a ruling or an owner. |
| 4. Reversibility | Group source values by target value. | Each many-to-one group is marked not reversible. |
| 5. Publish | Put the mapping specification in the detailed design and write it into the detailed design directly. | Every row cites its source and the `developer` receives it as part of the definition of success. |
| 6. Hand off test data | Export the value pairs. | `test-architect` receives the pairs for contract and acceptance tests. |

## Rules

- Change a mapping only after the crosswalk row changes.
- Record the version of each source document with every row.
- Treat a missing, extra, or conflicting value as a defect, not a guess.
