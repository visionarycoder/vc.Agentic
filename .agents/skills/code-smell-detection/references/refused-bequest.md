---
title: Refused Bequest Smell Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: code-smell-detection
---

# Refused Bequest Smell

## Description

Derived class inherits behavior or data that it does not use or actively rejects.

## Detection Signals

- Derived class doesn't use base members
- Overridden members throw `NotSupportedException`
- Derived type ignores inherited fields or rules
- Subclass name signals a different responsibility than the base type

## Why This Is Problematic

- Liskov substitution breaks
- Consumers read a false "is-a" relationship
- Base class changes create surprise breakage
- Tests need exceptions for ordinary base operations

## Remediation

Use **Replace Inheritance with Delegation**.

```csharp
// ❌ BEFORE: Subclass rejects inherited write behavior
public abstract class Repository<T>
{
    public abstract Task<T?> GetByIdAsync(Guid id);
    public abstract Task SaveAsync(T item);
    public abstract Task DeleteAsync(Guid id);
}

public sealed class ReadOnlyInvoiceRepository : Repository<Invoice>
{
    public override Task<Invoice?> GetByIdAsync(Guid id) => throw new NotImplementedException();

    public override Task SaveAsync(Invoice item)
        => throw new NotSupportedException("Read-only repository.");

    public override Task DeleteAsync(Guid id)
        => throw new NotSupportedException("Read-only repository.");
}

// ✅ AFTER: Read model uses delegation instead of inheritance
public interface IInvoiceReader
{
    Task<Invoice?> GetByIdAsync(Guid id);
}

public sealed class SqlInvoiceReader : IInvoiceReader
{
    public Task<Invoice?> GetByIdAsync(Guid id) => throw new NotImplementedException();
}

public sealed class ReadOnlyInvoiceStore
{
    private readonly IInvoiceReader _reader;

    public ReadOnlyInvoiceStore(IInvoiceReader reader)
    {
        _reader = reader;
    }

    public Task<Invoice?> GetByIdAsync(Guid id) => _reader.GetByIdAsync(id);
}
```

## Verification

Test: Inspect subclass overrides and inheritance tree before and after refactoring.
Pass: Rejected inherited operations disappear. Public API matches actual responsibility. Tests pass.

## Reference

[Refused Bequest - Refactoring Guru](https://refactoring.guru/smells/refused-bequest)
