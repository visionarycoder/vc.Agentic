---
metadata-version: "1.0.0"
title: ".NET Immutability Standards"
description: "Preserve scoped source guidance for dotnet-immutability-standards."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# .NET Immutability Standards

Agent uses immutable design for state-carrying types unless real mutation is required. Agent keeps hidden state changes out of DTO, event, and value-oriented models.

## When to Use

| Condition | Use |
|---|---|
| Agent defines DTOs, value objects, messages, events, or options models | Use this skill |
| Agent reviews mutable properties, fields, or collection exposure | Use this skill |
| Agent chooses between record, sealed class, or readonly struct | Use this skill |
| Agent refactors state carriers for concurrency or caching safety | Use this skill |

## When Not to Use

| Condition | Use |
|---|---|
| Type is ORM entity with lifecycle mutation | Preserve controlled mutation |
| Type is builder used during construction | Keep builder mutable |
| Low-level interop or performance scope requires mutation | Use explicit mutable design |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Type role | Yes | DTO, event, value object, options model, or entity |
| Mutation need | Yes | Whether any member changes after construction |
| Collection ownership | Yes | Whether nested collections are copied, wrapped, or exposed |
| Framework constraint | No | Serializer, binder, or ORM rule that limits shape choice |

## Workflow

Agent follows these steps:

1. Agent classifies type as state carrier or lifecycle-driven type.
2. Agent selects immutable shape first for state carriers.
3. Agent applies the rule matrix to fields, collections, equality, and copy behavior.
4. Agent verifies framework compatibility without opening broad mutation paths.

Test: Run `dotnet build [project].csproj`.
Pass: Zero compile errors. Zero mutable collection leaks in changed scope.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Readonly reference points to mutable nested object | Copy or wrap nested object |
| Serializer convenience adds open setters | Use constructor or converter when available |
| Lifecycle-driven entity gets blanket immutability | Preserve controlled mutation |
| Internal collection is returned directly | Return readonly wrapper or copy |

## Rule Matrix

| Rule | Agent verifies | Detection Pattern | Fix |
|---|---|---|---|
| IMM-001 | State carriers use immutable shape by default | DTO or event with mutable public setters | Use record or init-only sealed class |
| IMM-002 | Stable fields are readonly | Constructor-assigned field stays reassignable | Mark field readonly |
| IMM-003 | Mutable collections are not exposed directly | Public `List<T>`, `Dictionary<TKey,TValue>`, or array leak | Expose readonly wrapper or defensive copy |
| IMM-004 | Real mutation stays explicit | Ad hoc setter calls across callers | Route mutation through focused method or builder |
| IMM-005 | Value semantics use value-oriented type | Equality-sensitive data uses mutable reference bag | Use record, record struct, or readonly struct |
| IMM-006 | Normalization happens once at construction | Repeated casing or trim logic across callers | Normalize in constructor or factory |
| IMM-007 | Nested state is truly immutable | Readonly property points to mutable object | Copy or wrap nested object |
| IMM-008 | Mutable exceptions stay documented | Serializer or ORM convenience opens public mutation | Isolate and document exception |

## Type Matrix

| Scenario | Use |
|---|---|
| DTO or event payload | Record or sealed class with init-only properties |
| Small value-oriented type | Readonly struct or record struct |
| Options snapshot after binding | Immutable model after bind step |
| ORM entity | Controlled mutable type |

## Verification Matrix

| Test | Run | Pass |
|---|---|---|
| Compile verification | `dotnet build [project].csproj` | Zero compile errors |
| Behavior verification | `dotnet test [test-project].csproj --filter Immutability` when tests exist | Zero failing tests |
| Collection scan verification | Search changed files for public mutable collections | Zero matches in changed scope unless documented |

## Verification Checklist

Agent verifies:
- [ ] State carriers use immutable shape by default
- [ ] Stable fields are readonly
- [ ] Collections do not leak mutable ownership
- [ ] Equality semantics match type role
- [ ] Mutable exceptions are explicit and documented

## C# 14+ Immutability Patterns

### Required Record Members with Init-Only Properties

```csharp
// Modern DTO with record and required fields
public record CreateOrderRequest(
    required int CustomerId,
    required string OrderNumber,
    required decimal Amount)
{
    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;
}

// Ensure immutability after construction
var request = new CreateOrderRequest(
    CustomerId: 123,
    OrderNumber: "ORD-2024-001",
    Amount: 99.99
);

// Cannot mutate after creation
// request.Amount = 50.00;  // compile error
```

### File-Scoped Immutable Value Objects

```csharp
// Hide internal value-object implementation with file scope
file record CachedValue<T>(
    required T Value,
    required DateTime ExpiresAt,
    required string CacheKey) : IEquatable<CachedValue<T>>
{
    public bool IsExpired => DateTime.UtcNow > ExpiresAt;
}

// Use safely with immutable contract
public CachedValue<Order>? GetOrder(int id) =>
    _cache.GetOrCreateAsync(id, async ct =>
        new CachedValue<Order>(
            Value: await _repo.GetAsync(id, ct),
            ExpiresAt: DateTime.UtcNow.AddMinutes(5),
            CacheKey: $"order-{id}"
        )
    );
```

### Collection Expression for Immutable Collections

```csharp
// Use collection expressions for efficient immutable data
public record OrderSummary(
    required int OrderId,
    required string CustomerName,
    required decimal Total)
{
    // C# 14 collection expression for immutable list initialization
    public IReadOnlyList<string> LineItems { get; init; } = [];
}

// Initialize with collection expression
var summary = new OrderSummary(
    OrderId: 1,
    CustomerName: "Acme Corp",
    Total: 500.00)
{
    LineItems = ["Item A", "Item B", "Item C"]
};
```

### Primary Constructor with Immutable Dependencies

```csharp
// Service using immutable dependencies via primary constructor
public class OrderService(
    IOrderRepository repo,
    ImmutableList<IOrderValidator> validators)
{
    public async ValueTask<Order> ProcessAsync(Order order, CancellationToken ct)
    {
        // Validators collection is immutable and thread-safe
        var errors = new List<string>();

        foreach (var validator in validators)
        {
            var result = await validator.ValidateAsync(order, ct);
            if (!result.IsValid)
            {
                errors.AddRange(result.Errors);
            }
        }

        if (errors.Count > 0)
            throw new ValidationException(string.Join("; ", errors));

        return await repo.SaveAsync(order, ct);
    }
}
```
