---
name: "cs-xml-doc-fixes"
description: "Fix XML documentation warnings (CS0419, CS1570-CS1658) with correct syntax, resolved crefs, and matching param tags"
metadata:
  metadata-version: "1.0.0"
  title: "CS XML Documentation Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# CS XML Documentation Fixes

Agent fixes XML documentation compiler warnings. When new XML doc CS rules appear, agent adds them to Rules Coverage matrix.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Cs Xml Doc Fixes work | Use this skill |
| Request falls inside the roslyn suite and needs this specific surface | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is broader than this skill and suite routing is still unclear | Use `roslyn-intake-router` first |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | This skill loads after `roslyn-intake-router` resolves suite scope. |

## Workflow

### 1. Inventory

```powershell
dotnet build <target> /nologo 2>&1 |
  Select-String -Pattern 'warning (CS0419|CS1570|CS1572|CS1573|CS1574|CS1584|CS1658)' |
  Group-Object { ($_ -split 'warning ')[1].Substring(0,6) } |
  Sort-Object Count -Descending
```

### 2. Fix

Agent fixes:
- **CS1572/CS1573** — Remove or rename param tags to match actual parameters
- **CS1574** — Fix cref attribute to resolvable member
- **CS1570** — Fix malformed XML syntax
- **CS0419** — Remove ambiguous cref references
- **CS1584** — Fix XML include file syntax
- **CS1658** — Fix other XML documentation warnings

### 3. Verify

- [ ] `dotnet build` clean, zero XML doc warnings
- [ ] XML tags match actual method signatures
- [ ] Cref attributes resolve to existing members

## Verification

- [ ] Agent used this skill only for its owned concern.

## Rules Coverage

| Code | Description | Fix |
|------|-------------|-----|
| CS0419 | Ambiguous reference in cref | Qualify member name or remove ambiguity |
| CS1570 | XML comment has badly formed XML | Fix XML syntax (close tags, escape characters) |
| CS1572 | XML param tag for non-existent parameter | Remove param tag or fix parameter name |
| CS1573 | Parameter has no matching param tag | Add param tag or suppress for inherited docs |
| CS1574 | XML cref attribute not resolved | Fix member name or remove invalid cref |
| CS1584 | XML include syntax error | Fix include file path or XML syntax |
| CS1658 | Warning in XML documentation | Fix specific XML error per warning detail |

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Delete all XML docs to silence warnings | Fix tags to match actual signatures |
| Copy/paste param tags without updating names | Match param names exactly |

## Outputs

Agent produces:
- Valid XML documentation matching actual signatures
- Resolvable cref attributes
- Well-formed XML syntax
