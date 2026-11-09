# CancellationToken Propagation Patterns

Advanced patterns for CancellationToken in distributed systems.

## Complete Propagation Chain

```csharp
// API Controller
[HttpGet("{id}")]
public async Task<ActionResult<OrderDto>> GetOrder(
    int id,
    CancellationToken ct) // ASP.NET binds this automatically
{
    var result = await _orderService.GetOrderAsync(id, ct);
    return result.IsSuccess
        ? Ok(result.Value)
        : Problem(result.Problem);
}

// Service Layer
public async Task<Result<OrderDto>> GetOrderAsync(int id, CancellationToken ct)
{
    try
    {
        var order = await _repository.GetByIdAsync(id, ct);
        if (order == null)
            return Result.NotFound($"Order {id} not found");

        var customer = await _customerService.GetCustomerAsync(order.CustomerId, ct);
        var items = await _inventoryService.GetItemsAsync(order.ItemIds, ct);

        return Result.Success(MapToDto(order, customer, items));
    }
    catch (OperationCanceledException)
    {
        _logger.LogInformation("Order retrieval cancelled for {OrderId}", id);
        throw; // Let it propagate
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error retrieving order {OrderId}", id);
        return Result.Problem(500, "Internal Error", "Unable to retrieve order");
    }
}

// Repository Layer
public async Task<Order?> GetByIdAsync(int id, CancellationToken ct)
{
    return await _dbContext.Orders
        .Include(o => o.Items)
        .FirstOrDefaultAsync(o => o.Id == id, ct); // EF Core respects ct
}
```

## Timeout Composition

Combine request timeout with operation timeout:

```csharp
public async Task<Result<Data>> GetWithTimeoutAsync(
    int id,
    CancellationToken requestCt)
{
    using var timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
    using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(
        requestCt,
        timeoutCts.Token);

    try
    {
        var data = await _externalApi.FetchDataAsync(id, linkedCts.Token);
        return Result.Success(data);
    }
    catch (OperationCanceledException) when (timeoutCts.IsCancellationRequested)
    {
        return Result.Problem(408, "Request Timeout",
            "External service did not respond in time");
    }
    catch (OperationCanceledException)
    {
        throw; // Request cancellation, propagate it
    }
}
```

## Background Work with Application Lifetime

```csharp
public class OrderProcessingService : BackgroundService
{
    private readonly IServiceProvider _services;
    private readonly ILogger<OrderProcessingService> _logger;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ProcessBatchAsync(stoppingToken);
                await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
            }
            catch (OperationCanceledException)
            {
                _logger.LogInformation("Order processing stopped");
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing orders");
                // Continue processing
            }
        }
    }

    private async Task ProcessBatchAsync(CancellationToken ct)
    {
        using var scope = _services.CreateScope();
        var orderService = scope.ServiceProvider.GetRequiredService<IOrderService>();

        var pendingOrders = await orderService.GetPendingOrdersAsync(ct);

        foreach (var order in pendingOrders)
        {
            if (ct.IsCancellationRequested)
                break;

            await orderService.ProcessOrderAsync(order.Id, ct);
        }
    }
}
```

## Retry with Cancellation

```csharp
public async Task<Result<T>> RetryAsync<T>(
    Func<CancellationToken, Task<Result<T>>> operation,
    int maxRetries,
    CancellationToken ct)
{
    for (int attempt = 0; attempt <= maxRetries; attempt++)
    {
        if (ct.IsCancellationRequested)
            return Result.Problem(499, "Request Cancelled", "Operation was cancelled");

        var result = await operation(ct);

        if (result.IsSuccess || !IsTransient(result.Problem))
            return result;

        if (attempt < maxRetries)
        {
            var delay = TimeSpan.FromSeconds(Math.Pow(2, attempt));
            _logger.LogWarning("Retry {Attempt}/{MaxRetries} after {Delay}s",
                attempt + 1, maxRetries, delay.TotalSeconds);
            await Task.Delay(delay, ct);
        }
    }

    return Result.Problem(503, "Service Unavailable",
        "Operation failed after retries");
}

private bool IsTransient(ProblemDetails problem)
{
    return problem.Status is 408 or 429 or 500 or 502 or 503 or 504;
}
```

## Parallel Operations with Cancellation

```csharp
public async Task<Result<Summary>> GetDashboardAsync(int userId, CancellationToken ct)
{
    try
    {
        var ordersTask = _orderService.GetRecentOrdersAsync(userId, ct);
        var shipmentsTask = _shippingService.GetActiveShipmentsAsync(userId, ct);
        var invoicesTask = _invoiceService.GetPendingInvoicesAsync(userId, ct);

        await Task.WhenAll(ordersTask, shipmentsTask, invoicesTask);

        return Result.Success(new Summary
        {
            Orders = await ordersTask,
            Shipments = await shipmentsTask,
            Invoices = await invoicesTask
        });
    }
    catch (OperationCanceledException)
    {
        _logger.LogInformation("Dashboard load cancelled for user {UserId}", userId);
        throw;
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error loading dashboard for user {UserId}", userId);
        return Result.Problem(500, "Internal Error", "Unable to load dashboard");
    }
}
```

## Graceful Degradation

Continue with partial results when non-critical operations are cancelled:

```csharp
public async Task<Result<ProductDetails>> GetProductDetailsAsync(
    int productId,
    CancellationToken ct)
{
    var product = await _repository.GetProductAsync(productId, ct);
    if (product == null)
        return Result.NotFound($"Product {productId} not found");

    var details = new ProductDetails { Product = product };

    // Critical: pricing must succeed
    var pricingResult = await _pricingService.GetPricingAsync(productId, ct);
    if (!pricingResult.IsSuccess)
        return Result.Problem(pricingResult.Problem);
    details.Pricing = pricingResult.Value;

    // Non-critical: reviews are optional
    try
    {
        using var reviewCts = CancellationTokenSource.CreateLinkedTokenSource(ct);
        reviewCts.CancelAfter(TimeSpan.FromSeconds(2));

        var reviewsResult = await _reviewService.GetReviewsAsync(
            productId, reviewCts.Token);
        if (reviewsResult.IsSuccess)
            details.Reviews = reviewsResult.Value;
    }
    catch (OperationCanceledException)
    {
        _logger.LogWarning("Reviews timed out for product {ProductId}", productId);
        // Continue without reviews
    }

    return Result.Success(details);
}
```

## HttpClient with Cancellation

```csharp
public class ExternalApiClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<ExternalApiClient> _logger;

    public async Task<Result<ApiResponse>> CallExternalApiAsync(
        ApiRequest request,
        CancellationToken ct)
    {
        try
        {
            var httpRequest = new HttpRequestMessage(HttpMethod.Post, "/api/endpoint")
            {
                Content = JsonContent.Create(request)
            };

            var response = await _httpClient.SendAsync(httpRequest, ct);

            if (!response.IsSuccessStatusCode)
            {
                var problemContent = await response.Content
                    .ReadFromJsonAsync<ProblemDetails>(ct);
                return Result.Problem(problemContent ?? new ProblemDetails
                {
                    Status = (int)response.StatusCode,
                    Title = response.ReasonPhrase ?? "External API Error"
                });
            }

            var data = await response.Content.ReadFromJsonAsync<ApiResponse>(ct);
            return Result.Success(data!);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "HTTP error calling external API");
            return Result.Problem(502, "Bad Gateway",
                "Error communicating with external service");
        }
        catch (OperationCanceledException)
        {
            _logger.LogInformation("External API call cancelled");
            throw;
        }
    }
}
```

## Testing Cancellation

```csharp
[Fact]
public async Task GetOrderAsync_CancelledToken_ThrowsOperationCancelledException()
{
    var cts = new CancellationTokenSource();
    cts.Cancel();

    await Assert.ThrowsAsync<OperationCanceledException>(
        () => _service.GetOrderAsync(123, cts.Token));
}

[Fact]
public async Task GetOrderAsync_CancellationDuringExecution_StopsGracefully()
{
    var cts = new CancellationTokenSource();

    var task = _service.GetLongRunningOrderAsync(123, cts.Token);

    await Task.Delay(100); // Let it start
    cts.Cancel();

    await Assert.ThrowsAsync<OperationCanceledException>(() => task);

    // Verify cleanup happened
    _mockRepository.Verify(r => r.ReleaseLocksAsync(), Times.Once);
}
```
