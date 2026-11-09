---
metadata-version: "1.0.0"
title: "Volatility-Based Decomposition ServiceModel Architecture"
description: "Preserve scoped source guidance for vbd-service-contracts."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Volatility-Based Decomposition ServiceModel Architecture

Generate .NET components that follow Volatility-Based Decomposition (VBD) ServiceModel/RPC patterns with strict boundary enforcement, async-first design, and standardized error handling.

## Terminology Guardrail

In this repository, **VBD means Volatility-Based Decomposition** (per Lowy's iDesign decomposition guidance: Manager/Engine/Access and volatility-first boundaries).

## Core Principles

**Component boundaries are contracts.** Every public method represents a service endpoint that can be called across process boundaries. Design for interception, tracing, and enrichment without requiring developers to understand the infrastructure.

**Exceptions never cross boundaries.** Internal exceptions are implementation details. Map all exceptions to RFC 9457 ProblemDetails at the boundary so consumers receive structured, actionable error information.

**Cancellation is a first-class concern.** Every async operation accepts CancellationToken as the final parameter. Propagate tokens through the entire call chain to enable graceful shutdown and resource cleanup.

**Proxies enable transparency.** ServiceModel proxies intercept calls for logging, metrics, retry logic, circuit breaking, and distributed tracing without polluting business logic.

## Method Signature Pattern

Every public method follows this structure:

```csharp
[ServiceOperation] // or [OperationContract] for WCF-style
public async Task<TResult> MethodNameAsync(
    TParam1 param1,
    TParam2 param2,
    CancellationToken ct)
{
    // Implementation
}
```

**Key requirements:**

- All public methods are async (return `Task` or `Task<T>`)
- CancellationToken is always the last parameter, named `ct`
- Methods are decorated with ServiceModel attributes for proxy generation
- Return types are never void (use `Task` for fire-and-forget, `Task<Unit>` for explicit completion)
- Method names use `Async` suffix

## Exception Boundary Pattern

Map internal exceptions to ProblemDetails at component boundaries:

```csharp
public async Task<Result<Order>> GetOrderAsync(int orderId, CancellationToken ct)
{
    try
    {
        var order = await repository.GetByIdAsync(orderId, ct);
        if (order == null)
        {
            return Result.Problem(
                status: 404,
                title: "Order Not Found",
                detail: $"Order {orderId} does not exist",
                type: "https://api.example.com/errors/order-not-found");
        }

        return Result.Success(order);
    }
    catch (DbException ex)
    {
        logger.LogError(ex, "Database error retrieving order {OrderId}", orderId);
        return Result.Problem(
            status: 500,
            title: "Database Error",
            detail: "An error occurred accessing the database",
            type: "https://api.example.com/errors/database");
    }
    catch (OperationCanceledException)
    {
        logger.LogInformation("Order retrieval cancelled for {OrderId}", orderId);
        throw; // OCE is expected, propagate it
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Unexpected error retrieving order {OrderId}", orderId);
        return Result.Problem(
            status: 500,
            title: "Internal Error",
            detail: "An unexpected error occurred",
            type: "https://api.example.com/errors/internal");
    }
}
```

**Why this matters:** Consumers should never see raw exceptions like `SqlException` or `NullReferenceException`. ProblemDetails provides:

- Consistent structure across all errors
- HTTP-friendly status codes
- Type URIs for documentation linking
- Machine-readable format for client error handling
- Correlation IDs and trace information (added via extensions)

## CancellationToken Propagation

Pass CancellationToken through every async boundary:

```csharp
public async Task<Result<Invoice>> ProcessOrderAsync(
    Order order,
    CancellationToken ct)
{
    // Pass to all async calls
    var customer = await customerService.GetCustomerAsync(order.CustomerId, ct);
    var inventory = await inventoryService.ReserveItemsAsync(order.Items, ct);
    var payment = await paymentService.ChargeAsync(customer, order.Total, ct);

    // Check cancellation at logical boundaries
    ct.ThrowIfCancellationRequested();

    var invoice = await invoiceService.GenerateAsync(order, payment, ct);
    return Result.Success(invoice);
}
```

**Propagation rules:**

- Pass `ct` to every method that accepts it
- Check `ct.ThrowIfCancellationRequested()` before expensive operations
- Never ignore cancellation - it signals the client has disconnected or timed out
- Let `OperationCanceledException` propagate (don't catch it unless cleaning up)

## ServiceModel Proxy Pattern

Use proxies for cross-component calls to enable interception:

```csharp
// Service interface
public interface IOrderService
{
    Task<Result<Order>> GetOrderAsync(int orderId, CancellationToken ct);
    Task<Result<Order>> CreateOrderAsync(CreateOrderRequest request, CancellationToken ct);
}

// Consumer uses proxy, not direct implementation
public class CheckoutWorkflow
{
    private readonly IOrderService orderService;

    public CheckoutWorkflow(IOrderService orderService)
    {
        this.orderService = orderService; // Runtime proxy intercepts calls
    }

    public async Task<Result<Checkout>> CompleteCheckoutAsync(
        Cart cart,
        CancellationToken ct)
    {
        // This call goes through proxy infrastructure
        // Proxy adds: logging, metrics, tracing, retry, circuit breaking
        var orderResult = await orderService.CreateOrderAsync(
            new CreateOrderRequest(cart), ct);

        if (!orderResult.IsSuccess)
            return Result.Problem(orderResult.Problem);

        // Continue workflow
    }
}
```

**Proxy benefits:**

- Distributed tracing correlation IDs automatically propagated
- Call duration metrics collected without manual instrumentation
- Retry and circuit breaker policies applied declaratively
- Request/response logging for debugging
- Developers write business logic, infrastructure handles cross-cutting concerns

## Result<T> Pattern for Boundary Calls

Return `Result<T>` instead of throwing exceptions:

```csharp
public readonly struct Result<T>
{
    public bool IsSuccess { get; }
    public T Value { get; }
    public ProblemDetails Problem { get; }

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Problem(ProblemDetails problem) => new(problem);
}
```

This enables:

- Explicit error handling at call sites
- No hidden control flow via exceptions
- Composable error propagation
- Clear distinction between expected failures (Result.Problem) and unexpected exceptions (caught and mapped)

## Attribute-Based Service Contracts

Decorate methods for proxy generation:

```csharp
[ServiceContract]
public interface IPaymentService
{
    [OperationContract]
    [FaultContract(typeof(ProblemDetails))]
    Task<Result<PaymentConfirmation>> ProcessPaymentAsync(
        PaymentRequest request,
        CancellationToken ct);
}
```

Attributes enable:

- Code generation for client proxies
- Metadata for service discovery
- Contract versioning and compatibility checks
- Automatic serialization configuration

## ProblemDetails Extensions

Enrich errors with trace and correlation data:

```csharp
public static ProblemDetails CreateProblem(
    int status,
    string title,
    string detail,
    string type,
    HttpContext? httpContext = null)
{
    var problem = new ProblemDetails
    {
        Status = status,
        Title = title,
        Detail = detail,
        Type = type
    };

    // Add standard extensions
    problem.Extensions["traceId"] = Activity.Current?.Id ?? "unknown";
    problem.Extensions["timestamp"] = DateTimeOffset.UtcNow;

    if (httpContext != null)
    {
        problem.Instance = $"{httpContext.Request.Method} {httpContext.Request.Path}";
        problem.Extensions["requestId"] = httpContext.TraceIdentifier;
    }

    return problem;
}
```

## Decision Tree

1. **Is this a public method?** → Yes: Apply ServiceModel pattern
2. **Does it perform I/O or take >100ms?** → Yes: Make it async with CancellationToken
3. **Can it fail in expected ways?** → Yes: Return `Result<T>`, map exceptions to ProblemDetails
4. **Will other components call it?** → Yes: Use interface + proxy injection
5. **Does it call other services?** → Yes: Propagate CancellationToken, handle Result<T> failures

## Anti-Patterns to Avoid

**Letting exceptions escape:** Raw exceptions leak implementation details and break clients.

```csharp
// BAD
public async Task<Order> GetOrderAsync(int id, CancellationToken ct)
{
    return await dbContext.Orders.FindAsync(id); // SqlException escapes
}

// GOOD
public async Task<Result<Order>> GetOrderAsync(int id, CancellationToken ct)
{
    try
    {
        var order = await dbContext.Orders.FindAsync(id);
        return order != null
            ? Result.Success(order)
            : Result.Problem(404, "Not Found", $"Order {id} not found");
    }
    catch (DbException ex)
    {
        logger.LogError(ex, "Database error");
        return Result.Problem(500, "Database Error", "Unable to retrieve order");
    }
}
```

**Stopping CancellationToken at boundaries:** Breaks graceful shutdown and wastes resources.

```csharp
// BAD
public async Task<Result<Data>> GetDataAsync(int id, CancellationToken ct)
{
    var data = await repository.GetAsync(id); // Missing ct!
    return Result.Success(data);
}

// GOOD
public async Task<Result<Data>> GetDataAsync(int id, CancellationToken ct)
{
    var data = await repository.GetAsync(id, ct); // Propagated
    return Result.Success(data);
}
```

**Returning void from async methods:** Loses exception information and completion tracking.

```csharp
// BAD
public async void ProcessAsync(Data data, CancellationToken ct) { }

// GOOD
public async Task ProcessAsync(Data data, CancellationToken ct) { }
```

## Implementation Checklist

- [ ] All public methods are async with `Task` or `Task<T>` return types
- [ ] CancellationToken is the last parameter on every async method
- [ ] Exceptions are caught and mapped to ProblemDetails at boundaries
- [ ] OperationCanceledException is allowed to propagate
- [ ] ServiceModel attributes decorate public interfaces
- [ ] Methods return `Result<T>` for operations that can fail
- [ ] CancellationToken is passed to all downstream async calls
- [ ] ProblemDetails includes traceId and correlation information
- [ ] Logging captures errors before mapping to ProblemDetails
- [ ] Proxy injection used for cross-component calls
