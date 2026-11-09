---
metadata-version: "1.0.0"
title: "Source-Generated Compiled Regular Expressions"
description: "Preserve scoped source guidance for dotnet-source-generated-regex."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Source-Generated Compiled Regular Expressions

Convert runtime-compiled regex patterns to compile-time source-generated patterns for zero-cost abstraction, trim-safe code, and improved performance in .NET 7+.

---

## Overview

**Source-generated regex** (introduced in .NET 7) uses the `[GeneratedRegex]` attribute to move regex compilation from runtime to compile time.

| Approach | Compilation | Runtime Cost | Trim-Safe | AOT-Safe |
|----------|-------------|--------------|-----------|----------|
| Uncompiled `Regex.Match(...)` | Runtime | High (recompile each call) | ❌ No | ❌ No |
| `RegexOptions.Compiled` | Runtime initialization | Medium (compile once) | ❌ No | ❌ No |
| `[GeneratedRegex]` | **Compile time** | **None (IL inlined)** | ✅ **Yes** | ✅ **Yes** |

**Recommendation for .NET 10:** Always prefer source-generated regex.

---

## Pattern: Source-Generated Regex

### Basic Syntax

Create a partial method decorated with `[GeneratedRegex]`:

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

### Usage

Call the generated methods (no need to store static fields):

```csharp
public static Match? ParseDecimalPicture(string input)
{
    return CopybookPatterns.DecimalPictureRegex().Match(input);
}
```

---

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

---

## Key Benefits

| Benefit | Impact |
|---------|--------|
| **Zero-cost.** Regex compiled at build time, inlined into IL | No startup cost; no runtime compilation |
| **Trim-safe.** Works with .NET trimming and NativeAOT | Deploy smaller binaries, guaranteed correctness |
| **Type-safe.** Compiler validates regex syntax at build time | Catch pattern errors before runtime |
| **No allocations.** IL inlining reduces GC pressure | Better memory efficiency |
| **Explicit.** Clear intent in source code | Self-documenting regex usage |

---

## Step-by-Step Migration

### Step 1: Create Patterns Partial Class

Create a new file or add to existing helpers:

```csharp
// File: src/ifx/Ifx/Mainframe/CopybookPatterns.cs
using System.Text.RegularExpressions;

namespace Example.Accounting.Ifx.Mainframe;

/// <summary>
/// Source-generated regex patterns for mainframe copybook parsing.
/// </summary>
public static partial class CopybookPatterns
{
    [GeneratedRegex(@"S?9\((\d+)\)V(\d*)", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex DecimalPictureRegex();

    [GeneratedRegex(@"9\((\d+)\)(V9\((\d+)\))?", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex NumericPictureRegex();
}
```

### Step 2: Remove Runtime Field Declarations

In `CopybookConverter.cs`, delete these lines:

```csharp
// ❌ DELETE THESE
private const string DecimalPicturePattern = @"S?9\((\d+)\)V(\d*)";
private const string NumericPicturePattern = @"9\((\d+)\)(V9\((\d+)\))?";
private static readonly Regex decimalPictureRegex = new(...);
private static readonly Regex numericPictureRegex = new(...);
```

### Step 3: Update Call Sites

Replace regex field access with generated method calls:

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

The C# compiler automatically generates the implementation of partial methods marked `[GeneratedRegex]`.

---

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

**Important:** The generated method caches the regex instance, so repeated calls are cheap.

---

## Validation Checklist

- [ ] Class is marked `public static partial`
- [ ] Method is marked `public static partial` with no body
- [ ] `[GeneratedRegex]` attribute includes the pattern string
- [ ] `[GeneratedRegex]` includes `RegexOptions.CultureInvariant` for internal patterns
- [ ] Build succeeds without compiler warnings
- [ ] All call sites updated to use generated methods
- [ ] Old static field declarations removed
- [ ] Unit tests pass (behavior unchanged)
- [ ] Pattern is documented with XML comments

---

## Example: CopybookConverter Migration

### Current State (Lines 13–17)

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

**Updated: `CopybookConverter.cs`** (remove lines 13–17, update call sites)
```csharp
public static Match? ParseDecimalPicture(string picture)
{
    return CopybookPatterns.DecimalPictureRegex().Match(picture);
}
```

---

## Performance Profile

| Operation | Uncompiled | `RegexOptions.Compiled` | `[GeneratedRegex]` |
|-----------|-----------|-------------------------|-------------------|
| First call | ~50ms (parse + compile) | ~50ms (parse + compile) | <1ms (cached IL) |
| Subsequent calls | ~5ms each | ~2ms each | <0.5ms (inlined) |
| Startup time | No impact | +100ms–200ms compile | No impact |
| Memory overhead | High (repeated allocations) | Medium (1 compiled instance) | Low (inlined IL) |
| AOT/Trimming | ❌ Incompatible | ❌ Incompatible | ✅ Compatible |

---

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

---

## Common Patterns Library

See companion reference: `.github/skills/dotnet-source-generated-regex/references/pattern-library.md`

---

## Related Skills

- `.github/skills/dotnet-compiled-regex-patterns/` — Traditional `RegexOptions.Compiled` approach
- `.github/skills/roslyn-source-generator-authoring/` — Writing custom source generators
- `https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-source-generators` — Official MS documentation
