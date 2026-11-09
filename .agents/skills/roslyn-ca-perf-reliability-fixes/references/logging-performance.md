---
title: Logging Performance Patterns
doc_type: reference
status: active
last_updated: 2026-08-28
---

# Logging Performance Patterns

## CA1848: Use LoggerMessage Delegates

### Problem

Traditional logging uses string interpolation or concatenation at call site, allocating even when logging is disabled.

### Solution Pattern

Use compile-time LoggerMessage source generator (C# 10+):

```csharp
public static partial class Log
{
    [LoggerMessage(EventId = 1001, Level = LogLevel.Information,
        Message = "Processing order {OrderId} for customer {CustomerId}")]
    public static partial void ProcessingOrder(this ILogger logger, string orderId, string customerId);
}
```

### Benefits
- Zero allocation when log level disabled
- 3-6x faster than string interpolation
- Compile-time placeholder validation

## CA2254: Template Is Static Expression

### Problem

Dynamic log templates prevent optimization.

### Solution

Use static templates or separate LoggerMessage methods per condition.

```csharp
if (includeDetails)
    _logger.LogInformation("User {UserId} action: {Action}", userId, action);
else
    _logger.LogInformation("User {UserId}", userId);
```
