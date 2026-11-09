# ProblemDetails (RFC 9457) Reference

RFC 9457 (formerly RFC 7807) defines a standard JSON/XML format for HTTP API errors. ASP.NET Core has built-in support as of .NET 7.

## Core Structure

```json
{
  "type": "https://example.com/errors/insufficient-credit",
  "title": "Insufficient credit",
  "status": 400,
  "detail": "Your account has a balance of $30 but this transaction requires $50.",
  "instance": "/account/12345/transactions/abc"
}
```

**Required fields:**

- `type` (string, URI): Identifies the problem type. Should be a stable, dereferenceable URL documenting the error. Defaults to `about:blank`.
- `title` (string): Short, human-readable summary. Should be consistent across instances of the same type.
- `status` (integer): HTTP status code. Must match the response status.

**Optional fields:**

- `detail` (string): Human-readable explanation specific to this occurrence.
- `instance` (string, URI): Identifies this specific occurrence. Often the request path or a correlation ID.

**Extension members:** Any additional fields are allowed (e.g., `traceId`, `errors`, `timestamp`).

## ASP.NET Core Integration

### Automatic ValidationProblemDetails

When `[ApiController]` detects invalid `ModelState`, it automatically returns:

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "Email": ["The Email field is not a valid e-mail address."],
    "Age": ["The field Age must be between 0 and 120."]
  },
  "traceId": "00-abc123..."
}
```

The `errors` dictionary maps field names to error arrays—perfect for client-side form validation.

### Manual ProblemDetails

In controllers:

```csharp
return Problem(
    statusCode: StatusCodes.Status409Conflict,
    title: "Resource conflict",
    detail: "A user with this email already exists.",
    type: "https://api.example.com/errors/duplicate-email",
    instance: HttpContext.Request.Path
);
```

### Global Exception Handling

Use `IExceptionHandler` (ASP.NET Core 8+):

```csharp
public sealed class GlobalExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var (status, title, type) = exception switch
        {
            EntityNotFoundException => (404, "Not found", "https://tools.ietf.org/html/rfc9110#section-15.5.5"),
            UnauthorizedException => (401, "Unauthorized", "https://tools.ietf.org/html/rfc9110#section-15.5.2"),
            _ => (500, "Internal server error", "https://tools.ietf.org/html/rfc9110#section-15.6.1")
        };

        var problemDetails = new ProblemDetails
        {
            Status = status,
            Title = title,
            Type = type,
            Detail = exception.Message,
            Instance = httpContext.Request.Path
        };

        problemDetails.Extensions["traceId"] = httpContext.TraceIdentifier;

        httpContext.Response.StatusCode = status;
        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);

        return true;
    }
}
```

Register in `Program.cs`:

```csharp
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
builder.Services.AddProblemDetails();

app.UseExceptionHandler();
```

## Customizing ProblemDetails

### Add Custom Fields

```csharp
var problemDetails = new ProblemDetails
{
    Status = 422,
    Title = "Business rule violation",
    Detail = "Cannot delete a user with active orders."
};

problemDetails.Extensions["activeOrderCount"] = 3;
problemDetails.Extensions["suggestedAction"] = "Archive the user instead of deleting.";

return new ObjectResult(problemDetails)
{
    StatusCode = 422
};
```

### Customize via ProblemDetailsOptions

```csharp
builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = context =>
    {
        context.ProblemDetails.Extensions["traceId"] = context.HttpContext.TraceIdentifier;
        context.ProblemDetails.Extensions["timestamp"] = DateTime.UtcNow;

        // Never leak stack traces in production
        if (!context.HttpContext.RequestServices
            .GetRequiredService<IWebHostEnvironment>()
            .IsDevelopment())
        {
            context.ProblemDetails.Extensions.Remove("exception");
        }
    };
});
```

## Best Practices

**DO:**

- Use consistent `type` URIs across your API (e.g., `https://api.example.com/errors/validation-failed`)
- Include `traceId` for correlation with server logs
- Return `ValidationProblemDetails` for field-level errors (400)
- Use specific status codes (404, 409, 422) over generic 400/500
- Document all ProblemDetails shapes in OpenAPI with `[ProducesResponseType]`

**DON'T:**

- Return stack traces or internal error details in production
- Use different error formats (plain text, custom JSON) alongside ProblemDetails
- Overload `400 Bad Request`—use 422 for business rule violations
- Ignore the `instance` field—it's critical for debugging
- Return 200 OK with an error payload ("soft errors")—always use proper status codes

## OpenAPI Documentation

```csharp
[ProducesResponseType<UserResponse>(StatusCodes.Status200OK)]
[ProducesResponseType<ValidationProblemDetails>(StatusCodes.Status400BadRequest)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status404NotFound)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status500InternalServerError)]
public async Task<IActionResult> GetUser(int id) { }
```

This generates precise OpenAPI schemas clients can rely on.

## Validation Error Consolidation Pattern

When multiple layers (controller, service, domain) detect validation issues, consolidate into a single `ValidationProblemDetails` response:

```csharp
public IActionResult CreateOrder(OrderRequest request)
{
    // Controller-level validation already done by [ApiController]

    // Service-level validation
    var validationErrors = orderService.Validate(request);
    if (validationErrors.Any())
    {
        foreach (var error in validationErrors)
        {
            ModelState.AddModelError(error.Field, error.Message);
        }
        return ValidationProblem();
    }

    var order = orderService.Create(request);
    return CreatedAtAction(nameof(GetOrder), new { id = order.Id }, order);
}
```

This keeps error responses consistent whether validation fails at the DTO level or in business logic.

## Further Reading

- [RFC 9457 Specification](https://www.rfc-editor.org/rfc/rfc9457.html)
- [ASP.NET Core Error Handling Docs](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling)
- [ProblemDetails Class Reference](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.mvc.problemdetails)
