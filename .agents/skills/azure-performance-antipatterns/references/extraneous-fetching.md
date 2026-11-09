---
title: Extraneous Fetching Anti-Pattern Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: azure-performance-antipatterns
---

# Extraneous Fetching Anti-Pattern

## Description

Retrieving more rows, columns, or related objects than the operation uses.

## Detection Signals

- Query returns all columns when a subset fits the operation
- Entity query materializes full aggregates for list screens
- `Include` loads large related graphs that the response ignores
- API returns large payloads when callers read only summary fields
- Blob or document content loads with metadata queries

## Why This Is Problematic

- Database reads transfer excess data
- Memory usage rises during materialization
- Serialization cost rises with payload size
- Cache entries waste space on unused fields

## Remediation

**Project only the fields that the operation uses:**

```csharp
// ❌ BEFORE: Full entity graph for a summary view
var orders = await _context.Orders
    .Include(o => o.Customer)
    .Include(o => o.Lines)
    .ToListAsync(cancellationToken);

return orders.Select(o => new OrderSummaryDto(
    o.Id,
    o.Customer.Name,
    o.Status,
    o.Lines.Count));

// ✅ AFTER: Server-side projection
var orders = await _context.Orders
    .AsNoTracking()
    .Select(o => new OrderSummaryDto(
        o.Id,
        o.Customer.Name,
        o.Status,
        o.Lines.Count))
    .ToListAsync(cancellationToken);

return orders;
```

**Split metadata from large content:**

```csharp
// ❌ BEFORE: Reads document body for list page
var documents = await _context.Documents
    .AsNoTracking()
    .ToListAsync(cancellationToken);

// ✅ AFTER: Metadata query for the list page
var documents = await _context.Documents
    .AsNoTracking()
    .Select(d => new DocumentListItemDto(d.Id, d.Title, d.LastModifiedUtc))
    .ToListAsync(cancellationToken);
```

## Verification

Test: Compare SQL text, payload size, and allocated bytes before and after projection.
Pass: Result set width or row count decreases. Endpoint latency and memory allocation decrease.

## Reference

[Extraneous Fetching Anti-Pattern - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/extraneous-fetching/)
