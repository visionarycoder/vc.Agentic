---
name: "rate-limiting-aspnetcore"
description: "Configure ASP.NET Core rate limiting with fixed or sliding windows, token buckets, concurrency limits, and custom policies."
metadata:
  metadata-version: "1.0.0"
  title: "ASP.NET Core Rate Limiting"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# ASP.NET Core Rate Limiting

Configure ASP.NET Core request throttling with the built-in .NET 7+ rate limiting middleware.

## When to Use

Use for per-client or per-user quotas, burst control, downstream concurrency protection, or endpoint-specific throttling. Do not use when a gateway owns all throttling, for background-processing backpressure, or outside ASP.NET Core .NET 7+.

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Partition key | Yes | Select client IP, API key, user ID, tenant ID, or route group. |
| Limiter type | Yes | Select fixed window, sliding window, token bucket, concurrency, or custom policy. |
| Rejection contract | Yes | Define status code, body shape, and retry headers. |
| Endpoint scope | No | Record global, route-group, or endpoint-level application. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1 | Select the partition key and limiter type from traffic shape and fairness goals. | Read the startup registration and endpoint scope. | One explicit partition key and limiter type exist for each protected path. |
| 2 | Agent registers `AddRateLimiter()` with named policies. | Run `rg -n "AddRateLimiter|AddFixedWindowLimiter|AddSlidingWindowLimiter|AddTokenBucketLimiter|AddConcurrencyLimiter" <scope>`. | Service registration contains the intended named policies. |
| 3 | Agent wires `UseRateLimiter()` into the pipeline and maps policies to endpoints or groups. | Read `Program.cs`. | Middleware registration and endpoint policy mapping both exist. |
| 4 | Return a stable rejection response with `429` and retry metadata when applicable. | Inspect `OnRejected` and call a throttled endpoint. | Rejected requests return the intended contract. |
| 5 | Agent excludes health or infrastructure endpoints when prompt scope calls for exemption. | Read endpoint metadata. | Exempt endpoints do not use the throttling policy. |
| 6 | Agent runs targeted request bursts and concurrency checks. | Run existing API tests or scripted HTTP calls. | Allowed requests pass, excess requests fail with the intended result. |

## Implementation Patterns

```csharp
using System.Globalization;
using System.Threading.RateLimiting;

builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
    options.OnRejected = async (context, cancellationToken) =>
    {
        if (context.Lease.TryGetMetadata(MetadataName.RetryAfter, out var retryAfter))
        {
            context.HttpContext.Response.Headers.RetryAfter = ((int)retryAfter.TotalSeconds).ToString(CultureInfo.InvariantCulture);
        }

        await context.HttpContext.Response.WriteAsJsonAsync(new { title = "Too Many Requests", status = 429 }, cancellationToken);
    };

    options.AddPolicy("per-user", httpContext =>
        RateLimitPartition.GetTokenBucketLimiter(
            httpContext.User.Identity?.Name ?? httpContext.Connection.RemoteIpAddress?.ToString() ?? "anonymous",
            _ => new TokenBucketRateLimiterOptions
            {
                TokenLimit = 50,
                TokensPerPeriod = 10,
                ReplenishmentPeriod = TimeSpan.FromSeconds(30),
                QueueLimit = 0,
                AutoReplenishment = true
            }));
});

app.UseRateLimiter();
app.MapGet("/health/live", () => Results.Ok()).DisableRateLimiting();
app.MapGroup("/api/orders").RequireRateLimiting("per-user");
```

## Rules

| Rule | Agent Verifies | Fix |
|---|---|---|
| RL-001 | Partition key maps to the fairness boundary the prompt describes. | Change the partition to user, tenant, API key, or route group. |
| RL-002 | Authenticated quotas do not collapse all callers into one anonymous bucket after sign-in. | Move authenticated policies after authentication and use user or tenant identity. |
| RL-003 | IP-based limits behind proxies read the forwarded client IP safely. | Configure forwarded headers before IP-based partition logic. |
| RL-004 | Rejected requests return `429` with stable body shape and retry metadata when available. | Add `OnRejected` and `Retry-After` handling. |
| RL-005 | Queue limits stay bounded for latency-sensitive endpoints. | Set `QueueLimit` to zero or a small explicit value. |
| RL-006 | Health and infrastructure endpoints stay exempt when the scope calls for it. | Add `DisableRateLimiting()` or map a separate policy. |

## Outputs

- Named policies for the requested traffic shape
- Ordered middleware registration with endpoint mappings
- Stable `429` rejection contract with retry metadata
- Verification evidence for quota, burst, and concurrency behavior
