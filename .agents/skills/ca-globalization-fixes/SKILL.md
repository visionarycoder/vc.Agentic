---
name: "ca-globalization-fixes"
description: "Remediate culture-sensitive string and formatting operations with explicit CultureInfo or StringComparison"
metadata:
  metadata-version: "1.0.0"
  title: "CA Globalization Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# CA Globalization Fixes

Agent uses this bundle for culture-sensitive string and formatting operations. When new globalization CA rules appear, agent adds them to Rules Coverage matrix. Agent does not create separate skills for individual CA diagnostics in this category.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Ca Globalization Fixes work | Use this skill |
| Request falls inside the roslyn suite and needs this specific surface | Use this skill |
| The routed catalog needs a single current-state owner for this concern | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is broader than this skill and suite routing is still unclear | Use `roslyn-intake-router` first |
| Request belongs to a narrower specialist than this skill | Use that narrower specialist |
| Request is outside this skill's suite or concern | Use the correct suite router or execution skill |

## Workflow

### 1. Inventory

Agent runs:
```powershell
dotnet build <target> /nologo 2>&1 |
  Select-String -Pattern 'warning (CA1304|CA1305|CA1310|CA1311)' |
  Group-Object { ($_ -split 'warning ')[1].Substring(0,6) } |
  Sort-Object Count -Descending
```
Test: Command completes
Pass: List of CA rules with occurrence counts

### 2. Classify Intent

Agent classifies each occurrence:
- **Invariant culture** — Internal keys, file paths, programmatic identifiers, JSON property names
- **Current culture** — User-visible text, UI display strings
- **Specific culture** — Explicit locale required (rare)

### 3. Apply Fixes

**CA1304/CA1305** — Add CultureInfo parameter:
```csharp
// Before: culture-dependent
var upper = name.ToUpper();
var formatted = value.ToString();

// After: invariant for internal use
var upper = name.ToUpper(CultureInfo.InvariantCulture);
var formatted = value.ToString(CultureInfo.InvariantCulture);

// After: current culture for UI
var upper = name.ToUpper(CultureInfo.CurrentCulture);
var formatted = value.ToString(CultureInfo.CurrentCulture);
```

**CA1310/CA1311** — Add StringComparison:
```csharp
// Before: culture-dependent
if (key.StartsWith("temp"))
if (key.Equals(other))

// After: invariant for internal keys
if (key.StartsWith("temp", StringComparison.OrdinalIgnoreCase))
if (key.Equals(other, StringComparison.Ordinal))

// After: current culture for UI
if (displayName.StartsWith(prefix, StringComparison.CurrentCultureIgnoreCase))
```

### 4. Verify

Agent verifies:
- [ ] `dotnet build` clean, zero new warnings
- [ ] `dotnet test` green for touched projects
- [ ] Invariant culture used for internal/programmatic strings
- [ ] Current culture used for user-visible text
- [ ] String comparisons explicit (Ordinal, OrdinalIgnoreCase, CurrentCulture, etc.)

## Common Pitfalls

| Rule or Area | Pitfall | Fix |
|---|---|---|
| CA1304/CA1305 | Use CurrentCulture for internal keys | Use InvariantCulture for non-UI strings |
| CA1310/CA1311 | Use culture-sensitive comparison for programmatic identifiers | Use Ordinal or OrdinalIgnoreCase |
| All rules | Blanket-suppress without understanding intent | Classify each site as invariant or current-culture first |
| Future rules | Create another micro-skill for one analyzer ID | Extend this bundle instead |

## Rules Coverage

| Rule | Description | Fix | Auto |
|------|-------------|-----|------|
| CA1304 | Specify CultureInfo | Add CultureInfo parameter to culture-sensitive methods | Partial |
| CA1305 | Specify IFormatProvider | Add IFormatProvider parameter to formatting methods | Partial |
| CA1310 | Specify StringComparison for correctness | Add StringComparison parameter to string methods | Yes |
| CA1311 | Specify culture or use invariant version | Use culture-explicit or invariant method overload | Yes |

## Adding New Rules

When new globalization CA rule appears:

Agent performs:
1. Agent verifies rule belongs to culture-sensitive string or formatting operations
2. Agent adds rule to **Rules Coverage** with description, fix pattern, auto-fix availability
3. Agent updates scan regex and examples
4. Agent keeps this bundle as only globalization CA surface. Agent does not create new single-rule skill.

## Overview

Agent handles culture-sensitive string operations, formatting, and comparisons. Agent extends this bundle for future globalization CA diagnostics instead of creating new skills.

## Critical Rules

1. **Invariant culture for internal use** — File paths, JSON keys, database identifiers, programmatic strings
2. **Current culture for UI** — User-visible display text, messages
3. **Ordinal for programmatic comparison** — Dictionary keys, identifiers, non-linguistic matching
4. **Never blanket-suppress** — Inline justification required
5. **Build + test after each batch**

## References

- Rule docs: https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca<id>
- Globalization best practices: https://learn.microsoft.com/dotnet/standard/globalization-localization/

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Project/solution path | Yes | - |
| Rule subset | No | All 4 rules |

## Outputs

Agent produces:
- Explicit culture for all culture-sensitive operations
- InvariantCulture for internal/programmatic strings
- CurrentCulture for user-visible text
- Explicit StringComparison for all string operations
- Justified suppressions where fixes are unsafe
