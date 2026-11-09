---
name: "ontology-design-patterns"
description: "Design ontologies, RDF or OWL vocabularies, taxonomy hierarchies, and domain semantics when a prompt needs formal knowledge representation."
metadata:
  metadata-version: "1.0.0"
  title: "Ontology design patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Ontology design patterns

Use for vocabularies, RDF/OWL models, semantic alignment, and graph validation. Use a glossary for stewardship alone and a dimensional model for analytical measures alone.

1. Record bounded scope, source authority, competency questions, consumers, and expected inference or validation behavior.
2. Choose SKOS for concept schemes, RDFS for basic vocabulary relationships, or an explicit OWL profile for logical inference. Record stable IRIs and versioning rules.
3. Model classes, individuals, object properties, and data properties separately. Domain/range axioms infer types; they are not input-validation rules. Missing information is not automatically false under OWL.
4. Use SHACL shapes for explicit graph constraints. State the data graph and entailment regime. OWL cardinality alone is not a substitute for validating incomplete records.
5. Record evidence before declaring external terms equivalent. Prefer weaker mappings where meanings differ.
6. Test competency queries, expected inferences, contradictions, and valid/invalid graph fixtures using the selected parser, reasoner, and SHACL engine. Report each result separately.

## Bundled references

- [Reasoning and validation example](references/reasoning-examples.md): independent generic fixtures.
- [Accounting vocabulary alignment](references/accounting-ontologies.md): conceptual mapping without client files or a missing parent skill.

Use the [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/) for modeling semantics and [W3C SHACL](https://www.w3.org/TR/shacl/) for validation semantics. An external repository ontology is not a prerequisite.
