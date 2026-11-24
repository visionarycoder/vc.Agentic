---
name: "mainframe-copybook-parsing"
description: "Parse COBOL copybooks into validated structural models when work needs field layout, hierarchy, or parser strategy selection."
metadata:
  metadata-version: "1.0.0"
  title: "Mainframe Copybook Parsing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Mainframe Copybook Parsing

Agent parses COBOL copybooks into hierarchical field models with offsets, lengths, data semantics, and validation results.

## When to Use

| Condition | Use |
|---|---|
| Work starts with a COBOL copybook and no trusted structural model exists | Use this skill |
| Work needs field offsets, lengths, OCCURS counts, or REDEFINES overlays | Use this skill |
| Work needs parser design guidance for .NET ingestion components | Use this skill |
| Work needs copybook validation before data conversion or class generation | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Work already has a validated parsed model and only needs C# emission | Use `copybook-to-dotnet` |
| Work focuses on byte decoding from EBCDIC or packed fields | Use `copybook-data-conversion` |
| Work asks for XML or delimited schema inference instead of copybooks | Use `xml-schema-inference` or `csv-ingestion-diagnostics` |
| Work edits COBOL business logic outside copybook structure | Use a COBOL code workflow |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Copybook source | Yes | Record file path, encoding, and line-continuation style. |
| Dialect facts | No | Record IBM Enterprise COBOL, Micro Focus, or local extensions when known. |
| Record root name | No | Derive the 01 group when the caller omits it. |
| Validation strictness | No | Record fail-fast or warning-first behavior. |
| Downstream target | No | Record C# generation, Fabric ingestion, EF Core staging, or diagnostics. |

## Rules

| Topic | Rule |
|---|---|
| Strategy selection | Choose a custom parser, a third-party adapter, or a staged preprocessor plus parser; match the choice to dialect breadth and delivery needs. |
| Dialect handling | Record unresolved dialect-dependent width or syntax as a validation finding with line scope instead of guessing; flag unsupported dialect constructs. |
| Separation of concerns | Keep parsing distinct from EBCDIC decoding and .NET type emission. |
| Validation | Report clause combinations, level jumps, duplicate names, and unsupported features as errors or warnings with line scope. |

## Outputs

- Structural model with record name, hierarchy, offsets, lengths, and clause metadata
- Validation report with errors, warnings, and source locations
- Parser-strategy selection record
- Integration metadata for generation, staging, or ingestion
