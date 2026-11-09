---
title: C# 14+ Resilience Patterns
doc_type: reference
status: active
last_updated: 2026-08-15
---

# C# 14+ Resilience Patterns

Modern Polly-based resilience patterns using C# 14+ features.

## Primary Constructor with Polly Policies

```csharp
// Service with explicit resilience policies via primary constructor
public class ExternalApiClient(
    HttpClient httpClient,
    IAsyncPolicy<HttpResponseMessage> retryPolicy,
    IAsyncPolicy<HttpResponseMessage> circuitBreakerPolicy,
    ILogger<ExternalApiClient> logger)
{
    public async ValueTask<ApiResponse> GetDataAsync(string id, CancellationToken ct)
    {
        // Combine policies for robust fault handling
        var pipelinePolicy = Policy.WrapAsync(retryPolicy, circuitBreakerPolicy);

        try
        {
            var response = await pipelinePolicy.ExecuteAsync(
                async token => await httpClient.GetAsync($"/api/{id}", token),
                ct);

            response.EnsureSuccessStatusCode();
            var content = await response.Content.ReadAsAsync<ApiResponse>(cancellationToken: ct);
            return content;
        }
        catch (HttpRequestException ex)
        {
            logger.LogError(ex, "API call failed for id {Id}", id);
            throw;
        }
    }
}
```

## File-Scoped Resilience Policy Configuration

```csharp
// Hide internal policy definitions with file scope
file static class ResilientPolicies
{
    internal static IAsyncPolicy<HttpResponseMessage> CreateRetryPolicy() =>
        Policy.Handle<HttpRequestException>()
            .Or<TimeoutRejectedException>()
            .OrResult<HttpResponseMessage>(r => r.StatusCode == HttpStatusCode.ServiceUnavailable)
            .WaitAndRetryAsync(
                retryCount: 3,
                sleepDurationProvider: retryAttempt =>
                    TimeSpan.FromMilliseconds(Math.Pow(2, retryAttempt) * 100),
                onRetry: (outcome, timespan, retryCount, context) =>
                {
                    // Logging handled via ILogger
                });

    internal static IAsyncPolicy<HttpResponseMessage> CreateCircuitBreakerPolicy() =>
        Policy.Handle<HttpRequestException>()
            .OrResult<HttpResponseMessage>(r => !r.IsSuccessStatusCode)
            .CircuitBreakerAsync<HttpResponseMessage>(
                handledEventsAllowedBeforeBreaking: 5,
                durationOfBreak: TimeSpan.FromSeconds(30));
}
```

## Timeout with Cancellation Token Integration

```csharp
// Modern timeout handling with cancellation token
public class ResilientRepository(
    HttpClient httpClient,
    ILogger<ResilientRepository> logger)
{
    public async ValueTask<Entity?> GetByIdAsync(
        int id,
        TimeSpan? timeout = null,
        CancellationToken ct = default)
    {
        var effectiveTimeout = timeout ?? TimeSpan.FromSeconds(5);

        using var cts = CancellationTokenSource.CreateLinkedTokenSource(ct);
        cts.CancelAfter(effectiveTimeout);

        try
        {
            var response = await httpClient.GetAsync($"/entities/{id}", cts.Token);
            if (!response.IsSuccessStatusCode)
            {
                logger.LogWarning("Entity {Id} not found", id);
                return null;
            }

            return await response.Content.ReadAsAsync<Entity>(cancellationToken: cts.Token);
        }
        catch (OperationCanceledException ex)
        {
            logger.LogError(ex, "Timeout while fetching entity {Id}", id);
            throw;
        }
    }
}
```
