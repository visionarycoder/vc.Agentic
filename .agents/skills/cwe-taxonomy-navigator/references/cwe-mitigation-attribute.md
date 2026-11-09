---
title: CweMitigation Attribute Reference
doc_type: reference
status: active
last_updated: 2026-09-11
---
# CweMitigation Attribute Reference

`[CweMitigation]` documents compile-time security mitigations on classes, structs, and methods. The generator collects each attribute into `CweCoverageManifest.Entries` so audit tooling can discover claimed protections by CWE identifier.

## Example

Before:

```csharp
public static string SanitizeOrderBy(string columnName)
{
    return AllowedColumns.Contains(columnName) ? columnName : "CreatedOn";
}
```

After:

```csharp
[Example.Accounting.Ifx.Generators.CweMitigation(
    89,
    "Restricts ORDER BY values to an allow-list",
    Skill = "cwe-89-fix",
    Verification = "Covered by QuerySanitizerTests.SanitizeOrderBy")]
public static string SanitizeOrderBy(string columnName)
{
    return AllowedColumns.Contains(columnName) ? columnName : "CreatedOn";
}
```

## Reading the manifest

Generated code exposes `Example.Accounting.Ifx.Generators.CweCoverageManifest.Entries`. Query `Entries` where `CweId == 89` to find every class or method in the assembly that claims to mitigate SQL injection, then inspect `Mitigation`, `Skill`, `Verification`, and `TargetMemberName` for audit follow-up.
