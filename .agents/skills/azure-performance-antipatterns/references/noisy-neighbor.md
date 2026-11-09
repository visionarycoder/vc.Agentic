---
title: Noisy Neighbor Anti-Pattern Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: azure-performance-antipatterns
---

# Noisy Neighbor Anti-Pattern

## Description

Allowing one tenant or workload to consume shared capacity without partitioning, quotas, or isolation.

## Detection Signals

- Single tenant consumes disproportionate resources
- One tenant drives most CPU, queue depth, or database throughput
- Shared worker pool serves tenants without partitioning
- Burst traffic from one account degrades latency for other accounts
- Resource starvation appears in shared caches, queues, or partitions

## Why This Is Problematic

- Small tenant counts hide fairness defects until a burst arrives
- Shared capacity collapses around one hot partition
- SLOs fail for healthy tenants
- Support and billing disputes increase

## Remediation

**Apply per-tenant rate limits:**

```csharp
// ❌ BEFORE: Global limiter lets one tenant consume shared capacity
builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = new ConcurrencyLimiter(new ConcurrencyLimiterOptions
    {
        PermitLimit = 200,
        QueueLimit = 500
    });
});

// ✅ AFTER: Partition permits by tenant
builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(context =>
    {
        string tenantId = context.User.FindFirst("tenant_id")?.Value ?? "anonymous";

        return RateLimitPartition.GetConcurrencyLimiter(tenantId, _ => new ConcurrencyLimiterOptions
        {
            PermitLimit = 20,
            QueueLimit = 40
        });
    });
});
```

**Partition background work:**

```csharp
// ✅ AFTER: Partition queue selection by tenant
string queueName = $"exports-{tenantId}";
await _queueRouter.EnqueueAsync(queueName, job, cancellationToken);
```

## Verification

Test: Generate burst traffic from one tenant while steady traffic runs from several other tenants.
Pass: Burst traffic hits tenant-local limits. Latency and throughput for other tenants stay stable.

## Reference

[Noisy Neighbor Anti-Pattern - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/noisy-neighbor/)
