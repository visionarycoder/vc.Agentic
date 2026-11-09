---
title: Feature Envy Smell Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: code-smell-detection
---

# Feature Envy Smell

## Description

Method works more with another class's data than with its own data.

## Detection Signals

- Method uses >3 fields from another class
- Method chains through another object for most decisions
- Caller reads foreign state, then applies foreign business rules
- Same foreign data access pattern appears in related methods

## Why This Is Problematic

- Responsibility sits in the wrong class
- Encapsulation breaks
- Changes to foreign data shape ripple outward
- Unit tests need extra setup for unrelated collaborators

## Remediation

Use **Move Method to owner class**.

```csharp
// ❌ BEFORE: Service method uses Customer data heavily
public sealed class LoyaltyService
{
    public string GetTierLabel(Customer customer)
    {
        ArgumentNullException.ThrowIfNull(customer);

        if (customer.PointBalance >= 5000 &&
            customer.LastPurchaseUtc >= DateTime.UtcNow.AddDays(-30) &&
            customer.TotalSpend >= 10000m &&
            customer.IsPreferred)
        {
            return "Platinum";
        }

        if (customer.PointBalance >= 2000 && customer.TotalSpend >= 3000m)
        {
            return "Gold";
        }

        return "Standard";
    }
}

// ✅ AFTER: Customer owns the tier rule
public sealed class Customer
{
    public required int PointBalance { get; init; }
    public required DateTime LastPurchaseUtc { get; init; }
    public required decimal TotalSpend { get; init; }
    public required bool IsPreferred { get; init; }

    public string GetTierLabel(DateTime utcNow)
    {
        if (PointBalance >= 5000 &&
            LastPurchaseUtc >= utcNow.AddDays(-30) &&
            TotalSpend >= 10000m &&
            IsPreferred)
        {
            return "Platinum";
        }

        if (PointBalance >= 2000 && TotalSpend >= 3000m)
        {
            return "Gold";
        }

        return "Standard";
    }
}

public sealed class LoyaltyService
{
    public string GetTierLabel(Customer customer, DateTime utcNow)
    {
        ArgumentNullException.ThrowIfNull(customer);
        return customer.GetTierLabel(utcNow);
    }
}
```

## Verification

Test: Count foreign field accesses in the original method and in the moved design.
Pass: Foreign field access count drops in the caller. Business rule lives with the owning data. Tests pass.

## Reference

[Feature Envy - Refactoring Guru](https://refactoring.guru/smells/feature-envy)
