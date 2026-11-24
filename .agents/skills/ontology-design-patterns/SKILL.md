---
name: "ontology-design-patterns"
description: "Design ontologies, RDF or OWL vocabularies, taxonomy hierarchies, and domain semantics when a prompt needs formal knowledge representation."
metadata:
  metadata-version: "1.0.0"
  title: "Ontology design patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Ontology design patterns

Use for vocabularies, RDF/OWL models, semantic alignment, and graph validation. Use a glossary for stewardship alone and a dimensional model for analytical measures alone.

1. Record bounded scope, source authority, competency questions, consumers, and expected inference or validation behavior. Record stable IRIs and versioning rules.
2. Use SHACL shapes for explicit graph constraints and state the data graph and entailment regime. Type SHACL fixture nodes explicitly when using `sh:targetClass`.
3. Record evidence before declaring external terms equivalent. Prefer weaker mappings (SKOS close/broad/narrow) where meanings differ.
4. Test competency queries, expected inferences, contradictions, and valid/invalid graph fixtures. Report each result separately and record the parser, reasoner, and SHACL engine versions, entailment settings, and the data and shapes graphs used.
5. In accounting ontologies, semantic assertions and SHACL shapes describe and validate graph data only; they grant no posting authority and establish no accounting compliance. Keep calculations and posting controls in the approved implementation boundary, and distinguish ledger, journal entry, account, amount, currency, and period concepts from storage tables.

## Bundled references

- [Reasoning and validation example](references/reasoning-examples.md): independent generic fixtures.
- [Accounting vocabulary alignment](references/accounting-ontologies.md): conceptual mapping without client files or a missing parent skill.

Use the [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/) for modeling semantics and [W3C SHACL](https://www.w3.org/TR/shacl/) for validation semantics. An external repository ontology is not a prerequisite.
