---
metadata-version: "1.0.0"
title: "Reasoning and validation example"
description: "Use generic fixtures for RDF inference and SHACL checks."
document-type: "index"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Reasoning and validation example

This fictional vocabulary is an example, not a project contract.

```turtle
@prefix ex: <https://example.org/demo/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:Project a rdfs:Class .
ex:owner rdfs:domain ex:Project .
ex:demo ex:owner ex:alice .
```

RDFS entailment infers that `ex:demo` is a Project. Missing an owner does not by itself establish a logical inconsistency.

Use a separate shape for an explicit data requirement:

```turtle
@prefix ex: <https://example.org/demo/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
ex:ProjectShape a sh:NodeShape ;
    sh:targetClass ex:Project ;
    sh:property [ sh:path ex:owner ; sh:minCount 1 ; sh:maxCount 1 ] .
```

Explicitly type each validation fixture as `ex:Project` so results do not depend on inferred target membership. Check one owner conforms, zero violates minimum count, and two distinct owners violate maximum count. Record engine/version, inference settings, both graphs, and results.

See [W3C SHACL](https://www.w3.org/TR/shacl/) and the [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/).
