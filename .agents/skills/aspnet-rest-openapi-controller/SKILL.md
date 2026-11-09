---
name: "aspnet-rest-openapi-controller"
description: "Build production-grade ASP.NET Core controllers following REST semantics and OpenAPI/OpenAI-style API specifications. Use this when creating or refactoring API controllers, implementing model validation with ProblemDetails (RFC 9457), designing OpenAPI-first endpoints, handling validation errors with early exit patterns, consolidating errors from deeper call chains, streaming responses with SSE, or implementing deterministic JSON serialization for AI/LLM-friendly APIs. Also applies to Web API modernization, API versioning, error standardization, and building spec-driven, contract-first HTTP APIs in .NET 8-10/C# 12-14."
metadata:
  metadata-version: "1.0.0"
  title: "ASP.NET REST + OpenAPI Controller"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# ASP.NET REST + OpenAPI Controller

## Philosophy

A controller is a **thin HTTP façade**—nothing more. Its job: bind inputs, validate contracts, call services, return typed results. Business logic, data access, domain rules, and serialization hacks belong elsewhere.

This matters because OpenAPI/OpenAI-style APIs demand **strict contract adherence**: deterministic JSON, schema-driven DTOs, predictable errors, and streaming support. Controllers that stay thin and declarative make these guarantees easy to uphold.

## Core Pattern

**Controller responsibilities (exhaustive list):**

- Validate request contract via `[ApiController]` automatic validation
- Bind inputs (route, query, body) to strongly-typed DTOs
- Call application service (one line)
- Return typed result (`Ok`, `CreatedAtAction`, `NoContent`)
- Emit OpenAPI metadata via attributes
- Support streaming when required (SSE for LLM-style APIs)
- Enforce idempotency and versioning via routing

**Never in a controller:**

- Business logic
- Data access or EF Core queries
- Domain rules or calculations
- Manual JSON serialization
- Conditional branching beyond HTTP concerns (status code selection, content negotiation)

If you're writing `if` statements that check business conditions, move that logic to a service.

## Attribute-Driven Contract Definition

```csharp
[ApiController]
[Route("v1/chat")]
public sealed class ChatController : ControllerBase
{
    private readonly IChatService chatService;

    public ChatController(IChatService chatService)
    {
        this.chatService = chatService;
    }

    [HttpPost("completions")]
    [ProducesResponseType<ChatCompletionResponse>(StatusCodes.Status200OK)]
    [ProducesResponseType<ProblemDetails>(StatusCodes.Status400BadRequest)]
    [ProducesResponseType<ProblemDetails>(StatusCodes.Status500InternalServerError)]
    public async Task<IActionResult> CreateCompletion(
        [FromBody] ChatCompletionRequest request,
        CancellationToken cancellationToken)
    {
        var result = await chatService.CreateCompletionAsync(request, cancellationToken);
        return Ok(result);
    }
}
```

**Why this works:**

- `[ApiController]` enables automatic model validation—invalid requests return `400` + `ValidationProblemDetails` before your code runs
- `[ProducesResponseType<T>]` (generic, .NET 8+) generates precise OpenAPI schemas
- No logic—just bind, call, return
- Cancellation tokens flow through for long-running operations

## DTO Design for OpenAPI Strictness

OpenAI/OpenAPI clients expect **zero ambiguity**. Your DTOs must be:

- **Immutable** (use `record`)
- **Explicit about nullability** (required vs optional)
- **CamelCase JSON** (configure globally)
- **No polymorphism** unless unavoidable

```csharp
public sealed record ChatCompletionRequest(
    string Model,
    IReadOnlyList<Message> Messages,
    double? Temperature = null,
    int? MaxTokens = null,
    bool Stream = false);

public sealed record Message(
    string Role,
    string Content);

public sealed record ChatCompletionResponse(
    string Id,
    string Model,
    IReadOnlyList<Choice> Choices,
    Usage Usage);
```

**Global JSON configuration** (in `Program.cs`):

```csharp
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
    options.SerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull;
    options.SerializerOptions.WriteIndented = false;
});
```

This ensures deterministic output—no whitespace variations, no null noise, no casing inconsistencies.

## Validation: Exit Early, Return ProblemDetails

`[ApiController]` handles data annotation validation automatically. For **business rule validation** (e.g., "only one owner allowed"), add errors to `ModelState` and return `ValidationProblem()`:

```csharp
[HttpPost]
[ProducesResponseType<PersonResponse>(StatusCodes.Status201Created)]
[ProducesResponseType<ValidationProblemDetails>(StatusCodes.Status400BadRequest)]
public IActionResult CreatePerson([FromBody] PersonRequest request)
{
    // Data annotations already validated by [ApiController]

    // Business rule validation
    if (request.Role == PersonRole.Owner && personService.HasOwner())
    {
        ModelState.AddModelError(nameof(PersonRequest.Role), "Only one owner is allowed");
        return ValidationProblem();
    }

    var person = personService.Create(request);
    return CreatedAtAction(nameof(GetPerson), new { id = person.Id }, person);
}
```

**ValidationProblem()** returns RFC 9457-compliant JSON:

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "Role": ["Only one owner is allowed"]
  },
  "traceId": "00-abc123..."
}
```

Clients get **field-level errors** they can map directly to form inputs.

## Error Consolidation from Deeper Layers

When services or domain layers detect errors, they should throw **domain-specific exceptions** (never return error codes or booleans). A global `IExceptionHandler` consolidates these into ProblemDetails.

**In `Program.cs`:**

```csharp
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
builder.Services.AddProblemDetails();

var app = builder.Build();
app.UseExceptionHandler();
app.UseStatusCodePages();
```

**GlobalExceptionHandler.cs:**

```csharp
public sealed class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> logger;

    public GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    {
        this.logger = logger;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var problemDetails = exception switch
        {
            EntityNotFoundException notFound => new ProblemDetails
            {
                Status = StatusCodes.Status404NotFound,
                Title = "Resource not found",
                Detail = notFound.Message,
                Type = "https://tools.ietf.org/html/rfc9110#section-15.5.5",
                Instance = httpContext.Request.Path
            },
            BusinessRuleException businessRule => new ProblemDetails
            {
                Status = StatusCodes.Status422UnprocessableEntity,
                Title = "Business rule violation",
                Detail = businessRule.Message,
                Type = "https://tools.ietf.org/html/rfc4918#section-11.2",
                Instance = httpContext.Request.Path
            },
            _ => new ProblemDetails
            {
                Status = StatusCodes.Status500InternalServerError,
                Title = "An error occurred",
                Detail = "An unexpected error occurred. Please contact support.",
                Type = "https://tools.ietf.org/html/rfc9110#section-15.6.1",
                Instance = httpContext.Request.Path
            }
        };

        problemDetails.Extensions["traceId"] = httpContext.TraceIdentifier;

        logger.LogError(exception,
            "Error handled: {Type} | Status: {Status} | TraceId: {TraceId}",
            exception.GetType().Name, problemDetails.Status, httpContext.TraceIdentifier);

        httpContext.Response.StatusCode = problemDetails.Status ?? 500;
        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);

        return true;
    }
}
```

**Why this works:**

- Controllers stay clean—no try/catch blocks
- All errors follow RFC 9457 ProblemDetails format
- Trace IDs link client errors to server logs
- Production errors hide internal details but log full context

## Streaming Responses (SSE for LLM APIs)

OpenAI-style APIs use **Server-Sent Events** for streaming completions. ASP.NET supports this via `IAsyncEnumerable<T>`:

```csharp
[HttpPost("completions/stream")]
public async Task StreamCompletion(
    [FromBody] ChatCompletionRequest request,
    CancellationToken cancellationToken)
{
    Response.Headers.ContentType = "text/event-stream";
    Response.Headers.CacheControl = "no-cache";
    Response.Headers.Connection = "keep-alive";

    await foreach (var chunk in chatService.StreamCompletionAsync(request, cancellationToken))
    {
        await Response.WriteAsync($"data: {JsonSerializer.Serialize(chunk)}\n\n", cancellationToken);
        await Response.Body.FlushAsync(cancellationToken);
    }
}
```

**Critical details:**

- Flush after each chunk—SSE requires immediate delivery
- Use `IAsyncEnumerable<T>` in service layer for backpressure
- Never buffer the entire response
- Disable compression for SSE endpoints (breaks streaming)
- Respect `CancellationToken` to detect client disconnects

## Versioning: Path-Based, Not Query-Based

OpenAI uses `/v1/...` path segments. Follow the same:

```csharp
[Route("v1/chat")]
public sealed class ChatV1Controller : ControllerBase { }

[Route("v2/chat")]
public sealed class ChatV2Controller : ControllerBase { }
```

Avoid query-based versioning (`?version=1`) or header-based versioning—path segments are explicit, cacheable, and OpenAPI-friendly.

## OpenAPI Metadata Quality

Your OpenAPI spec is your API's contract. Ensure it's **unambiguous**:

```csharp
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SupportNonNullableReferenceTypes();
    options.UseAllOfToExtendReferenceSchemas();
    options.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, "YourApi.xml"));
});
```

**Document all response types:**

```csharp
[ProducesResponseType<ChatCompletionResponse>(StatusCodes.Status200OK)]
[ProducesResponseType<ValidationProblemDetails>(StatusCodes.Status400BadRequest)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status401Unauthorized)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status500InternalServerError)]
```

Clients (and AI agents) rely on this metadata to generate correct requests.

## Testing Strategy

- **Integration tests** (WebApplicationFactory): Test full HTTP request/response cycle, including validation, error handling, and serialization
- **Contract tests**: Validate OpenAPI schema against actual responses (use tools like Schemathesis or Dredd)
- **Streaming tests**: Verify SSE chunking and cancellation behavior
- **Unit tests**: Test service layer, not controllers—controllers are too thin to unit test

## Common Mistakes to Avoid

- **Fat controllers**: If your controller has business logic, extract it to a service
- **Manual ModelState checks**: `[ApiController]` does this automatically—don't duplicate
- **Inconsistent error formats**: Always use ProblemDetails, never plain strings or custom JSON
- **Ignoring cancellation tokens**: Long-running operations must respect cancellation
- **Buffering streams**: SSE must flush immediately, not buffer
- **Polymorphic DTOs**: Avoid inheritance in request/response models—OpenAPI tooling struggles with it
- **Missing `ProducesResponseType` attributes**: Clients need to know all possible responses

## Reference Architecture

```
Controller (HTTP façade)
  ↓ calls
Application Service (orchestration, validation)
  ↓ calls
Domain Layer (business rules, entities)
  ↓ calls
Infrastructure (EF Core, external APIs)
```

Controllers never skip layers. If you're calling EF Core directly from a controller, refactor.

## When to Deviate

This pattern assumes **CRUD-style REST APIs**. For:

- **Minimal APIs**: Same principles apply, different syntax
- **GraphQL**: Different error model (errors array, not status codes)
- **gRPC**: Different transport, but thin façade principle still holds
- **CQRS**: Commands/queries replace services, but controllers remain thin

The core principle—**controllers are declarative HTTP bindings, nothing more**—applies universally.
