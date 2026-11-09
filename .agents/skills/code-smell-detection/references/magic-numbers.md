---
title: Magic Numbers Smell Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: code-smell-detection
---

# Magic Numbers Smell

## Description

Unexplained numeric or string literals appear in logic without a named meaning.

## Detection Signals

- Unexplained numeric literal
- Repeated thresholds, offsets, or retry counts
- Inline percentages, tax rates, or status codes
- Literal values that need comments for meaning

## Why This Is Problematic

- Business meaning stays hidden
- Rule changes require manual search
- Duplicate values drift apart
- Reviewers read numbers instead of intent

## Remediation

Use **Replace Magic Number with Symbolic Constant**.

```csharp
// ❌ BEFORE: Literals hide business rules
public sealed class CheckoutPolicy
{
    public decimal CalculateDiscount(int loyaltyPoints, decimal orderTotal)
    {
        if (loyaltyPoints >= 2500 && orderTotal >= 500m)
        {
            return orderTotal * 0.15m;
        }

        if (loyaltyPoints >= 1000)
        {
            return orderTotal * 0.05m;
        }

        return 0m;
    }
}

// ✅ AFTER: Named constants expose intent
public sealed class CheckoutPolicy
{
    private const int GoldPointsThreshold = 2500;
    private const int SilverPointsThreshold = 1000;
    private const decimal GoldDiscountRate = 0.15m;
    private const decimal SilverDiscountRate = 0.05m;
    private const decimal GoldOrderMinimum = 500m;

    public decimal CalculateDiscount(int loyaltyPoints, decimal orderTotal)
    {
        if (loyaltyPoints >= GoldPointsThreshold && orderTotal >= GoldOrderMinimum)
        {
            return orderTotal * GoldDiscountRate;
        }

        if (loyaltyPoints >= SilverPointsThreshold)
        {
            return orderTotal * SilverDiscountRate;
        }

        return 0m;
    }
}
```

## Verification

Test: Search for repeated unnamed literals in the target rule before and after extraction.
Pass: Domain literals move to named constants or value types. Callers read intent without comments. Tests pass.

## Reference

[Magic number (programming) - Wikipedia](https://en.wikipedia.org/wiki/Magic_number_(programming))
