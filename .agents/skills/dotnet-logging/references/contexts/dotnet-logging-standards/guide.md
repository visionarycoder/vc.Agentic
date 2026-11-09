---
metadata-version: "1.0.0"
title: ".NET Logging Standards"
description: "Preserve scoped source guidance for dotnet-logging."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# .NET Logging Standards

Agent keeps logs structured, searchable, correlation-friendly, and safe. Agent writes logs that help operators without leaking secrets or generating noise.

## When to Use

| Condition | Use |
|---|---|
| Agent adds or reviews logging in any .NET layer | Use this skill |
| Agent converts interpolated logs to structured templates | Use this skill |
| Agent standardizes correlation IDs or telemetry-enriched logs | Use this skill |
| Agent reviews sensitive-data exposure or log-level drift | Use this skill |

## When Not to Use

| Condition | Use |
|---|---|
| Log line is temporary local debugging | Delete log line before completion |
| Task changes only metrics or spans | Route to telemetry skill |
| Task designs user-facing error text | Route to API or UX contract skill |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Workflow scope | Yes | Request, batch job, command handler, or background service |
| Failure modes | Yes | Warning and error outcomes operators need |
| Sensitive fields | Yes | Secret, token, PII, or payload data to omit or redact |
| Correlation key | No | Trace ID, request ID, job ID, or domain key |

## Workflow

Agent follows these steps:

1. Agent selects operator-facing events for the workflow.
2. Agent applies the rule matrix to message templates, property names, and levels.
3. Agent routes correlation keys through scopes and downstream calls.
4. Agent verifies redaction and noise level before completion.

Test: Run `dotnet build [project].csproj`.
Pass: Zero compile errors. Zero interpolated logging defects in changed scope.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Whole request object is logged by habit | Log only needed fields |
| Same exception is logged at every layer | Log once at owning layer |
| One identifier uses many property names | Reuse one property name |
| Debug chatter becomes permanent | Keep only durable operator-facing logs |

## Rule Matrix

| Rule | Agent verifies | Detection Pattern | Fix |
|---|---|---|---|
| LOG-001 | `ILogger` placement stays predictable | Mixed constructor or method parameter order | Use repository parameter order |
| LOG-002 | Repeated logs use `LoggerMessage` source generation | Copy-pasted templates across files | Route to generated logging helper |
| LOG-003 | Logs use structured templates | String interpolation or concatenation in log call | Use template with named properties |
| LOG-004 | Correlation flows through scopes and downstream calls | Log lines cannot route to request or activity | Add scope or correlation properties |
| LOG-005 | Sensitive values stay omitted or redacted | Secret, token, PII, or full payload in log | Omit, hash, or sanitize value |
| LOG-006 | Level matches operator action | Error log for expected outcome or information log for chatter | Lower or raise level to match action |
| LOG-007 | Expensive payload generation stays guarded | Serialization or formatting on disabled level | Guard with `IsEnabled` |
| LOG-008 | Event names and properties stay stable | Same event uses different text or property names | Reuse one event contract |

## Pattern Matrix

| Concern | Use | Avoid |
|---|---|---|
| Message text | Short operator-facing text | Raw payload dump |
| Properties | Stable named properties | Positional or unnamed data |
| Failure logging | One owning layer logs recovery decision | Same exception logged at every layer |
| Correlation | Scope plus trace or request key | Ad hoc identifiers per file |

## Verification Matrix

| Test | Run | Pass |
|---|---|---|
| Compile verification | `dotnet build [project].csproj` | Zero compile errors |
| Logging behavior verification | `dotnet test [test-project].csproj --filter Logging` when tests exist | Zero failing tests |
| Template scan verification | Search changed files for `$"` inside logger calls | Zero matches in changed scope |

## Verification Checklist

Agent verifies:
- [ ] Logs use structured templates
- [ ] Sensitive values stay omitted or redacted
- [ ] Correlation data is present
- [ ] Log level matches operator action
- [ ] Expensive payload generation is guarded when needed
- [ ] Repeated events use stable names and properties

## C# 14+ Logging Patterns (.NET 10)

Agent uses modern language features in structured logging implementations.

### Primary Constructor with Typed Logger

```csharp
// Service with structured logging via primary constructor
public class OrderProcessor(
    IOrderRepository repo,
    ILogger<OrderProcessor> logger)
{
    public async ValueTask ProcessAsync(Order order, CancellationToken ct)
    {
        // Structured logging with typed properties
        using (logger.BeginScope(new Dictionary<string, object>
        {
            ["OrderId"] = order.Id,
            ["CustomerId"] = order.CustomerId,
            ["Amount"] = order.TotalAmount
        }))
        {
            logger.LogInformation("Processing order {OrderId} for customer {CustomerId}",
                order.Id, order.CustomerId);

            // exception handling example
            {
                await repo.SaveAsync(order, ct);
                logger.LogInformation("Order {OrderId} saved successfully", order.Id);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Failed to save order {OrderId}", order.Id);
                throw;
            }
        }
    }
}
```

### Collection Expression for Log Properties

```csharp
// Modern structured logging with collection expressions
public void LogRequestMetrics(HttpContext context, TimeSpan elapsed)
{
    var properties = new Dictionary<string, object>
    {
        ["Path"] = context.Request.Path,
        ["Method"] = context.Request.Method,
        ["StatusCode"] = context.Response.StatusCode,
        ["ElapsedMs"] = elapsed.TotalMilliseconds
    };

    _logger.LogInformation("Request completed {Path} {Method}: {StatusCode} in {ElapsedMs}ms",
        context.Request.Path, context.Request.Method,
        context.Response.StatusCode, elapsed.TotalMilliseconds);
}
```

### File-Scoped Logging Extension for Internal Events

```csharp
// Hide internal logging helpers in file scope
file static class InternalLogEvents
{
    internal const int CacheHitId = 1001;
    internal const int CacheMissId = 1002;

    internal static void LogCacheHit(this ILogger logger, string key) =>
        logger.LogDebug(CacheHitId, "Cache hit for key {CacheKey}", key);

    internal static void LogCacheMiss(this ILogger logger, string key) =>
        logger.LogDebug(CacheMissId, "Cache miss for key {CacheKey}", key);
}
```
