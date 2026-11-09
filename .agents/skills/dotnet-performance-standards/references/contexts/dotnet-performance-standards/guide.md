---
metadata-version: "1.0.0"
title: ".NET Performance Standards"
description: "Preserve scoped source guidance for dotnet-performance-standards."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# .NET Performance Standards

Agent optimizes measured hot paths first. Agent keeps clarity until measurement data proves that extra complexity pays for itself.

## When to Use

| Condition | Use |
|---|---|
| Measurement data shows allocation, latency, or throughput pressure | Use this skill |
| Agent reviews hot loops, parsers, serializers, or shared helpers | Use this skill |
| Agent compares `class`, `struct`, pooling, spans, or LINQ alternatives | Use this skill |
| Agent hardens generated code that runs at scale | Use this skill |

## When Not to Use

| Condition | Use |
|---|---|
| Code runs infrequently and has no measurement data | Keep simpler code |
| Optimization is speculative | Gather baseline first |
| Task belongs to build or query optimization scope | Route to narrower skill |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Baseline measurement | Yes | Profiler, trace, benchmark, or allocation snapshot |
| Hot-path scope | Yes | Method, loop, parser, mapper, or service path |
| Success metric | Yes | Latency, throughput, allocation count, or GC pressure |
| Compatibility constraint | No | API stability, readability, or framework limit |

## Workflow

Agent follows these steps:

1. Agent records baseline measurement for the target scope.
2. Agent applies the rule matrix from dominant cost to minor cost.
3. Agent keeps each optimization isolated and measurable.
4. Agent reruns the same measurement before accepting the optimization.

Test: Run baseline command before and after change.
Pass: Target metric improves. Correctness stays unchanged.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Clever rewrite happens before measurement | Gather baseline first |
| `ValueTask<T>` becomes default | Use `Task<T>` unless data proves benefit |
| Pooling adds unclear ownership | Keep simpler allocation or add clear ownership |
| LINQ is deleted on principle | Replace only when data shows real cost |

## Rule Matrix

| Rule | Agent verifies | Detection Pattern | Fix |
|---|---|---|---|
| PERF-001 | Hot-path allocations stay minimal | Per-iteration array, list, or object allocation | Reuse buffer, pool object, or move allocation out of loop |
| PERF-002 | Type choice matches data size and copy cost | Tiny immutable data uses heap object or large mutable struct is copied widely | Pick class or struct deliberately |
| PERF-003 | Collections start with useful capacity | Repeated growth in predictable workload | Set initial capacity |
| PERF-004 | String handling avoids repeated churn | Concatenation in loop or repeated casing work | Use `StringBuilder`, `string.Create`, span, or cached normalization |
| PERF-005 | LINQ use is justified on hot path | Multiple enumeration or allocation-heavy chain | Collapse passes or use loop |
| PERF-006 | Async overhead matches measured need | Fake async wrapper or unneeded task churn | Simplify async flow |
| PERF-007 | Boxing is absent on hot path | Value type boxed through interface or non-generic API | Use generic overload or typed collection |
| PERF-008 | Advanced optimization stays evidence-based | Pooling, span, or `ValueTask<T>` added without data | Keep simple code until data exists |

## Optimization Matrix

| Concern | Use | Avoid |
|---|---|---|
| Measurement | Same dataset and environment before and after | Different workload between runs |
| Memory | Localized pooling and clear ownership | Shared pool with unclear lifetime |
| Loops | Simple explicit loop on measured hot path | Multi-pass LINQ chain by habit |
| API shape | Stable external contract | Public contract churn for tiny gain |

## Verification Matrix

| Test | Run | Pass |
|---|---|---|
| Compile verification | `dotnet build [project].csproj` | Zero compile errors |
| Measurement verification | Re-run profiler, benchmark, or trace | Target metric improves |
| Correctness verification | `dotnet test [test-project].csproj` | Zero failing tests |

## Verification Checklist

Agent verifies:
- [ ] Baseline measurement exists
- [ ] Optimization targets dominant cost
- [ ] Target metric improves measurably
- [ ] Correctness and API behavior stay unchanged
- [ ] Added complexity is localized and justified

## C# 14+ Performance Patterns

### Ref Structs and Spans for Zero-Allocation

```csharp
// Use ref structs and ReadOnlySpan<T> for hot paths
public readonly ref struct DataProcessor
{
    private readonly ReadOnlySpan<byte> _buffer;

    public DataProcessor(ReadOnlySpan<byte> buffer)
    {
        _buffer = buffer;
    }

    public int CountMatches(byte value)
    {
        var count = 0;
        foreach (var b in _buffer)
        {
            if (b == value) count++;
        }
        return count;
    }
}
```

### Collection Expressions for Stack-Allocated Arrays

```csharp
// Use collection expressions with Span for efficient allocation
public bool ValidateFields(ReadOnlySpan<string> fields)
{
    // Collection expression creates stackalloc-friendly data
    var requiredFields = ["Name", "Email", "PhoneNumber"];

    foreach (var required in requiredFields)
    {
        if (!fields.Contains(required))
            return false;
    }
    return true;
}
```

### Params Collections with Minimal Allocations

```csharp
// Modern params syntax with Span<T> for zero allocations
public class QueryBuilder
{
    public string BuildInsert(string table, params (string Column, object Value)[] values)
    {
        var sb = new StringBuilder($"INSERT INTO {table} (");

        for (int i = 0; i < values.Length; i++)
        {
            sb.Append(values[i].Column);
            if (i < values.Length - 1) sb.Append(", ");
        }

        sb.Append(") VALUES (");
        for (int i = 0; i < values.Length; i++)
        {
            sb.Append("@p" + i);
            if (i < values.Length - 1) sb.Append(", ");
        }
        sb.Append(")");

        return sb.ToString();
    }
}
```

### File-Scoped High-Performance Helpers

```csharp
// Hide micro-optimized helpers in file scope
file static class BinarySearch
{
    internal static int FindIndex(ReadOnlySpan<int> sorted, int value)
    {
        var left = 0;
        var right = sorted.Length - 1;

        while (left <= right)
        {
            var mid = left + ((right - left) >> 1);  // avoid overflow
            var cmp = sorted[mid].CompareTo(value);

            if (cmp == 0) return mid;
            if (cmp < 0) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
}
```
