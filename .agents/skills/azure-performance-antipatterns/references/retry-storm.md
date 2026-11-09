---
title: Retry Storm Anti-Pattern Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: azure-performance-antipatterns
---

# Retry Storm Anti-Pattern

## Description

Flooding a failing dependency with immediate or layered retries that multiply traffic during an outage.

## Detection Signals

- Retry policy has no exponential backoff or circuit breaker
- Multiple application layers retry the same dependency
- Immediate retries fire on timeouts or 5xx responses
- Outbound request count spikes when the upstream service slows down
- Recovery time lengthens after a transient failure starts

## Why This Is Problematic

- Failing services receive more load at the worst moment
- Queues and socket pools fill with duplicate work
- Latency expands across the full call graph
- Recovery slows because fresh requests compete with retries

## Remediation

**Replace manual loops with bounded resiliency policies:**

```csharp
// ❌ BEFORE: Immediate retries with no backoff or breaker
for (int attempt = 0; attempt < 5; attempt++)
{
    HttpResponseMessage response = await _client.GetAsync("/inventory", cancellationToken);
    if (response.IsSuccessStatusCode)
    {
        return await response.Content.ReadFromJsonAsync<InventoryDto>(cancellationToken: cancellationToken);
    }
}

throw new HttpRequestException("Inventory request failed.");
```

```csharp
// ✅ AFTER: Polly adds exponential backoff and a circuit breaker
IAsyncPolicy<HttpResponseMessage> retryPolicy =
    HttpPolicyExtensions
        .HandleTransientHttpError()
        .WaitAndRetryAsync(3, attempt => TimeSpan.FromMilliseconds(200 * Math.Pow(2, attempt)));

IAsyncPolicy<HttpResponseMessage> circuitBreakerPolicy =
    HttpPolicyExtensions
        .HandleTransientHttpError()
        .CircuitBreakerAsync(5, TimeSpan.FromSeconds(30));

builder.Services.AddHttpClient<InventoryClient>(client =>
    client.BaseAddress = new Uri("https://inventory"))
    .AddPolicyHandler(Policy.WrapAsync(retryPolicy, circuitBreakerPolicy));
```

## Verification

Test: Inject 5xx and timeout faults in the downstream dependency during a load test.
Pass: Outbound retries stay bounded. Request rate to the failing service drops after the breaker opens.

## Reference

[Retry Storm Anti-Pattern - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/retry-storm/)
