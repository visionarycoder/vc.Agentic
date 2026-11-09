---
title: Primitive Obsession Smell Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: code-smell-detection
---

# Primitive Obsession Smell

## Description

Code models domain concepts with primitives instead of dedicated types.

## Detection Signals

- Primitive for domain concept
- Repeated validation for the same string, number, or date
- Method signatures pass raw identifiers, money, or status values
- Conditional logic decodes primitive state across many files

## Why This Is Problematic

- Domain rules scatter across the codebase
- Invalid values enter the system easily
- Signatures hide meaning
- Refactoring pressure rises when the concept gains behavior

## Remediation

Use **Replace Data Value with Object**.

```csharp
// ❌ BEFORE: Email lives as a raw string everywhere
public sealed class CustomerService
{
    public Task RegisterAsync(string fullName, string email)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(fullName);

        if (string.IsNullOrWhiteSpace(email) || !email.Contains('@'))
        {
            throw new ArgumentException("Invalid email.", nameof(email));
        }

        return Task.CompletedTask;
    }
}

// ✅ AFTER: Value object owns the rule and meaning
public sealed record EmailAddress
{
    public string Value { get; }

    public EmailAddress(string value)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(value);

        var trimmed = value.Trim();
        if (!trimmed.Contains('@'))
        {
            throw new ArgumentException("Invalid email.", nameof(value));
        }

        Value = trimmed;
    }

    public override string ToString() => Value;
}

public sealed class CustomerService
{
    public Task RegisterAsync(string fullName, EmailAddress email)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(fullName);
        ArgumentNullException.ThrowIfNull(email);
        return Task.CompletedTask;
    }
}
```

## Verification

Test: Search for repeated primitive validation and raw domain values before and after extraction.
Pass: Domain concept uses a dedicated type. Repeated validation code disappears. Tests pass.

## Reference

[Primitive Obsession - Refactoring Guru](https://refactoring.guru/smells/primitive-obsession)
