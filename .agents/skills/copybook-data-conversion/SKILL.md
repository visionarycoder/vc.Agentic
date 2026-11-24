---
name: "copybook-data-conversion"
description: "Convert EBCDIC and fixed-width mainframe data into .NET values when work needs packed decimal, sign, date, or streaming record decoding."
metadata:
  metadata-version: "1.0.0"
  title: "Copybook Data Conversion"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Copybook Data Conversion

Agent converts raw mainframe bytes into validated .NET values by combining copybook layout metadata with encoding and numeric conversion rules.

## When to Use

| Condition | Use |
|---|---|
| Work reads EBCDIC or fixed-width mainframe files | Use this skill |
| Work decodes `COMP-3`, zoned decimal, or binary `COMP` fields | Use this skill |
| Work needs streaming conversion for multi-GB data files | Use this skill |
| Work needs date, sign, or null-space normalization from mainframe records | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Work needs copybook structure extraction only | Use `mainframe-copybook-parsing` |
| Work needs generated C# models from a parsed copybook | Use `copybook-to-dotnet` |
| Work reads delimited or JSON payloads instead of fixed-width records | Use a format-specific ingestion skill |
| Work focuses on relational schema design after conversion | Use EF Core or data-modeling workflows |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Parsed copybook layout | Yes | Use validated offsets, lengths, usage, and sign metadata. |
| Source encoding | Yes | Record EBCDIC code page or ASCII-family encoding. |
| Record length | Yes | Verify fixed-width record span before conversion. |
| Reject policy | No | Record fail-fast, quarantine row, or warning-first handling. |
| Throughput target | No | Record batch size, streaming need, and memory ceiling. |

## Workflow

| Step | Action | Pass |
|---|---|---|
| 1 | Fix the encoding and record span from validated copybook metadata. | One encoding and one record length apply to the file. |
| 2 | Slice records with spans and copybook offsets. | Every field slice stays inside its declared byte range. |
| 3 | Decode alphanumeric, display numeric, packed, zoned, binary, date, `OCCURS`, `REDEFINES`, and blank-field rules. | Sign, scale, range, and alternate views remain correct. |
| 4 | Project typed values into DTOs, staging rows, or EF Core entities. | Converted rows land in one typed destination shape. |
| 5 | Choose buffered or streaming I/O and emit rejects plus diagnostics. | Large files stay memory-bounded and bad rows stay measurable. |

## COBOL Data Type Mapping

| Storage form | Conversion target | Notes |
|---|---|---|
| `PIC X(n)` | `string` | Trim and null policy stays explicit |
| Display numeric, implied decimal | `int`, `long`, or `decimal` | Blank handling stays caller-defined |
| Packed decimal `COMP-3` | `decimal` | Stored size is `ceil((digits + 1) / 2)` bytes; `PIC S9(5)V99 COMP-3` is 4 bytes |
| Zoned decimal | `decimal` or integer type | Sign from last byte overpunch |
| Binary `COMP` | `short`, `int`, or `long` | Endian-safe read; width from usage metadata and dialect |
| `COMP-1`, `COMP-2` | `float`, `double` | Rare; IEEE or dialect-specific |
| `OCCURS`, `REDEFINES` | Arrays, overlay views | Iterate repeated spans; decode overlays from shared bytes |

## Integration Hooks

| Target | Result |
|---|---|
| Microsoft Fabric ingestion | Bronze and silver stages retain byte-to-column traceability. |
| EF Core storage | Staging entities preserve precision, scale, and raw-row lineage. |

## Before and After Example

```cobol
01 PAYMENT-REC.
   05 ACCOUNT-NUMBER PIC X(10).
   05 PAYMENT-AMOUNT PIC S9(5)V99 COMP-3.
   05 EFFECTIVE-DATE PIC 9(7).
```

```csharp
public static PaymentRec Parse(ReadOnlySpan<byte> record, Encoding ebcdic) => new(
    ebcdic.GetString(record[..10]).TrimEnd(),
    PackedDecimalConverter.ReadDecimal(record.Slice(10, 4), scale: 2),
    JulianDateConverter.ReadDate(record.Slice(14, 7)));
```

## Outputs

| Output | Contents |
|---|---|
| Conversion pipeline | Encoding, field converters, and projection target |
| Typed rows | Strings, numerics, dates, arrays, and overlay views |
| Reject artifacts | Record index, field name, byte span, and failure reason |
| Performance plan | Streaming, batching, and allocation control |
