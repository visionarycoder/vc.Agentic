---
title: Source-Generated Regex Migration Guide
description: Detailed migration examples and performance comparisons for moving from runtime-compiled to source-generated regex.
doc_type: reference
status: active
last_updated: 2026-08-22
target_audience: ai
complexity: medium
estimated_tokens: 1200
parent_skill: dotnet-source-generated-regex
tags:
  - dotnet
  - regex
  - migration
  - examples
---

# Source-Generated Regex Migration Guide

Detailed examples and performance data for migrating regex patterns to source generators.

## Migration: Before → After

### Current Implementation (Runtime-Compiled)

```csharp
public static class CopybookConverter
{
    private const string DecimalPicturePattern = @"S?9\((\d+)\)V(\d*)";
    private const string NumericPicturePattern = @"9\((\d+)\)(V9\((\d+)\))?";

    // ⚠️ Runtime compilation at application startup
    private static readonly Regex decimalPictureRegex = new(
        DecimalPicturePattern,
        RegexOptions.Compiled | RegexOptions.IgnoreCase
    );

    private static readonly Regex numericPictureRegex = new(
        NumericPicturePattern,
        RegexOptions.Compiled | RegexOptions.IgnoreCase
    );

    public static Match? MatchDecimal(string picture)
    {
        return decimalPictureRegex.Match(picture);
    }
}
```

### Modern Implementation (Source-Generated)

```csharp
using System.Text.RegularExpressions;

namespace Example.Accounting.Ifx.Mainframe;

/// <summary>
/// Source-generated regex patterns for copybook picture clause parsing.
/// Patterns are compiled at build time, not runtime.
/// </summary>
public static partial class CopybookPatterns
{
    /// <summary>
    /// Matches COBOL decimal picture clause: S?9(n)V(m)
    /// Example: S9(5)V(2) → Sign (optional), 5 digits, 2 decimal places
    /// </summary>
    [GeneratedRegex(@"S?9\((\d+)\)V(\d*)", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex DecimalPictureRegex();

    /// <summary>
    /// Matches COBOL numeric picture clause: 9(n) or 9(n)V9(m)
    /// Example: 9(10)V9(3) → 10 digits, optional 3 decimal places
    /// </summary>
    [GeneratedRegex(@"9\((\d+)\)(V9\((\d+)\))?", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex NumericPictureRegex();
}

// In CopybookConverter.cs
public static class CopybookConverter
{
    public static Match? MatchDecimal(string picture)
    {
        return CopybookPatterns.DecimalPictureRegex().Match(picture);
    }

    public static Match? MatchNumeric(string picture)
    {
        return CopybookPatterns.NumericPictureRegex().Match(picture);
    }
}
```

## Step-by-Step Migration

### Step 1: Create Patterns Partial Class

```csharp
// File: src/ifx/Ifx/Mainframe/CopybookPatterns.cs
using System.Text.RegularExpressions;

namespace Example.Accounting.Ifx.Mainframe;

public static partial class CopybookPatterns
{
    [GeneratedRegex(@"S?9\((\d+)\)V(\d*)", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex DecimalPictureRegex();

    [GeneratedRegex(@"9\((\d+)\)(V9\((\d+)\))?", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex NumericPictureRegex();
}
```

### Step 2: Remove Runtime Field Declarations

Delete these lines:
```csharp
// ❌ DELETE
private const string DecimalPicturePattern = @"S?9\((\d+)\)V(\d*)";
private const string NumericPicturePattern = @"9\((\d+)\)(V9\((\d+)\))?";
private static readonly Regex decimalPictureRegex = new(...);
private static readonly Regex numericPictureRegex = new(...);
```

### Step 3: Update Call Sites

```csharp
// ❌ Before
var match = decimalPictureRegex.Match(picture);

// ✅ After
var match = CopybookPatterns.DecimalPictureRegex().Match(picture);
```

### Step 4: Build and Verify

```bash
dotnet build src/ifx/Ifx/Ifx.csproj
```

## Performance Profile

| Operation | Uncompiled | `RegexOptions.Compiled` | `[GeneratedRegex]` |
|-----------|-----------|-------------------------|-------------------|
| First call | ~50ms (parse + compile) | ~50ms (parse + compile) | <1ms (cached IL) |
| Subsequent calls | ~5ms each | ~2ms each | <0.5ms (inlined) |
| Startup time | No impact | +100ms–200ms compile | No impact |
| Memory overhead | High (repeated allocations) | Medium (1 compiled instance) | Low (inlined IL) |
| AOT/Trimming | ❌ Incompatible | ❌ Incompatible | ✅ Compatible |

## Comparison Matrix

| Feature | `Regex(pattern, RegexOptions.Compiled)` | `[GeneratedRegex]` |
|---------|---------------------------------------|-------------------|
| **Requires .NET** | 2.0+ | 7.0+ |
| **Compilation** | Runtime at startup | Build time |
| **Startup latency** | Yes (blocking) | No |
| **Trim-safe** | No | Yes |
| **Version check** | Required at runtime | Guaranteed at build |
| **Regex validation** | Runtime exception | Build-time error |
| **Call site code** | `regex.Match(...)` | `ClassName.Method().Match(...)` |
| **Performance** | Good | Excellent |

## Generated Code Reference

The compiler generates code similar to this (transparent to you):

```csharp
// ✨ This is generated automatically — you do NOT write this
public static partial Regex DecimalPictureRegex()
{
    return new Regex(
        @"S?9\((\d+)\)V(\d*)",
        RegexOptions.IgnoreCase | RegexOptions.CultureInvariant,
        TimeSpan.FromMilliseconds(...)
    );
}
```

The generated method caches the regex instance, so repeated calls are cheap.

## Example: CopybookConverter Migration

### Current State

```csharp
private const string DecimalPicturePattern = @"S?9\((\d+)\)V(\d*)";
private const string NumericPicturePattern = @"9\((\d+)\)(V9\((\d+)\))?";

private static readonly Regex decimalPictureRegex = new(DecimalPicturePattern, RegexOptions.Compiled | RegexOptions.IgnoreCase);
private static readonly Regex numericPictureRegex = new(NumericPicturePattern, RegexOptions.Compiled | RegexOptions.IgnoreCase);
```

### Post-Migration

**New file: `CopybookPatterns.cs`**
```csharp
using System.Text.RegularExpressions;

namespace Example.Accounting.Ifx.Mainframe;

public static partial class CopybookPatterns
{
    [GeneratedRegex(@"S?9\((\d+)\)V(\d*)", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex DecimalPictureRegex();

    [GeneratedRegex(@"9\((\d+)\)(V9\((\d+)\))?", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex NumericPictureRegex();
}
```

**Updated: `CopybookConverter.cs`**
```csharp
public static Match? ParseDecimalPicture(string picture)
{
    return CopybookPatterns.DecimalPictureRegex().Match(picture);
}
```
