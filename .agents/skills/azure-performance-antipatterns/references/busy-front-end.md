---
title: Busy Front End Anti-Pattern Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: azure-performance-antipatterns
---

# Busy Front End Anti-Pattern

## Description

Running CPU-intensive work on the request thread instead of offloading the work to a background path or a precomputed asset.

## Detection Signals

- Request method performs CPU-intensive computation
- Request handler renders images, PDFs, or reports inline
- Large compression, encryption, or serialization step runs on the request thread
- Thread pool exhaustion appears during request bursts
- Response time rises with CPU even when I/O remains low

## Why This Is Problematic

- Request threads stay busy for long intervals
- Thread pool growth lags behind demand
- Queue length rises during traffic bursts
- CPU hotspots reduce throughput for every request

## Remediation

**Move heavy work to a background queue:**

```csharp
// ❌ BEFORE: CPU-intensive work runs on the request thread
app.MapPost("/reports/{id:guid}/render", async (
    Guid id,
    ReportRenderer renderer,
    CancellationToken cancellationToken) =>
{
    byte[] pdf = await renderer.RenderPdfAsync(id, cancellationToken);
    return Results.File(pdf, "application/pdf", $"{id}.pdf");
});

// ✅ AFTER: Request enqueues work and returns immediately
app.MapPost("/reports/{id:guid}/render", async (
    Guid id,
    IBackgroundTaskQueue queue,
    CancellationToken cancellationToken) =>
{
    await queue.EnqueueAsync(new RenderReportJob(id), cancellationToken);
    return Results.Accepted($"/reports/{id}/status");
});
```

**Use a background service for the CPU path:**

```csharp
public sealed class ReportRenderWorker(
    IBackgroundTaskQueue queue,
    ReportRenderer renderer,
    ILogger<ReportRenderWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (RenderReportJob job in queue.DequeueAsync(stoppingToken))
        {
            byte[] pdf = await renderer.RenderPdfAsync(job.ReportId, stoppingToken);
            logger.LogInformation("Rendered report {ReportId} with {Length} bytes.", job.ReportId, pdf.Length);
        }
    }
}
```

## Verification

Test: Load test the endpoint before and after the queue-based path.
Pass: Request latency drops during CPU-heavy workloads. Thread pool queue length and active request duration decrease.

## Reference

[Busy Front End Anti-Pattern - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/busy-front-end/)
