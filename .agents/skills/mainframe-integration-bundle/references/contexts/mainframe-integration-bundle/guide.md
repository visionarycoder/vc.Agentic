---
metadata-version: "1.0.0"
title: "Mainframe Integration Bundle"
description: "Preserve scoped source guidance for mainframe-integration-bundle."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Mainframe Integration Bundle

Agent uses this bundle for legacy mainframe file integration spanning copybook structure, .NET model generation, and data-format conversion.

## When to Use

| Prompt Pattern | Use This Bundle |
|---|---|
| COBOL copybook plus .NET ingestion request | Yes |
| Mainframe file decode, unpack, or migration request | Yes |
| Large fixed-width batch integration request | Yes |
| Single narrow copybook parse task with no routing need | No |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Source artifact | Yes | Copybook, sample data file, or record specification |
| Record strategy | Yes | Single record, multi-record, or REDEFINES-heavy layout |
| Target integration | Yes | C# classes, parser pipeline, ETL, or API ingestion |
| File scale | No | Daily batch size, record length, and throughput target |

## Performance Considerations for Large Mainframe Files

| Concern | Agent Focus | Pass Signal |
|---|---|---|
| File size | Stream sequential reads instead of whole-file buffering. | Working set stays bounded to parser buffers. |
| Record count | Use record-by-record parsing and batch writes. | Throughput stays stable across long runs. |
| Conversion cost | Reuse field metadata and avoid per-record reflection. | Parser cost stays dominated by I/O and decode work. |
| Error handling | Capture record offsets and continue according to policy. | Bad records isolate without losing file position. |

## Integration with Modern .NET Patterns

| Concern | Pattern |
|---|---|
| Parsing pipeline | Use streaming readers, bounded buffers, and explicit record contracts |
| Domain boundary | Keep generated transport types separate from business aggregates |
| Validation | Validate decoded records before persistence or API publication |
| Observability | Log file name, record offset, record count, and reject count with structured logging |
| Persistence | Batch database writes and keep idempotent import keys per record source |

## Decision Order

| Decision | Agent Action |
|---|---|
| Manual mapping remains simpler | Agent records manual mapping rationale and skips generation. |
| Large-file throughput risk appears | Agent applies streaming and metadata-caching patterns before implementation. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inspect source | Agent identifies copybook authority, sample file, and record strategy. | Agent records source artifacts. | One authoritative layout source exists. |
| 2. Parse structure | Agent maps levels, fields, repeats, and redefinitions. | Agent records structural metadata. | Every byte range maps to one active interpretation rule. |
| 3. Select target model | Agent chooses generated transport types or manual projection. | Agent records target model path. | One target-model path exists. |
| 4. Apply conversions | Agent decodes text, numeric, and date formats. | Inspect sample record outputs. | Decoded values match sample expectations. |
| 5. Verify throughput path | Agent checks streaming, buffering, and rejection flow. | Inspect parser design and existing tests. | Parser path supports bounded-memory execution. |

## Verification Matrix

| Area | Test | Pass |
|---|---|---|
| Copybook parse | Compare parsed metadata to copybook clauses. | Every PIC, OCCURS, and REDEFINES rule maps correctly. |
| C# generation | Inspect generated types against field definitions. | Field widths, nullability, and names stay aligned. |
| Data conversion | Run sample records through decode path. | Text, numeric, and date values match expected outputs. |
| Performance | Inspect large-file processing path. | Design uses streaming and avoids whole-file materialization. |
| Integration | Inspect decoded-record handoff to .NET services. | Transport model and domain model stay separated. |

## Common Pitfalls

| Pitfall | Agent Fix |
|---|---|
| Business model generation starts before physical layout is stable | Agent parses copybook first. |
| Generated classes leak mainframe field names into domain code | Agent keeps generated transport types at the integration boundary. |
| Large file import loads entire file into memory | Agent uses streaming readers and batch persistence. |
| REDEFINES branches lack discriminator logic | Agent records branch-selection rules during parsing. |

## Verification Checklist

- [ ] Agent created `.agents/skills/mainframe-integration-bundle/SKILL.md`.
- [ ] Agent listed all three specialist skills in coverage and routing tables.
- [ ] Agent included parse-vs-manual, conversion, performance, and .NET integration guidance.
- [ ] Agent kept `estimated_tokens` below 1200.
