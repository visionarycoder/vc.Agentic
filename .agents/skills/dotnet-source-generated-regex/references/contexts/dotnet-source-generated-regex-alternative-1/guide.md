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

## When to Use

| User prompt | Use |
|---|---|
| User asks to modernize regex to use source generators | Use this skill |
| User asks to convert `RegexOptions.Compiled` to `[GeneratedRegex]` | Use this skill |
| User asks to optimize regex performance in .NET 7+ | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User targets .NET 6 or earlier | Use `dotnet-compiled-regex-patterns` |
| User asks for general performance optimization | Use `analyzing-dotnet-performance` first |

## Overview

Source-generated regex (introduced in .NET 7) uses the `[GeneratedRegex]` attribute to move regex compilation from runtime to compile time.

| Approach | Compilation | Runtime Cost | Trim-Safe | AOT-Safe |
|----------|-------------|--------------|-----------|----------|
| Uncompiled `Regex.Match(...)` | Runtime | High (recompile each call) | ❌ No | ❌ No |
| `RegexOptions.Compiled` | Runtime initialization | Medium (compile once) | ❌ No | ❌ No |
| `[GeneratedRegex]` | **Compile time** | **None (IL inlined)** | ✅ **Yes** | ✅ **Yes** |

**Recommendation for .NET 10:** Always prefer source-generated regex.

## Pattern: Source-Generated Regex

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

```csharp
public static Match? ParseDecimalPicture(string input)
{
    return CopybookPatterns.DecimalPictureRegex().Match(input);
}
```

## Key Benefits

| Benefit | Impact |
|---------|--------|
| **Zero-cost.** Regex compiled at build time, inlined into IL | No startup cost; no runtime compilation |
| **Trim-safe.** Works with .NET trimming and NativeAOT | Deploy smaller binaries, guaranteed correctness |
| **Type-safe.** Compiler validates regex syntax at build time | Catch pattern errors before runtime |
| **No allocations.** IL inlining reduces GC pressure | Better memory efficiency |
| **Explicit.** Clear intent in source code | Self-documenting regex usage |

## Workflow

| Step | Action | Test | Pass Criteria |
|---|---|---|---|
| 1. Create partial class | Agent creates `public static partial class` with `[GeneratedRegex]` methods. | Build project. | Build succeeds; no warnings. |
| 2. Remove old fields | Agent removes `static readonly Regex` fields and pattern constants. | Search for old field names. | Zero references to old fields remain. |
| 3. Update call sites | Agent replaces `fieldName.Match(...)` with `ClassName.Method().Match(...)`. | Run tests. | All tests pass; behavior unchanged. |
| 4. Verify options | Agent includes `RegexOptions.CultureInvariant` for internal patterns. | Review options. | Culture-invariant option present. |

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

## References

- Migration examples: `references/migration-guide.md`
- Performance data: `references/migration-guide.md`
- Comparison matrices: `references/migration-guide.md`

## Related Skills

- `dotnet-compiled-regex-patterns` — Traditional `RegexOptions.Compiled` approach
- `roslyn-source-generator-authoring` — Writing custom source generators
- `analyzing-dotnet-performance` — General performance optimization
