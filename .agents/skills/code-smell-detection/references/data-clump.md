---
title: Data Clump Smell Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: code-smell-detection
---

# Data Clump Smell

## Description

Same group of variables appears together across methods, constructors, or classes.

## Detection Signals

- Same 3+ variables passed together
- Repeated address, date range, or contact field groups
- Multiple overloads that repeat the same variable set
- Validation logic repeated for the same variable group

## Why This Is Problematic

- Hidden domain concept stays unnamed
- Parameter order defects enter call sites
- Validation logic spreads across the codebase
- Changes touch many signatures

## Remediation

Use **Introduce Value Object**.

```csharp
// ❌ BEFORE: Address fields travel together through multiple methods
public sealed class ShipmentService
{
    public Shipment CreateShipment(
        string recipientName,
        string street,
        string city,
        string state,
        string postalCode,
        string country)
    {
        ValidateAddress(street, city, state, postalCode, country);

        return new Shipment
        {
            RecipientName = recipientName,
            Street = street,
            City = city,
            State = state,
            PostalCode = postalCode,
            Country = country
        };
    }

    private static void ValidateAddress(
        string street,
        string city,
        string state,
        string postalCode,
        string country)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(street);
        ArgumentException.ThrowIfNullOrWhiteSpace(city);
        ArgumentException.ThrowIfNullOrWhiteSpace(state);
        ArgumentException.ThrowIfNullOrWhiteSpace(postalCode);
        ArgumentException.ThrowIfNullOrWhiteSpace(country);
    }
}

// ✅ AFTER: Value object carries the grouped data
public sealed record PostalAddress
{
    public string Street { get; }
    public string City { get; }
    public string State { get; }
    public string PostalCode { get; }
    public string Country { get; }

    public PostalAddress(
        string street,
        string city,
        string state,
        string postalCode,
        string country)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(street);
        ArgumentException.ThrowIfNullOrWhiteSpace(city);
        ArgumentException.ThrowIfNullOrWhiteSpace(state);
        ArgumentException.ThrowIfNullOrWhiteSpace(postalCode);
        ArgumentException.ThrowIfNullOrWhiteSpace(country);

        Street = street.Trim();
        City = city.Trim();
        State = state.Trim();
        PostalCode = postalCode.Trim();
        Country = country.Trim();
    }
}

public sealed class ShipmentService
{
    public Shipment CreateShipment(string recipientName, PostalAddress address)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(recipientName);
        ArgumentNullException.ThrowIfNull(address);

        return new Shipment
        {
            RecipientName = recipientName,
            Street = address.Street,
            City = address.City,
            State = address.State,
            PostalCode = address.PostalCode,
            Country = address.Country
        };
    }
}
```

## Verification

Test: Search for repeated variable groups in signatures before and after extraction.
Pass: One value object replaces repeated field groups. Repeated validation logic disappears. Tests pass.

## Reference

[Data Clumps - Refactoring Guru](https://refactoring.guru/smells/data-clumps)
