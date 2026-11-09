---
metadata-version: "1.0.0"
title: "MSTest Warnings Bundle"
description: "Preserve scoped source guidance for mstest-fixes-bundle."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# MSTest Warnings Bundle

Agent uses this bundle for one-pass MSTest analyzer fixes across common warning groups.

## Activation

| Prompt Scope | Use This Bundle | Route Detail |
|---|---|---|
| Several `MSTEST0017`, `MSTEST0042`, `MSTEST0044`, `MSTEST0052`, or `MSTEST0065` warnings | Yes | Agent fixes all listed warnings in one workflow |
| One warning family plus broader test-quality audit | Yes | Agent fixes warnings first, then routes to `test-fixes` |
| New test authoring with no analyzer warnings | No | Agent routes to `mstest-test-authoring` |

## Rules Coverage

| Rule | Defect | Agent Writes | Test | Pass |
|---|---|---|---|---|
| `MSTEST0017` | Outdated MSTest usage | Agent applies the analyzer-approved MSTest pattern at the smallest scope. | Run `dotnet build <target> /nologo`. | Zero `MSTEST0017` warnings in scope. |
| `MSTEST0042` | Non-compliant modern MSTest usage | Agent refactors to the current MSTest pattern expected by the analyzer. | Run `dotnet build <target> /nologo`. | Zero `MSTEST0042` warnings in scope. |
| `MSTEST0044` | Non-compliant test structure or attribute usage | Agent replaces the flagged construct with the compliant MSTest form. | Run `dotnet build <target> /nologo`. | Zero `MSTEST0044` warnings in scope. |
| `MSTEST0052` | Static `TestContext` storage | Agent keeps `TestContext` instance-scoped and passes it to helpers. | Run `rg "static\\s+TestContext" Tests AzureAPI src`. | Zero matches in touched scope. |
| `MSTEST0065` | Obsolete `[DataTestMethod]` usage | Agent replaces `[DataTestMethod]` with `[TestMethod]` patterns and named scenarios. | Run `rg "\\[DataTestMethod\\]" Tests AzureAPI src`. | Zero matches in touched scope. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Baseline warnings | Agent runs a build and captures target warnings. | Run `dotnet build <solution-or-test-project> /nologo 2>&1 \| Select-String -Pattern 'MSTEST(0017\|0042\|0044\|0052\|0065)'`. | Output lists only in-scope warnings. |
| 2. Group by project | Agent groups warnings by project and shared test helpers. | Agent records warning count per project. | Every warning maps to one project. |
| 3. Write smallest fixes | Agent writes the smallest fix for each warning family. | Run `dotnet build <target> /nologo` after each warning family. | Target warning family count drops to zero or documented suppression count. |
| 4. Run tests | Agent runs tests for touched projects. | Run `dotnet test <project-or-solution> --no-build`. | Zero failing tests in touched scope. |

## Rule-Specific Write Matrix

| Rule | Agent Writes | Guardrail |
|---|---|---|
| `MSTEST0017` | Agent uses the analyzer-approved MSTest pattern. | Agent does not suppress the warning. |
| `MSTEST0042` | Agent writes the current MSTest pattern expected by the analyzer. | Agent keeps expected and actual ordering readable. |
| `MSTEST0044` | Agent writes the compliant attribute or structure shape. | Agent keeps tests deterministic. |
| `MSTEST0052` | Agent writes `public TestContext TestContext { get; set; } = null!;` and passes `TestContext` to helpers. | Agent does not write replacement global mutable state. |
| `MSTEST0065` | Agent writes `[TestMethod]` tests with explicit scenario names. | Agent keeps scenario coverage equal or larger. |

## Preferred Pattern

```csharp
public sealed class PayrollTests
{
    public TestContext TestContext { get; set; } = null!;

    [TestMethod]
    public void CalculateTotals_WithWeekendShift_ReturnsExpectedAmount()
    {
        var result = CalculateTotalsForShift(dayOfWeek: DayOfWeek.Saturday);
        Assert.AreEqual(expected: 125m, actual: result.TotalPay);
    }

    private PayrollResult CalculateTotalsForShift(DayOfWeek dayOfWeek)
    {
        return new PayrollResult(totalPay: dayOfWeek == DayOfWeek.Saturday ? 125m : 100m);
    }
}
```

## Verification Matrix

| Scope | Test | Pass |
|---|---|---|
| Warning inventory | Run baseline build filter. | Only targeted warning families appear in the work list. |
| Build health | Run `dotnet build <target> /nologo`. | Zero `MSTEST0017`, `MSTEST0042`, `MSTEST0044`, `MSTEST0052`, and `MSTEST0065` warnings in scope. |
| Test health | Run `dotnet test <project-or-solution> --no-build`. | Zero failing tests in touched scope. |
| `TestContext` scope | Run `rg "static\\s+TestContext" Tests AzureAPI src`. | Zero matches in touched scope. |
| Data-driven rewrite | Run `rg "\\[DataTestMethod\\]" Tests AzureAPI src`. | Zero matches in touched scope. |

## Common Pitfalls

| Pitfall | Safer move |
|---|---|
| Suppressing analyzer warnings | Agent fixes the MSTest construct instead. |
| Replacing one bad global with another | Agent passes `TestContext` explicitly to helpers. |
| Splitting `[DataTestMethod]` rows into vague names | Agent uses explicit scenario names per new `[TestMethod]`. |
| Broad test rewrites | Agent keeps each change local and analyzer-driven. |
