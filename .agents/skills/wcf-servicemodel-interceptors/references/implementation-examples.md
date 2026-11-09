# Implementation Examples

Detailed implementations for each interceptor layer.

## 1. Telemetry Interceptor (OpenTelemetry)

```csharp
using System.Diagnostics;
using System.ServiceModel;
using System.ServiceModel.Channels;
using System.ServiceModel.Dispatcher;

public class TelemetryMessageInspector : IDispatchMessageInspector
{
    private static readonly ActivitySource ActivitySource = new("MyCompany.WcfServices");

    public object AfterReceiveRequest(ref Message request, IClientChannel channel, InstanceContext instanceContext)
    {
        // Extract trace context from SOAP headers (W3C TraceContext format)
        var traceParent = ExtractTraceParent(request);
        var parentContext = ActivityContext.TryParse(traceParent, null, out var ctx) ? ctx : default;

        var activity = ActivitySource.StartActivity(
            $"WCF {request.Headers.Action}",
            ActivityKind.Server,
            parentContext
        );

        if (activity != null)
        {
            activity.SetTag("rpc.system", "wcf");
            activity.SetTag("rpc.service", instanceContext.Host.Description.Name);
            activity.SetTag("rpc.method", request.Headers.Action);
            activity.SetTag("net.peer.ip", channel.RemoteAddress?.Uri.Host);
            activity.SetTag("net.transport", "ip_tcp"); // or extract from binding
        }

        return activity;
    }

    public void BeforeSendReply(ref Message reply, object correlationState)
    {
        if (correlationState is Activity activity)
        {
            activity.SetTag("rpc.status_code", reply.IsFault ? "error" : "ok");
            if (reply.IsFault)
            {
                activity.SetStatus(ActivityStatusCode.Error);
            }
            activity.Stop();
        }
    }

    private string ExtractTraceParent(Message request)
    {
        // Extract from SOAP header or message property
        var headerIndex = request.Headers.FindHeader("traceparent", "http://opentelemetry.io/");
        if (headerIndex >= 0)
            return request.Headers.GetHeader<string>(headerIndex);
        return null;
    }
}
```

## 2. Logging Interceptor (Structured Logging)

```csharp
using Microsoft.Extensions.Logging;
using System.ServiceModel;
using System.ServiceModel.Channels;
using System.ServiceModel.Dispatcher;

public class LoggingMessageInspector : IDispatchMessageInspector
{
    private readonly ILogger<LoggingMessageInspector> _logger;

    public LoggingMessageInspector(ILogger<LoggingMessageInspector> logger)
    {
        _logger = logger;
    }

    public object AfterReceiveRequest(ref Message request, IClientChannel channel, InstanceContext instanceContext)
    {
        var correlationId = GetCorrelationId(request);
        var stopwatch = Stopwatch.StartNew();

        _logger.LogInformation(
            "WCF request received: {Operation} from {RemoteAddress} [CorrelationId: {CorrelationId}]",
            request.Headers.Action,
            channel.RemoteAddress?.Uri,
            correlationId
        );

        return stopwatch;
    }

    public void BeforeSendReply(ref Message reply, object correlationState)
    {
        if (correlationState is Stopwatch stopwatch)
        {
            stopwatch.Stop();
            var correlationId = Activity.Current?.Id ?? "unknown";

            if (reply.IsFault)
            {
                _logger.LogWarning(
                    "WCF request failed: {Duration}ms [CorrelationId: {CorrelationId}]",
                    stopwatch.ElapsedMilliseconds,
                    correlationId
                );
            }
            else
            {
                _logger.LogInformation(
                    "WCF request completed: {Duration}ms [CorrelationId: {CorrelationId}]",
                    stopwatch.ElapsedMilliseconds,
                    correlationId
                );
            }
        }
    }

    private string GetCorrelationId(Message request)
    {
        return Activity.Current?.Id ?? Guid.NewGuid().ToString();
    }
}
```

## 3. Correlation Interceptor

```csharp
public class CorrelationMessageInspector : IDispatchMessageInspector
{
    private const string CorrelationIdHeader = "X-Correlation-Id";
    private const string CausationIdHeader = "X-Causation-Id";

    public object AfterReceiveRequest(ref Message request, IClientChannel channel, InstanceContext instanceContext)
    {
        // Extract or generate correlation ID
        var correlationId = ExtractHeader(request, CorrelationIdHeader) ?? Guid.NewGuid().ToString();
        var causationId = ExtractHeader(request, CausationIdHeader);

        // Store in message properties for downstream access
        request.Properties["CorrelationId"] = correlationId;
        request.Properties["CausationId"] = causationId;

        // Store in OperationContext for access in service methods
        OperationContext.Current.IncomingMessageProperties["CorrelationId"] = correlationId;
        OperationContext.Current.IncomingMessageProperties["CausationId"] = causationId;

        return null;
    }

    public void BeforeSendReply(ref Message reply, object correlationState)
    {
        // Attach correlation ID to response
        var correlationId = OperationContext.Current.IncomingMessageProperties["CorrelationId"] as string;
        if (!string.IsNullOrEmpty(correlationId))
        {
            var header = MessageHeader.CreateHeader(CorrelationIdHeader, "http://mycompany.com/", correlationId);
            reply.Headers.Add(header);
        }
    }

    private string ExtractHeader(Message request, string headerName)
    {
        var headerIndex = request.Headers.FindHeader(headerName, "http://mycompany.com/");
        return headerIndex >= 0 ? request.Headers.GetHeader<string>(headerIndex) : null;
    }
}
```

## 4. Authentication Interceptor (JWT)

```csharp
using System.IdentityModel.Tokens.Jwt;
using Microsoft.IdentityModel.Tokens;

public class AuthenticationMessageInspector : IDispatchMessageInspector
{
    private readonly TokenValidationParameters _validationParameters;

    public AuthenticationMessageInspector(TokenValidationParameters validationParameters)
    {
        _validationParameters = validationParameters;
    }

    public object AfterReceiveRequest(ref Message request, IClientChannel channel, InstanceContext instanceContext)
    {
        var token = ExtractBearerToken(request);
        if (string.IsNullOrEmpty(token))
            throw new FaultException("Missing authentication token", new FaultCode("Unauthorized"));

        try
        {
            var handler = new JwtSecurityTokenHandler();
            var principal = handler.ValidateToken(token, _validationParameters, out var validatedToken);

            // Set authenticated principal
            Thread.CurrentPrincipal = principal;
            if (HttpContext.Current != null)
                HttpContext.Current.User = principal;

            // Store claims in OperationContext for downstream access
            OperationContext.Current.IncomingMessageProperties["Principal"] = principal;
        }
        catch (SecurityTokenException ex)
        {
            throw new FaultException($"Invalid token: {ex.Message}", new FaultCode("Unauthorized"));
        }

        return null;
    }

    public void BeforeSendReply(ref Message reply, object correlationState) { }

    private string ExtractBearerToken(Message request)
    {
        var authHeader = request.Headers.FindHeader("Authorization", "http://mycompany.com/");
        if (authHeader >= 0)
        {
            var value = request.Headers.GetHeader<string>(authHeader);
            if (value?.StartsWith("Bearer ") == true)
                return value.Substring(7);
        }
        return null;
    }
}
```

## 5. Authorization Invoker

```csharp
using System.Security.Claims;

public class AuthorizationOperationInvoker : IOperationInvoker
{
    private readonly IOperationInvoker _inner;
    private readonly string[] _requiredRoles;

    public AuthorizationOperationInvoker(IOperationInvoker inner, string[] requiredRoles)
    {
        _inner = inner;
        _requiredRoles = requiredRoles;
    }

    public bool IsSynchronous => _inner.IsSynchronous;

    public object[] AllocateInputs() => _inner.AllocateInputs();

    public object Invoke(object instance, object[] inputs, out object[] outputs)
    {
        var principal = Thread.CurrentPrincipal as ClaimsPrincipal;
        if (principal == null)
            throw new FaultException("No authenticated principal", new FaultCode("Forbidden"));

        // Check role-based authorization
        if (_requiredRoles != null && _requiredRoles.Length > 0)
        {
            var hasRole = _requiredRoles.Any(role => principal.IsInRole(role));
            if (!hasRole)
            {
                var correlationId = OperationContext.Current.IncomingMessageProperties["CorrelationId"];
                throw new FaultException(
                    $"Access denied. Required roles: {string.Join(", ", _requiredRoles)} [CorrelationId: {correlationId}]",
                    new FaultCode("Forbidden")
                );
            }
        }

        // Check claim-based authorization (example: tenant isolation)
        var tenantClaim = principal.FindFirst("tenant_id")?.Value;
        var requestedTenant = ExtractTenantFromInputs(inputs);
        if (!string.IsNullOrEmpty(requestedTenant) && tenantClaim != requestedTenant)
        {
            throw new FaultException("Access denied: tenant mismatch", new FaultCode("Forbidden"));
        }

        return _inner.Invoke(instance, inputs, out outputs);
    }

    public IAsyncResult InvokeBegin(object instance, object[] inputs, AsyncCallback callback, object state)
    {
        // Perform authorization check synchronously, then delegate
        Invoke(instance, inputs, out _); // This will throw if unauthorized
        return _inner.InvokeBegin(instance, inputs, callback, state);
    }

    public object InvokeEnd(object instance, out object[] outputs, IAsyncResult result)
    {
        return _inner.InvokeEnd(instance, out outputs, result);
    }

    private string ExtractTenantFromInputs(object[] inputs)
    {
        // Example: extract tenant ID from first parameter if it has a TenantId property
        var firstInput = inputs?.FirstOrDefault();
        return firstInput?.GetType().GetProperty("TenantId")?.GetValue(firstInput)?.ToString();
    }
}
```

## 6. Validation Parameter Inspector

```csharp
using FluentValidation;

public class ValidationParameterInspector : IParameterInspector
{
    private readonly IServiceProvider _serviceProvider;

    public ValidationParameterInspector(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public object BeforeCall(string operationName, object[] inputs)
    {
        foreach (var input in inputs)
        {
            if (input == null) continue;

            var validatorType = typeof(IValidator<>).MakeGenericType(input.GetType());
            var validator = _serviceProvider.GetService(validatorType) as IValidator;

            if (validator != null)
            {
                var context = new ValidationContext<object>(input);
                var result = validator.Validate(context);

                if (!result.IsValid)
                {
                    var errors = result.Errors.Select(e => new ValidationError
                    {
                        Field = e.PropertyName,
                        Message = e.ErrorMessage,
                        Code = e.ErrorCode
                    }).ToArray();

                    throw new FaultException<ValidationFault>(
                        new ValidationFault { Errors = errors },
                        new FaultReason("Validation failed")
                    );
                }
            }
        }

        return null;
    }

    public void AfterCall(string operationName, object[] outputs, object returnValue, object correlationState) { }
}

[DataContract]
public class ValidationFault
{
    [DataMember]
    public ValidationError[] Errors { get; set; }
}

[DataContract]
public class ValidationError
{
    [DataMember]
    public string Field { get; set; }

    [DataMember]
    public string Message { get; set; }

    [DataMember]
    public string Code { get; set; }
}
```

## 7. Resilience Invoker (Polly)

```csharp
using Polly;

public class ResilienceOperationInvoker : IOperationInvoker
{
    private readonly IOperationInvoker _inner;
    private readonly IAsyncPolicy _policy;

    public ResilienceOperationInvoker(IOperationInvoker inner)
    {
        _inner = inner;

        // Define retry policy for transient failures
        _policy = Policy
            .Handle<TimeoutException>()
            .Or<SqlException>(ex => IsTransient(ex))
            .WaitAndRetryAsync(
                retryCount: 3,
                sleepDurationProvider: attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)),
                onRetry: (exception, timespan, retryCount, context) =>
                {
                    // Log retry attempt
                    var correlationId = Activity.Current?.Id;
                    Console.WriteLine($"Retry {retryCount} after {timespan.TotalSeconds}s [CorrelationId: {correlationId}]");
                }
            );
    }

    public bool IsSynchronous => _inner.IsSynchronous;

    public object[] AllocateInputs() => _inner.AllocateInputs();

    public object Invoke(object instance, object[] inputs, out object[] outputs)
    {
        object[] capturedOutputs = null;
        var result = _policy.ExecuteAsync(async () =>
        {
            return await Task.Run(() => _inner.Invoke(instance, inputs, out capturedOutputs));
        }).GetAwaiter().GetResult();

        outputs = capturedOutputs;
        return result;
    }

    public IAsyncResult InvokeBegin(object instance, object[] inputs, AsyncCallback callback, object state)
    {
        return _policy.ExecuteAsync(async () =>
        {
            return await Task.Factory.FromAsync(
                _inner.InvokeBegin(instance, inputs, callback, state),
                asyncResult => _inner.InvokeEnd(instance, out _, asyncResult)
            );
        }).AsTask().ContinueWith(task => callback?.Invoke(task), state).GetAwaiter().GetResult();
    }

    public object InvokeEnd(object instance, out object[] outputs, IAsyncResult result)
    {
        return _inner.InvokeEnd(instance, out outputs, result);
    }

    private bool IsTransient(SqlException ex)
    {
        // SQL Server transient error codes
        int[] transientErrorNumbers = { -2, -1, 2, 20, 64, 233, 10053, 10054, 10060, 40197, 40501, 40613 };
        return ex.Errors.Cast<SqlError>().Any(error => transientErrorNumbers.Contains(error.Number));
    }
}
```

## 8. Exception Normalization Invoker

```csharp
public class ExceptionNormalizationInvoker : IOperationInvoker
{
    private readonly IOperationInvoker _inner;
    private readonly ILogger _logger;

    public ExceptionNormalizationInvoker(IOperationInvoker inner, ILogger logger)
    {
        _inner = inner;
        _logger = logger;
    }

    public bool IsSynchronous => _inner.IsSynchronous;

    public object[] AllocateInputs() => _inner.AllocateInputs();

    public object Invoke(object instance, object[] inputs, out object[] outputs)
    {
        try
        {
            return _inner.Invoke(instance, inputs, out outputs);
        }
        catch (FaultException)
        {
            // Already a fault, rethrow
            outputs = null;
            throw;
        }
        catch (Exception ex)
        {
            outputs = null;
            return HandleException(ex);
        }
    }

    private object HandleException(Exception ex)
    {
        var correlationId = Activity.Current?.Id ?? "unknown";

        // Log the full exception internally
        _logger.LogError(ex, "Operation failed [CorrelationId: {CorrelationId}]", correlationId);

        // Map to typed error code
        var (errorCode, message) = MapException(ex);

        // Return normalized fault (never expose internal details)
        throw new FaultException<ErrorEnvelope>(
            new ErrorEnvelope
            {
                ErrorCode = errorCode,
                Message = message,
                CorrelationId = correlationId,
                Timestamp = DateTimeOffset.UtcNow
            },
            new FaultReason(message)
        );
    }

    private (string ErrorCode, string Message) MapException(Exception ex)
    {
        return ex switch
        {
            ArgumentNullException => ("ERR_INVALID_INPUT", "Required parameter is missing"),
            ArgumentException => ("ERR_INVALID_INPUT", "Invalid parameter value"),
            UnauthorizedAccessException => ("ERR_FORBIDDEN", "Access denied"),
            KeyNotFoundException => ("ERR_NOT_FOUND", "Requested resource not found"),
            TimeoutException => ("ERR_TIMEOUT", "Operation timed out"),
            SqlException => ("ERR_DATABASE", "Database error occurred"),
            _ => ("ERR_INTERNAL", "An internal error occurred")
        };
    }

    public IAsyncResult InvokeBegin(object instance, object[] inputs, AsyncCallback callback, object state)
    {
        try
        {
            return _inner.InvokeBegin(instance, inputs, callback, state);
        }
        catch (Exception ex)
        {
            HandleException(ex);
            throw; // unreachable
        }
    }

    public object InvokeEnd(object instance, out object[] outputs, IAsyncResult result)
    {
        try
        {
            return _inner.InvokeEnd(instance, out outputs, result);
        }
        catch (FaultException)
        {
            outputs = null;
            throw;
        }
        catch (Exception ex)
        {
            outputs = null;
            return HandleException(ex);
        }
    }
}

[DataContract]
public class ErrorEnvelope
{
    [DataMember]
    public string ErrorCode { get; set; }

    [DataMember]
    public string Message { get; set; }

    [DataMember]
    public string CorrelationId { get; set; }

    [DataMember]
    public DateTimeOffset Timestamp { get; set; }
}
```

## Complete Behavior Registration

```csharp
public class EnterpriseInterceptorBehavior : IServiceBehavior
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILoggerFactory _loggerFactory;
    private readonly TokenValidationParameters _tokenValidation;

    public EnterpriseInterceptorBehavior(
        IServiceProvider serviceProvider,
        ILoggerFactory loggerFactory,
        TokenValidationParameters tokenValidation)
    {
        _serviceProvider = serviceProvider;
        _loggerFactory = loggerFactory;
        _tokenValidation = tokenValidation;
    }

    public void ApplyDispatchBehavior(ServiceDescription desc, ServiceHostBase host)
    {
        foreach (ChannelDispatcher cd in host.ChannelDispatchers)
        foreach (EndpointDispatcher ed in cd.Endpoints)
        {
            var runtime = ed.DispatchRuntime;

            // Message inspectors (layers 1-4)
            runtime.MessageInspectors.Add(new TelemetryMessageInspector());
            runtime.MessageInspectors.Add(new LoggingMessageInspector(_loggerFactory.CreateLogger<LoggingMessageInspector>()));
            runtime.MessageInspectors.Add(new CorrelationMessageInspector());
            runtime.MessageInspectors.Add(new AuthenticationMessageInspector(_tokenValidation));

            // Per-operation interceptors (layers 5-8)
            foreach (var op in runtime.Operations)
            {
                // Extract required roles from operation attributes
                var requiredRoles = ExtractRequiredRoles(op);

                // Wrap invoker (innermost first)
                var invoker = op.Invoker;
                invoker = new ExceptionNormalizationInvoker(invoker, _loggerFactory.CreateLogger<ExceptionNormalizationInvoker>());
                invoker = new ResilienceOperationInvoker(invoker);
                invoker = new AuthorizationOperationInvoker(invoker, requiredRoles);
                op.Invoker = invoker;

                // Parameter inspector for validation
                op.ParameterInspectors.Add(new ValidationParameterInspector(_serviceProvider));
            }
        }
    }

    public void AddBindingParameters(ServiceDescription desc, ServiceHostBase host, Collection<ServiceEndpoint> endpoints, BindingParameterCollection parameters) { }
    public void Validate(ServiceDescription desc, ServiceHostBase host) { }

    private string[] ExtractRequiredRoles(DispatchOperation op)
    {
        // Extract from custom attributes on service method
        // This is a simplified example
        return new[] { "User" }; // Default role
    }
}
```

These implementations are production-ready patterns. Adapt error handling, logging formats, and policy configurations to your specific requirements.
