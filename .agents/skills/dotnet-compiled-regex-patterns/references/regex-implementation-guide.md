---
title: Compiled Regex Patterns — Reference
doc_type: reference
status: active
---

# Compiled Regex Patterns — Implementation Reference

Detailed examples and patterns for converting regex to compiled expressions across common scenarios.

---

## Pattern Library

### COBOL Picture Clauses (Copybook Parsing)

**Use case:** Parse mainframe COBOL picture clauses for decimal and numeric fields.

```csharp
private const string DecimalPicturePattern = @"S?9\((\d+)\)V(\d*)";
private const string NumericPicturePattern = @"9\((\d+)\)(V9\((\d+)\))?";

private static readonly Regex DecimalPictureRegex = new(
    DecimalPicturePattern,
    RegexOptions.Compiled | RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
);

private static readonly Regex NumericPictureRegex = new(
    NumericPicturePattern,
    RegexOptions.Compiled | RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
);

public static (int? IntegerDigits, int? DecimalDigits) ParsePictureClause(string picture)
{
    var match = DecimalPictureRegex.Match(picture);
    if (!match.Success)
        match = NumericPictureRegex.Match(picture);

    if (!match.Success)
        return (null, null);

    int.TryParse(match.Groups[1].Value, out var intDigits);
    int.TryParse(match.Groups[2].Value, out var decimalDigits);

    return (intDigits > 0 ? intDigits : null, decimalDigits > 0 ? decimalDigits : null);
}
```

### Email Validation

**Use case:** RFC 5322 simplified email pattern.

```csharp
private const string EmailPattern = @"^[^\s@]+@[^\s@]+\.[^\s@]+$";

private static readonly Regex EmailRegex = new(
    EmailPattern,
    RegexOptions.Compiled | RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
);

public static bool IsValidEmail(string email)
{
    return EmailRegex.IsMatch(email);
}
```

### Credit Card (Minimal)

**Use case:** Check format before validation.

```csharp
private const string CreditCardPattern = @"^\d{13,19}$";

private static readonly Regex CreditCardRegex = new(
    CreditCardPattern,
    RegexOptions.Compiled | RegexOptions.CultureInvariant
);

public static bool IsValidCardFormat(string cardNumber)
{
    return CreditCardRegex.IsMatch(cardNumber);
}
```

### ISO 8601 Date-Time

**Use case:** Parse ISO 8601 timestamp.

```csharp
private const string Iso8601Pattern = @"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})";

private static readonly Regex Iso8601Regex = new(
    Iso8601Pattern,
    RegexOptions.Compiled | RegexOptions.CultureInvariant
);

public static bool IsValidIso8601(string timestamp)
{
    return Iso8601Regex.IsMatch(timestamp);
}
```

### Alphanumeric + Underscores

**Use case:** Identifier validation (usernames, variable names).

```csharp
private const string IdentifierPattern = @"^[A-Za-z_][A-Za-z0-9_]*$";

private static readonly Regex IdentifierRegex = new(
    IdentifierPattern,
    RegexOptions.Compiled | RegexOptions.CultureInvariant
);

public static bool IsValidIdentifier(string name)
{
    return IdentifierRegex.IsMatch(name);
}
```

### Line-Separated Records

**Use case:** Parse error messages with line prefix.

```csharp
private const string RecordLinePattern = @"^Record\s+(\d+):\s*(.+)$";

private static readonly Regex RecordLineRegex = new(
    RecordLinePattern,
    RegexOptions.Compiled | RegexOptions.CultureInvariant | RegexOptions.Multiline
);

public static (int RecordNumber, string Message)? ParseRecordLine(string line)
{
    var match = RecordLineRegex.Match(line);
    if (!match.Success)
        return null;

    if (!int.TryParse(match.Groups[1].Value, out var recordNumber))
        return null;

    var message = match.Groups[2].Value;
    return (recordNumber, message);
}
```

---

## Migration Patterns

### Before → After

#### Pattern 1: Inline Regex in Methods

```csharp
// ❌ Before — Recompiled on each call
public class ValidationService
{
    public bool IsValidEmail(string email)
    {
        return Regex.IsMatch(email, @"^[^\s@]+@[^\s@]+\.[^\s@]+$", RegexOptions.IgnoreCase);
    }
}

// ✅ After — Compiled once
public class ValidationService
{
    private const string EmailPattern = @"^[^\s@]+@[^\s@]+\.[^\s@]+$";
    private static readonly Regex EmailRegex = new(
        EmailPattern,
        RegexOptions.Compiled | RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
    );

    public bool IsValidEmail(string email)
    {
        return EmailRegex.IsMatch(email);
    }
}
```

#### Pattern 2: Multiple Patterns in Helper

```csharp
// ❌ Before
public static class CopybookHelper
{
    public static Match? MatchDecimal(string picture)
    {
        return Regex.Match(picture, @"S?9\((\d+)\)V(\d*)", RegexOptions.IgnoreCase);
    }

    public static Match? MatchNumeric(string picture)
    {
        return Regex.Match(picture, @"9\((\d+)\)(V9\((\d+)\))?", RegexOptions.IgnoreCase);
    }
}

// ✅ After
public static class CopybookHelper
{
    private const string DecimalPattern = @"S?9\((\d+)\)V(\d*)";
    private const string NumericPattern = @"9\((\d+)\)(V9\((\d+)\))?";

    private static readonly Regex DecimalRegex = new(
        DecimalPattern,
        RegexOptions.Compiled | RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
    );

    private static readonly Regex NumericRegex = new(
        NumericPattern,
        RegexOptions.Compiled | RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
    );

    public static Match? MatchDecimal(string picture) => DecimalRegex.Match(picture);
    public static Match? MatchNumeric(string picture) => NumericRegex.Match(picture);
}
```

---

## Testing Strategy

### Unit Test Example

```csharp
[TestClass]
public class CopybookHelperTests
{
    [TestMethod]
    public void MatchDecimal_WithValidPicture_ReturnsMatch()
    {
        // Arrange
        var picture = "S9(5)V(2)";

        // Act
        var match = CopybookHelper.MatchDecimal(picture);

        // Assert
        Assert.IsTrue(match!.Success);
        Assert.AreEqual("5", match.Groups[1].Value);
        Assert.AreEqual("2", match.Groups[2].Value);
    }

    [TestMethod]
    public void MatchDecimal_WithoutSignPrefix_ReturnsMatch()
    {
        // Arrange
        var picture = "9(10)V(3)";

        // Act
        var match = CopybookHelper.MatchDecimal(picture);

        // Assert
        Assert.IsTrue(match!.Success);
    }

    [TestMethod]
    public void MatchDecimal_WithInvalidFormat_ReturnsNoMatch()
    {
        // Arrange
        var picture = "INVALID";

        // Act
        var match = CopybookHelper.MatchDecimal(picture);

        // Assert
        Assert.IsFalse(match?.Success ?? false);
    }
}
```

---

## Performance Validation

### Benchmark Example (BenchmarkDotNet)

```csharp
[MemoryDiagnoser]
[SimpleJob(warmupCount: 3, targetCount: 5)]
public class RegexCompilationBenchmark
{
    private const string DecimalPattern = @"S?9\((\d+)\)V(\d*)";
    private const string TestPicture = "S9(5)V(2)";

    private static readonly Regex CompiledRegex = new(
        DecimalPattern,
        RegexOptions.Compiled | RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
    );

    private static readonly Regex UncompiledRegex = new(
        DecimalPattern,
        RegexOptions.IgnoreCase | RegexOptions.CultureInvariant
    );

    [Benchmark(Baseline = true)]
    public Match UncompiledMatch()
    {
        return UncompiledRegex.Match(TestPicture);
    }

    [Benchmark]
    public Match CompiledMatch()
    {
        return CompiledRegex.Match(TestPicture);
    }

    [Benchmark]
    public bool InlineRegexMatch()
    {
        return Regex.IsMatch(TestPicture, DecimalPattern, RegexOptions.IgnoreCase);
    }
}
```

**Expected result:** Compiled >= Inline > Uncompiled (after warm-up).

---

## Dos and Don'ts

| Do | Don't |
|---|---|
| ✅ Make patterns `static readonly` at class scope | ❌ Create new Regex in loops |
| ✅ Use `RegexOptions.Compiled` | ❌ Trust ad-hoc Regex.Match() performance |
| ✅ Use `RegexOptions.CultureInvariant` for internal patterns | ❌ Mix culture-dependent and culture-invariant patterns without intent |
| ✅ Document pattern purpose with comments | ❌ Use magic regex strings unexplained |
| ✅ Extract patterns to named constants | ❌ Embed raw patterns inline |
| ✅ Test patterns in unit tests | ❌ Assume patterns work without verification |

---

## Related Skills

- `.github/skills/analyzing-dotnet-performance/` — Broader performance diagnostics
- `.github/skills/microbenching/` — Set up BenchmarkDotNet suites
