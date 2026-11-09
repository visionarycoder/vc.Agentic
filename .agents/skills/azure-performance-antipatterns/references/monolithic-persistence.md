---
title: Monolithic Persistence Anti-Pattern Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: azure-performance-antipatterns
---

# Monolithic Persistence Anti-Pattern

## Description

Using one data store for OLTP, reporting, and analytics workloads that have different latency, indexing, and scaling needs.

## Detection Signals

- Analytics queries hit the OLTP database
- Dashboard aggregations run against transactional tables
- Long-running reports compete with order-entry or API writes
- One schema serves operational data and historical analysis
- Locking, blocking, or replica lag rises during reporting windows

## Why This Is Problematic

- Competing workloads fight for CPU, memory, and I/O
- Indexes drift toward one workload and hurt another
- Query plans shift with mixed access patterns
- Operational latency rises during analytical spikes

## Remediation

**Separate transactional writes from analytical reads:**

```csharp
// ❌ BEFORE: Reporting query hits the transactional store
public async Task<IReadOnlyList<SalesTrendPoint>> GetSalesTrendAsync(
    DateOnly start,
    DateOnly end,
    CancellationToken cancellationToken)
{
    return await _ordersContext.Orders
        .Where(o => o.CreatedOn >= start.ToDateTime(TimeOnly.MinValue) &&
                    o.CreatedOn < end.ToDateTime(TimeOnly.MinValue))
        .GroupBy(o => o.CreatedOn.Date)
        .Select(g => new SalesTrendPoint(g.Key, g.Sum(x => x.Total)))
        .ToListAsync(cancellationToken);
}

// ✅ AFTER: Reporting query uses a dedicated reporting store
public async Task<IReadOnlyList<SalesTrendPoint>> GetSalesTrendAsync(
    DateOnly start,
    DateOnly end,
    CancellationToken cancellationToken)
{
    return await _reportingContext.DailySales
        .Where(x => x.SalesDate >= start && x.SalesDate < end)
        .OrderBy(x => x.SalesDate)
        .Select(x => new SalesTrendPoint(x.SalesDate.ToDateTime(TimeOnly.MinValue), x.TotalSales))
        .ToListAsync(cancellationToken);
}
```

**Register separate data paths:**

```csharp
builder.Services.AddDbContext<OrdersDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Orders")));

builder.Services.AddDbContext<ReportingDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Reporting")));
```

## Verification

Test: Run transactional load with concurrent reporting queries before and after workload separation.
Pass: OLTP latency stays stable during reporting activity. Database waits and lock durations decrease.

## Reference

[Monolithic Persistence Anti-Pattern - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/monolithic-persistence/)
