---
title: Source-Generated Regex Pattern Library
doc_type: reference
status: active
---

# Source-Generated Regex Pattern Library

Reusable, production-ready source-generated regex patterns for common scenarios.

---

## Mainframe Copybook Patterns

### COBOL Picture Clauses

**File:** `src/ifx/Ifx/Mainframe/CopybookPatterns.cs`

```csharp
using System.Text.RegularExpressions;

namespace Example.Accounting.Ifx.Mainframe;

/// <summary>
/// Source-generated regex patterns for COBOL copybook picture clause parsing.
/// All patterns compiled at build time for zero-cost runtime access.
/// </summary>
public static partial class CopybookPatterns
{
    /// <summary>
    /// Matches COBOL decimal picture clause with optional sign.
    /// Pattern: S?9(n)V(m)
    /// Examples: S9(5)V(2), 9(10)V(3)
    /// Groups: 1=integer digits, 2=decimal digits
    /// </summary>
    [GeneratedRegex(@"S?9\((\d+)\)V(\d*)", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex DecimalPictureRegex();

    /// <summary>
    /// Matches COBOL numeric picture clause with optional decimal portion.
    /// Pattern: 9(n) or 9(n)V9(m)
    /// Examples: 9(10), 9(5)V9(2)
    /// Groups: 1=integer digits, 2=optional V9 part, 3=decimal digits (if present)
    /// </summary>
    [GeneratedRegex(@"9\((\d+)\)(V9\((\d+)\))?", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex NumericPictureRegex();

    /// <summary>
    /// Matches COBOL alphanumeric picture clause.
    /// Pattern: X(n)
    /// Example: X(50)
    /// Groups: 1=length
    /// </summary>
    [GeneratedRegex(@"X\((\d+)\)", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex AlphanumericPictureRegex();
}
```

### Usage Example

```csharp
public class CopybookPictureParser
{
    public record PictureInfo(int? IntegerDigits, int? DecimalDigits);

    public PictureInfo ParsePictureClause(string picture)
    {
        var decimalMatch = CopybookPatterns.DecimalPictureRegex().Match(picture);
        if (decimalMatch.Success)
        {
            int.TryParse(decimalMatch.Groups[1].Value, out var intDigits);
            int.TryParse(decimalMatch.Groups[2].Value, out var decDigits);
            return new(intDigits > 0 ? intDigits : null, decDigits > 0 ? decDigits : null);
        }

        var numericMatch = CopybookPatterns.NumericPictureRegex().Match(picture);
        if (numericMatch.Success)
        {
            int.TryParse(numericMatch.Groups[1].Value, out var intDigits);
            return new(intDigits > 0 ? intDigits : null, null);
        }

        return new(null, null);
    }
}
```

---

## Validation and Parsing Patterns

### Email Validation

```csharp
public static partial class ValidationPatterns
{
    /// <summary>
    /// RFC 5322 simplified email pattern (not exhaustive but practical).
    /// Matches: user@domain.ext
    /// </summary>
    [GeneratedRegex(
        @"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
    )]
    public static partial Regex EmailRegex();
}
```

### Credit Card Format

```csharp
public static partial class PaymentPatterns
{
    /// <summary>
    /// Validates credit card number format (13-19 digits).
    /// Note: This is format validation only; use Luhn check separately.
    /// </summary>
    [GeneratedRegex(@"^\d{13,19}$", RegexOptions.CultureInvariant)]
    public static partial Regex CreditCardFormatRegex();

    /// <summary>
    /// Validates CVV format (3-4 digits).
    /// </summary>
    [GeneratedRegex(@"^\d{3,4}$", RegexOptions.CultureInvariant)]
    public static partial Regex CvvFormatRegex();
}
```

### Date and Time

```csharp
public static partial class DateTimePatterns
{
    /// <summary>
    /// ISO 8601 date format: YYYY-MM-DD
    /// Example: 2024-12-31
    /// Groups: 1=year, 2=month, 3=day
    /// </summary>
    [GeneratedRegex(@"^(\d{4})-(\d{2})-(\d{2})$", RegexOptions.CultureInvariant)]
    public static partial Regex Iso8601DateRegex();

    /// <summary>
    /// ISO 8601 datetime with time: YYYY-MM-DDTHH:MM:SS[.fff][Z]
    /// Example: 2024-12-31T23:59:59.999Z
    /// </summary>
    [GeneratedRegex(
        @"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,3})?(?:Z)?$",
        RegexOptions.CultureInvariant
    )]
    public static partial Regex Iso8601DateTimeRegex();
}
```

### Identifiers and Names

```csharp
public static partial class IdentifierPatterns
{
    /// <summary>
    /// Validates C# identifier: starts with letter or underscore, continues with alphanumeric or underscore.
    /// </summary>
    [GeneratedRegex(@"^[A-Za-z_][A-Za-z0-9_]*$", RegexOptions.CultureInvariant)]
    public static partial Regex CSharpIdentifierRegex();

    /// <summary>
    /// Validates username: alphanumeric and underscores, 3-20 characters.
    /// </summary>
    [GeneratedRegex(@"^[A-Za-z0-9_]{3,20}$", RegexOptions.CultureInvariant)]
    public static partial Regex UsernameRegex();

    /// <summary>
    /// Validates slug format: lowercase alphanumeric and hyphens.
    /// </summary>
    [GeneratedRegex(@"^[a-z0-9-]+$", RegexOptions.CultureInvariant)]
    public static partial Regex SlugRegex();
}
```

---

## File and Path Patterns

### File Names and Extensions

```csharp
public static partial class FilePatterns
{
    /// <summary>
    /// Extracts file name and extension.
    /// Groups: 1=name, 2=extension (without dot)
    /// Example: document.pdf → Groups[1]=document, Groups[2]=pdf
    /// </summary>
    [GeneratedRegex(@"^(.+?)\.([a-zA-Z0-9]+)$", RegexOptions.CultureInvariant)]
    public static partial Regex FileNameWithExtensionRegex();

    /// <summary>
    /// Matches CSV file headers.
    /// </summary>
    [GeneratedRegex(@"^[A-Za-z_][A-Za-z0-9_]*(?:,[A-Za-z_][A-Za-z0-9_]*)*$", RegexOptions.CultureInvariant)]
    public static partial Regex CsvHeaderRegex();
}
```

---

## Error and Log Parsing

### Record-Based Logs

```csharp
public static partial class LogPatterns
{
    /// <summary>
    /// Parses error message with record prefix.
    /// Pattern: Record N: message
    /// Groups: 1=record number, 2=message text
    /// Example: Record 42: Field mismatch → Groups[1]=42, Groups[2]=Field mismatch
    /// </summary>
    [GeneratedRegex(
        @"^Record\s+(\d+):\s*(.+)$",
        RegexOptions.CultureInvariant | RegexOptions.Multiline
    )]
    public static partial Regex RecordErrorMessageRegex();

    /// <summary>
    /// Parses field-based error messages.
    /// Pattern: FieldName: error description
    /// Groups: 1=field name, 2=error text
    /// </summary>
    [GeneratedRegex(
        @"^(?<field>[A-Za-z][A-Za-z0-9_]*):\s*(.+)$",
        RegexOptions.CultureInvariant | RegexOptions.Multiline
    )]
    public static partial Regex FieldErrorMessageRegex();
}
```

---

## Testing Patterns

### Unit Test Example

```csharp
[TestClass]
public class CopybookPatternTests
{
    [TestMethod]
    [DataRow("S9(5)V(2)", true, "5", "2")]
    [DataRow("9(10)V(3)", true, "10", "3")]
    [DataRow("X(50)", false, null, null)]
    public void DecimalPictureRegex_WithVariousInputs_MatchesExpectations(
        string input,
        bool shouldMatch,
        string? expectedIntDigits,
        string? expectedDecDigits
    )
    {
        var match = CopybookPatterns.DecimalPictureRegex().Match(input);

        Assert.AreEqual(shouldMatch, match.Success);
        if (shouldMatch)
        {
            Assert.AreEqual(expectedIntDigits, match.Groups[1].Value);
            Assert.AreEqual(expectedDecDigits, match.Groups[2].Value);
        }
    }

    [TestMethod]
    [DataRow("user@example.com", true)]
    [DataRow("invalid.email@", false)]
    [DataRow("@domain.com", false)]
    public void EmailRegex_WithVariousEmailFormats_ValidatesCorrectly(
        string email,
        bool expectedValidity
    )
    {
        var isValid = ValidationPatterns.EmailRegex().IsMatch(email);
        Assert.AreEqual(expectedValidity, isValid);
    }

    [TestMethod]
    [DataRow("Record 42: Field mismatch", true, "42", "Field mismatch")]
    [DataRow("Record 1: Invalid value", true, "1", "Invalid value")]
    [DataRow("Invalid format", false, null, null)]
    public void RecordErrorMessageRegex_WithErrorMessages_ParsesCorrectly(
        string input,
        bool shouldMatch,
        string? expectedRecord,
        string? expectedMessage
    )
    {
        var match = LogPatterns.RecordErrorMessageRegex().Match(input);

        Assert.AreEqual(shouldMatch, match.Success);
        if (shouldMatch)
        {
            Assert.AreEqual(expectedRecord, match.Groups[1].Value);
            Assert.AreEqual(expectedMessage, match.Groups[2].Value);
        }
    }
}
```

---

## Best Practices

### Partial Class Organization

**Structure 1: Separate file per domain**
```
src/ifx/Ifx/Mainframe/
  ├── CopybookPatterns.cs      (copybook-specific patterns)
  └── CopybookConverter.cs     (uses patterns)

src/ifx/Ifx/Validation/
  └── ValidationPatterns.cs    (email, payment, etc.)
```

**Structure 2: Single patterns file per namespace**
```
src/ifx/Ifx/
  └── GeneratedPatterns.cs     (all patterns, nested partial classes)
```

### Naming Conventions

- Suffix method names with `Regex()` for clarity
- Document intent with XML comments referencing pattern and groups
- Use `RegexOptions.CultureInvariant` for all internal patterns
- Include capture group documentation

### Performance Considerations

```csharp
// ✅ GOOD: Single pattern method
public static partial class Patterns
{
    [GeneratedRegex(@"...")]
    public static partial Regex MyPattern();
}

// Call it
var match = Patterns.MyPattern().Match(input);

// ✅ GOOD: Cache result if called repeatedly in tight loop
var regex = Patterns.MyPattern();
foreach (var line in lines)
{
    var match = regex.Match(line);
    // ...
}

// ⚠️ ACCEPTABLE: The method caches internally, so repeated calls are cheap
foreach (var line in lines)
{
    var match = Patterns.MyPattern().Match(line); // Internally cached
    // ...
}
```

---

## Migration Checklist

- [ ] Create new `*Patterns.cs` file with `public static partial class`
- [ ] Define all pattern methods with `[GeneratedRegex]`
- [ ] Add XML doc comments for each pattern
- [ ] Include regex groups in documentation
- [ ] Remove old `private static readonly Regex` fields from original class
- [ ] Update all call sites to use `ClassName.PatternName().Match/IsMatch(...)`
- [ ] Build and verify compiler generates methods
- [ ] Run unit tests — behavior must be identical
- [ ] Verify no compiler warnings

---

## See Also

- **Main Skill:** `.github/skills/dotnet-source-generated-regex/SKILL.md`
- **Legacy Skill:** `.github/skills/dotnet-compiled-regex-patterns/SKILL.md`
- **Official Docs:** https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-source-generators
- **Performance:** https://learn.microsoft.com/en-us/dotnet/standard/base-types/regex-performance
