---
name: "dotnet-compiled-regex-patterns"
description: "Convert RegEx patterns to compiled regular expressions for improved runtime performance."
metadata:
  metadata-version: "1.0.0"
  title: "Compiled Regular Expression Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Compiled Regular Expression Patterns

Convert existing or ad-hoc `Regex` instances to compiled expressions to improve runtime performance.

---

## Problem

Uncompiled regex patterns recompile during each execution, incurring overhead. For frequently-used patterns, the compilation cost accumulates.

Agent avoids leaving `RegexOptions.Compiled` out:
- First invocation: parse pattern + compile to IL → execute.
- Subsequent invocations: re-parse + re-compile → execute.
- Memory cost: repeated allocation of compiled IL.

---

## Pattern

Agent uses static readonly fields or constants to hold compiled `Regex` instances:

```csharp
private const string DecimalPicturePattern = @"S?9\((\d+)\)V(\d*)";
private static readonly Regex DecimalPictureRegex = new(
    DecimalPicturePattern,
    RegexOptions.Compiled | RegexOptions.IgnoreCase
);
```

### Key points

| Item | Detail |
|------|--------|
| **Storage** | Static readonly field — survives the lifetime of the AppDomain. |
| `RegexOptions.Compiled` | Compile pattern to IL at initialization (not at match time). |
| **Pattern constant** | Separate const for reuse, testing, and documentation. |
| **Options** | Combine `RegexOptions.Compiled` with other flags (e.g., `IgnoreCase`, `CultureInvariant`). |

---

## Conversion Steps

### 1. Identify Uncompiled Patterns

Agent looks for ad-hoc `Regex` instantiation:

```csharp
// ❌ Uncompiled — recompiled on every call
var match = Regex.Match(input, @"pattern");
var isMatch = Regex.IsMatch(input, @"pattern");
new Regex(pattern).Match(input);
```

### 2. Extract to Constant

Define the pattern as a named const:

```csharp
private const string MyPattern = @"pattern";
```

### 3. Create Static Readonly Field

Agent compiles once:

```csharp
private static readonly Regex MyRegex = new(
    MyPattern,
    RegexOptions.Compiled | RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
);
```

### 4. Replace Call Sites

Agent uses the static field:

```csharp
// ❌ Before
var match = Regex.Match(input, @"S9\(\d+\)V\d*", RegexOptions.IgnoreCase);

// ✅ After
var match = DecimalPictureRegex.Match(input);
```

---

## Real-World Example

**File:** `src/ifx/Ifx/Mainframe/CopybookConverter.cs`

```csharp
using System.Text.RegularExpressions;

namespace Example.Accounting.Ifx.Mainframe;

public static class CopybookConverter
{
    private const string DecimalPicturePattern = @"S?9\((\d+)\)V(\d*)";
    private const string NumericPicturePattern = @"9\((\d+)\)(V9\((\d+)\))?";

    // Compiled at AOT — not at match time
    private static readonly Regex decimalPictureRegex = new(
        DecimalPicturePattern,
        RegexOptions.Compiled | RegexOptions.IgnoreCase
    );

    private static readonly Regex numericPictureRegex = new(
        NumericPicturePattern,
        RegexOptions.Compiled | RegexOptions.IgnoreCase
    );

    public static Match? ParseDecimalPicture(string input)
    {
        return decimalPictureRegex.Match(input); // No recompile cost
    }
}
```

---

## Performance Implications

| Scenario | Uncompiled | Compiled | Gain |
|----------|-----------|----------|------|
| 1,000 matches per cycle | ~50 ms (1,000 parses) | ~5 ms | 10x |
| First invocation | ~10 ms | ~10 ms | None |
| Steady state (n matches) | O(n × parse_cost) | O(n) | Yes |
| Memory (1 pattern) | Repeated allocations | 1 allocation | Low |

Rule of thumb: Agent compiles a pattern when the pattern runs more than five times per application lifetime.

---

## Regex Options

Combine flags with `|` (bitwise OR):

```csharp
RegexOptions.Compiled           // Compile to IL
  | RegexOptions.IgnoreCase     // a = A
  | RegexOptions.CultureInvariant // Use invariant culture (recommended for internal patterns)
  | RegexOptions.Multiline      // ^ and $ match line boundaries
  | RegexOptions.Singleline     // . matches newline
  | RegexOptions.ExplicitCapture // Only named/numbered groups are captured
```

Internal pattern rule: Agent uses `RegexOptions.CultureInvariant` to avoid locale-dependent mismatches.

---

## Validation Checklist

- [ ] Pattern extracted to `const string` with clear name
- [ ] Static readonly field declared at class scope
- [ ] `RegexOptions.Compiled` is present
- [ ] Agent updates all call sites to use the static field instead of ad-hoc `Regex.Match(...)`.
- [ ] Agent verifies matching behavior and preserves existing patterns
- [ ] No side effects from options change (e.g., `IgnoreCase` behavior is intentional)

---

## See Also

- [System.Text.RegularExpressions](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions)
- [RegexOptions.Compiled](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions.regexoptions)
- `.github/skills/analyzing-dotnet-performance/references/regex-patterns.md`

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [dotnet-compiled-regex-patterns-alternative-1](references/contexts/dotnet-compiled-regex-patterns-alternative-1/guide.md)
- [dotnet-compiled-regex-patterns-alternative-2](references/contexts/dotnet-compiled-regex-patterns-alternative-2/guide.md)
- [dotnet-compiled-regex-patterns-alternative-3](references/contexts/dotnet-compiled-regex-patterns-alternative-3/guide.md)
