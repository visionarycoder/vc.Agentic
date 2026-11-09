---
title: Shotgun Surgery Smell Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: code-smell-detection
---

# Shotgun Surgery Smell

## Description

One business change forces edits across many classes, methods, or modules.

## Detection Signals

- Change requires edits to >5 classes
- Same business rule appears in multiple services
- Parallel updates occur in handlers, mappers, validators, and reports
- Release notes often group the same files for one feature change

## Why This Is Problematic

- Small rule updates consume large effort
- Partial edits create inconsistent behavior
- Merge conflicts increase
- Change review scope grows beyond one responsibility

## Remediation

Use **Move Method** or **Move Field** to gather the rule in one place.

```csharp
// ❌ BEFORE: Tax rule lives in several classes
public sealed class OrderPricer
{
    public decimal CalculateTotal(decimal subtotal) => subtotal + (subtotal * 0.0825m);
}

public sealed class InvoicePricer
{
    public decimal CalculateTotal(decimal subtotal) => subtotal + (subtotal * 0.0825m);
}

public sealed class QuotePricer
{
    public decimal CalculateTotal(decimal subtotal) => subtotal + (subtotal * 0.0825m);
}

// ✅ AFTER: Shared policy owns the rule
public sealed class TaxPolicy
{
    private const decimal SalesTaxRate = 0.0825m;

    public decimal ApplySalesTax(decimal subtotal) => subtotal + (subtotal * SalesTaxRate);
}

public sealed class OrderPricer
{
    private readonly TaxPolicy _taxPolicy;

    public OrderPricer(TaxPolicy taxPolicy)
    {
        _taxPolicy = taxPolicy;
    }

    public decimal CalculateTotal(decimal subtotal) => _taxPolicy.ApplySalesTax(subtotal);
}

public sealed class InvoicePricer
{
    private readonly TaxPolicy _taxPolicy;

    public InvoicePricer(TaxPolicy taxPolicy)
    {
        _taxPolicy = taxPolicy;
    }

    public decimal CalculateTotal(decimal subtotal) => _taxPolicy.ApplySalesTax(subtotal);
}
```

## Verification

Test: Trace one business rule change through the affected files before and after consolidation.
Pass: One component owns the shared rule. Future edits touch one place. Tests pass.

## Reference

[Shotgun Surgery - Refactoring Guru](https://refactoring.guru/smells/shotgun-surgery)
