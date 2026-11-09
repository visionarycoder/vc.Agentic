# ProblemDetails Exception Mapping Reference

Comprehensive patterns for mapping .NET exceptions to RFC 9457 ProblemDetails.

## Standard HTTP Status Mappings

```csharp
public static class ExceptionMapper
{
    public static ProblemDetails MapException(Exception ex, HttpContext? context = null)
    {
        return ex switch
        {
            ArgumentException or ArgumentNullException or ArgumentOutOfRangeException
                => CreateProblem(400, "Bad Request", ex.Message,
                    "https://api.example.com/errors/bad-request", context),

            UnauthorizedAccessException
                => CreateProblem(401, "Unauthorized", "Authentication required",
                    "https://api.example.com/errors/unauthorized", context),

            InvalidOperationException when ex.Message.Contains("not found")
                => CreateProblem(404, "Not Found", ex.Message,
                    "https://api.example.com/errors/not-found", context),

            TimeoutException
                => CreateProblem(408, "Request Timeout", "Operation timed out",
                    "https://api.example.com/errors/timeout", context),

            InvalidOperationException when ex.Message.Contains("conflict")
                => CreateProblem(409, "Conflict", ex.Message,
                    "https://api.example.com/errors/conflict", context),

            DbUpdateConcurrencyException
                => CreateProblem(409, "Concurrency Conflict",
                    "Resource was modified by another user",
                    "https://api.example.com/errors/concurrency", context),

            NotImplementedException
                => CreateProblem(501, "Not Implemented", "Feature not implemented",
                    "https://api.example.com/errors/not-implemented", context),

            DbException or SqlException
                => CreateProblem(500, "Database Error",
                    "An error occurred accessing the database",
                    "https://api.example.com/errors/database", context),

            HttpRequestException
                => CreateProblem(502, "Bad Gateway",
                    "Error communicating with external service",
                    "https://api.example.com/errors/external-service", context),

            _   => CreateProblem(500, "Internal Server Error",
                    "An unexpected error occurred",
                    "https://api.example.com/errors/internal", context)
        };
    }
}
```

## Domain-Specific Exception Mapping

Create custom exceptions for business rules:

```csharp
public class InsufficientInventoryException : Exception
{
    public int RequestedQuantity { get; }
    public int AvailableQuantity { get; }
    public string ProductId { get; }

    public InsufficientInventoryException(
        string productId,
        int requested,
        int available)
        : base($"Insufficient inventory for {productId}")
    {
        ProductId = productId;
        RequestedQuantity = requested;
        AvailableQuantity = available;
    }

    public ProblemDetails ToProblemDetails() => new()
    {
        Status = 409,
        Title = "Insufficient Inventory",
        Detail = $"Requested {RequestedQuantity} but only {AvailableQuantity} available",
        Type = "https://api.example.com/errors/insufficient-inventory",
        Extensions =
        {
            ["productId"] = ProductId,
            ["requestedQuantity"] = RequestedQuantity,
            ["availableQuantity"] = AvailableQuantity
        }
    };
}
```

## Validation Error Mapping

Map FluentValidation or DataAnnotations failures:

```csharp
public static ProblemDetails MapValidationErrors(ValidationException ex)
{
    var problem = new ProblemDetails
    {
        Status = 400,
        Title = "Validation Failed",
        Detail = "One or more validation errors occurred",
        Type = "https://api.example.com/errors/validation"
    };

    var errors = ex.Errors
        .GroupBy(e => e.PropertyName)
        .ToDictionary(
            g => g.Key,
            g => g.Select(e => e.ErrorMessage).ToArray());

    problem.Extensions["errors"] = errors;
    return problem;
}
```

Example output:
```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 400,
  "detail": "One or more validation errors occurred",
  "errors": {
    "Email": ["Email address is required", "Email format is invalid"],
    "Age": ["Age must be between 18 and 120"]
  }
}
```

## Sensitive Data Protection

Never leak internal details in production:

```csharp
public static ProblemDetails SafeMapException(
    Exception ex,
    IHostEnvironment env,
    HttpContext? context = null)
{
    var problem = MapException(ex, context);

    if (!env.IsDevelopment())
    {
        // Remove sensitive details in production
        problem.Detail = "An error occurred processing your request";
        problem.Extensions.Remove("stackTrace");
        problem.Extensions.Remove("innerException");
    }
    else
    {
        // Include debugging info in development
        problem.Extensions["stackTrace"] = ex.StackTrace;
        problem.Extensions["exceptionType"] = ex.GetType().FullName;
        if (ex.InnerException != null)
            problem.Extensions["innerException"] = ex.InnerException.Message;
    }

    return problem;
}
```

## Correlation and Tracing

Always include trace information:

```csharp
private static ProblemDetails CreateProblem(
    int status,
    string title,
    string detail,
    string type,
    HttpContext? context = null)
{
    var problem = new ProblemDetails
    {
        Status = status,
        Title = title,
        Detail = detail,
        Type = type
    };

    // Distributed tracing
    var activity = Activity.Current;
    if (activity != null)
    {
        problem.Extensions["traceId"] = activity.Id;
        problem.Extensions["spanId"] = activity.SpanId.ToString();
        problem.Extensions["parentId"] = activity.ParentId;
    }

    // Request context
    if (context != null)
    {
        problem.Instance = $"{context.Request.Method} {context.Request.Path}";
        problem.Extensions["requestId"] = context.TraceIdentifier;
    }

    problem.Extensions["timestamp"] = DateTimeOffset.UtcNow;

    return problem;
}
```

## ASP.NET Core Integration

Global exception handler:

```csharp
public class ProblemDetailsExceptionHandler : IExceptionHandler
{
    private readonly ILogger<ProblemDetailsExceptionHandler> _logger;
    private readonly IHostEnvironment _env;

    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken ct)
    {
        if (exception is OperationCanceledException)
        {
            // Client disconnected, don't log as error
            _logger.LogInformation("Request cancelled: {Path}", httpContext.Request.Path);
            httpContext.Response.StatusCode = 499; // Client Closed Request
            return true;
        }

        _logger.LogError(exception, "Unhandled exception");

        var problem = ExceptionMapper.SafeMapException(exception, _env, httpContext);

        httpContext.Response.StatusCode = problem.Status ?? 500;
        await httpContext.Response.WriteAsJsonAsync(problem, ct);

        return true;
    }
}

// Register in Program.cs
builder.Services.AddExceptionHandler<ProblemDetailsExceptionHandler>();
builder.Services.AddProblemDetails();
```

## Testing Exception Mapping

```csharp
[Fact]
public void MapException_ArgumentException_Returns400()
{
    var ex = new ArgumentException("Invalid parameter");
    var problem = ExceptionMapper.MapException(ex);

    Assert.Equal(400, problem.Status);
    Assert.Equal("Bad Request", problem.Title);
    Assert.Contains("Invalid parameter", problem.Detail);
}

[Fact]
public void MapException_IncludesTraceId()
{
    using var activity = new Activity("test").Start();
    var ex = new InvalidOperationException();
    var problem = ExceptionMapper.MapException(ex);

    Assert.True(problem.Extensions.ContainsKey("traceId"));
    Assert.Equal(activity.Id, problem.Extensions["traceId"]);
}
```
