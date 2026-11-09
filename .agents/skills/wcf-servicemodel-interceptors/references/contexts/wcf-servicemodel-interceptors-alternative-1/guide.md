---
metadata-version: "1.0.0"
title: "WCF/ServiceModel Interceptors"
description: "Preserve scoped source guidance for wcf-servicemodel-interceptors."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# WCF/ServiceModel Interceptors

## Overview

Enterprise WCF/CoreWCF services require deterministic, layered interceptor pipelines to handle cross-cutting concerns: observability, security, validation, and resilience. This skill defines the **eight-layer interceptor stack** for production systems, correct ordering rationale, implementation patterns, and mapping to Volatility-Based Decomposition (VBD) Manager→Engine→Access architectures.

The interceptor model applies to both classic WCF (.NET Framework) and CoreWCF (.NET 6+), using `IDispatchMessageInspector`, `IOperationInvoker`, `IParameterInspector`, and behavior extensibility.

## The Eight-Layer Stack (Critical Ordering)

### 1. Telemetry (Distributed Tracing)

**Position:** Outermost layer
**Why first:** Must wrap the entire call chain to measure end-to-end latency and emit complete spans.

**Responsibilities:**

- Start/stop `Activity` (`ActivitySource`) per operation
- Emit OpenTelemetry traces with operation name, caller identity, correlation ID
- Attach baggage for cross-service propagation
- Emit metrics: request count, duration, failure rate

**Implementation:**

- `IDispatchMessageInspector.AfterReceiveRequest`: Start activity, extract trace context from headers
- `IDispatchMessageInspector.BeforeSendReply`: Stop activity, record duration, emit span
- CoreWCF: Use `AddSource("CoreWCF.Primitives")` for built-in instrumentation
- Classic WCF: Implement custom `IDispatchMessageInspector` with `System.Diagnostics.Activity`

**Rationale:** Telemetry wraps everything else—if authorization fails, the trace still captures the rejection. If resilience retries, the trace shows all attempts.

---

### 2. Logging (Structured Logging)

**Position:** Second layer
**Why here:** Logs the request envelope before any transformations or failures occur.

**Responsibilities:**

- Log request envelope: operation name, parameter hash (never raw PII), caller identity, correlation ID
- Log response envelope: status, duration, response size
- Log exceptions with full stack, correlation ID, and causation chain
- Enforce structured logging (JSON, never free-form text)

**Implementation:**

- `IDispatchMessageInspector.AfterReceiveRequest`: Log inbound request metadata
- `IDispatchMessageInspector.BeforeSendReply`: Log outbound response metadata
- Use `ILogger<T>` with structured properties, not string interpolation

**Rationale:** Logging sits inside telemetry (so log entries inherit trace context) but outside security checks (so unauthorized attempts are logged).

---

### 3. Correlation (Request Identity)

**Position:** Third layer
**Why here:** Every downstream layer and log entry must reference a stable correlation ID.

**Responsibilities:**

- Generate `CorrelationId` if missing (GUID or trace ID)
- Propagate `CorrelationId` to downstream services via headers/message properties
- Attach `CausationId` for nested calls (parent operation ID)
- Store in `OperationContext.Current` or message properties for access in all layers

**Implementation:**

- `IDispatchMessageInspector.AfterReceiveRequest`: Extract or generate correlation ID, inject into context
- Attach to outbound calls via `IClientMessageInspector.BeforeSendRequest`

**Rationale:** Correlation must be established early so authentication, authorization, and validation failures can be traced back to the originating request.

---

### 4. Authentication (Identity Establishment)

**Position:** Fourth layer
**Why here:** Identity must be validated before any authorization or business logic.

**Responsibilities:**

- Validate JWT, certificate, or token
- Extract identity claims (user ID, roles, tenant ID)
- Attach identity to `OperationContext` or `Thread.CurrentPrincipal`
- Reject unauthenticated calls with `401 Unauthorized` before reaching business logic

**Implementation:**

- `IDispatchMessageInspector.AfterReceiveRequest`: Validate token, extract claims, set principal
- Throw `SecurityException` or return fault for invalid tokens

**Rationale:** Authentication precedes authorization—you can't check permissions until you know who the caller is.

---

### 5. Authorization (Policy Enforcement)

**Position:** Fifth layer
**Why here:** Once identity is established, enforce access rules before validation or execution.

**Responsibilities:**

- Evaluate role-based or claim-based policies
- Enforce operation-level permissions (e.g., `[Authorize(Roles = "Admin")]`)
- Enforce resource-level permissions (e.g., "Can user X access tenant Y?")
- Emit `403 Forbidden` with correlation ID for policy violations

**Implementation:**

- `IOperationInvoker.Invoke`: Check policies before invoking the operation
- Alternatively, use `IParameterInspector.BeforeCall` to inspect resource IDs and validate access

**Rationale:** Authorization sits inside authentication (identity required) but outside validation (no point validating payloads the caller can't access).

---

### 6. Validation (Contract Integrity)

**Position:** Sixth layer
**Why here:** Validate request DTOs after authorization but before business logic.

**Responsibilities:**

- Validate `DataContract`/`DataMember` rules (required fields, string lengths, ranges)
- Validate business invariants (e.g., "start date must precede end date")
- Reject malformed or incomplete requests with `400 Bad Request`
- Emit validation errors in a normalized format (typed error codes, field names)

**Implementation:**

- `IParameterInspector.BeforeCall`: Validate parameters before operation invocation
- Use FluentValidation or DataAnnotations
- Return `FaultException<ValidationFault>` with structured error details

**Rationale:** Validation happens after authorization (authorized users get better error messages) but before resilience (no point retrying invalid requests).

---

### 7. Resilience (Retries, Circuit Breakers, Timeouts)

**Position:** Seventh layer
**Why here:** Wraps the actual operation invocation to handle transient failures.

**Responsibilities:**

- Apply retry policies (exponential backoff for transient errors)
- Apply circuit breaker rules (stop calling failing downstream services)
- Apply per-operation timeouts
- Emit resilience metrics (retry count, circuit state, timeout occurrences)

**Implementation:**

- `IOperationInvoker.Invoke`: Wrap `innerInvoker.Invoke()` with Polly policies
- Differentiate retriable errors (transient DB failures) from non-retriable (validation errors)

**Rationale:** Resilience wraps the operation itself—retries only make sense after validation passes. Circuit breakers prevent cascading failures to downstream systems.

---

### 8. Exception Normalization (Enterprise Error Envelope)

**Position:** Innermost layer (wraps operation execution)
**Why last:** Catches all exceptions from the operation and converts them to a deterministic error contract.

**Responsibilities:**

- Catch all exceptions (business, validation, infrastructure)
- Map to typed error codes (e.g., `ERR_VALIDATION`, `ERR_NOT_FOUND`, `ERR_INTERNAL`)
- Wrap in a normalized error contract (e.g., `FaultException<ErrorEnvelope>`)
- Attach correlation ID to every error
- Prevent leaking internal details (stack traces, connection strings) over the wire

**Implementation:**

- `IErrorHandler.ProvideFault`: Convert exceptions to fault messages
- `IOperationInvoker.Invoke`: Catch exceptions, map to typed faults
- Return consistent structure: `{ "errorCode": "ERR_VALIDATION", "message": "...", "correlationId": "..." }`

**Rationale:** Exception normalization is the last line of defense—it ensures no raw exceptions escape the service boundary. Clients receive predictable, actionable error messages.

---

## Ordering Rationale Summary

| Layer                          | Why This Order                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------ |
| **1. Telemetry**               | Wraps everything—must capture full request lifecycle, including failures       |
| **2. Logging**                 | Logs raw request before transformations; inherits trace context from telemetry |
| **3. Correlation**             | Establishes request identity for all downstream layers and logs                |
| **4. Authentication**          | Identity must be validated before authorization or business logic              |
| **5. Authorization**           | Permissions checked after identity established, before validation              |
| **6. Validation**              | Validate payloads only for authorized users, before expensive operations       |
| **7. Resilience**              | Wraps operation invocation; retries only make sense after validation passes    |
| **8. Exception Normalization** | Innermost layer—catches all exceptions and converts to normalized faults       |

**Key principle:** Outer layers handle infrastructure concerns (observability, identity), inner layers handle business concerns (validation, execution). Failures at any layer are captured by telemetry and logging.

---

## Implementation Patterns

### IDispatchMessageInspector (Message-Level)

Use for telemetry, logging, correlation, authentication.

```csharp
public class TelemetryInspector : IDispatchMessageInspector
{
    private readonly ActivitySource activitySource;

    public TelemetryInspector(ActivitySource activitySource)
    {
        this.activitySource = activitySource;
    }

    public object AfterReceiveRequest(ref Message request, IClientChannel channel, InstanceContext instanceContext)
    {
        var activity = activitySource.StartActivity("WCF Operation", ActivityKind.Server);
        activity?.SetTag("operation", request.Headers.Action);
        // Extract trace context from headers, set baggage
        return activity; // correlation state
    }

    public void BeforeSendReply(ref Message reply, object correlationState)
    {
        if (correlationState is Activity activity)
        {
            activity.SetTag("status", reply.IsFault ? "fault" : "success");
            activity.Stop();
        }
    }
}
```

### IOperationInvoker (Operation-Level)

Use for authorization, resilience, exception normalization.

```csharp
public class ResilienceInvoker : IOperationInvoker
{
    private readonly IOperationInvoker inner;
    private readonly IAsyncPolicy policy;

    public ResilienceInvoker(IOperationInvoker inner, IAsyncPolicy policy)
    {
        this.inner = inner;
        this.policy = policy;
    }

    public object Invoke(object instance, object[] inputs, out object[] outputs)
    {
        return policy.Execute(() => inner.Invoke(instance, inputs, out outputs));
    }

    // Implement InvokeBegin/InvokeEnd for async operations
}
```

### IParameterInspector (Parameter-Level)

Use for validation.

```csharp
public class ValidationInspector : IParameterInspector
{
    public object BeforeCall(string operationName, object[] inputs)
    {
        foreach (var input in inputs)
        {
            var validationResults = Validate(input);
            if (!validationResults.IsValid)
                throw new FaultException<ValidationFault>(new ValidationFault(validationResults));
        }
        return null;
    }

    public void AfterCall(string operationName, object[] outputs, object returnValue, object correlationState) { }
}
```

### Behavior Registration

Interceptors attach via behaviors:

```csharp
public class InterceptorBehavior : IServiceBehavior
{
    public void ApplyDispatchBehavior(ServiceDescription desc, ServiceHostBase host)
    {
        foreach (ChannelDispatcher cd in host.ChannelDispatchers)
        foreach (EndpointDispatcher ed in cd.Endpoints)
        {
            // Add message inspectors
            ed.DispatchRuntime.MessageInspectors.Add(new TelemetryInspector());
            ed.DispatchRuntime.MessageInspectors.Add(new LoggingInspector());
            ed.DispatchRuntime.MessageInspectors.Add(new CorrelationInspector());
            ed.DispatchRuntime.MessageInspectors.Add(new AuthenticationInspector());

            // Add operation invokers (per operation)
            foreach (var op in ed.DispatchRuntime.Operations)
            {
                op.Invoker = new AuthorizationInvoker(op.Invoker);
                op.Invoker = new ResilienceInvoker(op.Invoker);
                op.Invoker = new ExceptionNormalizationInvoker(op.Invoker);

                // Add parameter inspectors
                op.ParameterInspectors.Add(new ValidationInspector());
            }
        }
    }
}
```

Register via config or code:

```xml
<system.serviceModel>
  <behaviors>
    <serviceBehaviors>
      <behavior>
        <interceptorBehavior />
      </behavior>
    </serviceBehaviors>
  </behaviors>
  <extensions>
    <behaviorExtensions>
      <add name="interceptorBehavior" type="MyNamespace.InterceptorBehaviorExtension, MyAssembly" />
    </behaviorExtensions>
  </extensions>
</system.serviceModel>
```

---

## Mapping to VBD Architecture

In this repository, **VBD means Volatility-Based Decomposition**. The eight interceptor layers execute at the ServiceModel boundary (typically hosted by a Manager-facing service endpoint), while responsibilities still align to Manager/Engine/Access boundaries.

**ServiceModel boundary (hosted endpoint):**

- Telemetry
- Logging
- Correlation
- Authentication

**Manager responsibility boundary:**

- Authorization
- Validation
- Exception Normalization

**Engine/Access call path:**

- Resilience (timeouts/retries/circuit breaking) wraps downstream calls invoked by Managers and Engines

**Engine layer:**

- Business rules and transformations (no transport-specific interceptor dependency)

**Access layer:**

- External resource calls (data/API/queue), invoked through contracts and wrapped by resilience policies

This organization ensures:

- Transport concerns (tracing, auth) stay at the edge
- Business logic (authorization, validation) lives in Managers
- Infrastructure resilience (retries, circuit breakers, timeouts) wraps downstream operations without leaking transport concerns into domain logic

---

## CoreWCF Specifics

**Built-in OpenTelemetry:**
CoreWCF 1.5+ includes native OpenTelemetry support:

```csharp
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing => tracing.AddSource("CoreWCF.Primitives"));
```

This automatically emits traces for all operations. For custom enrichment:

```csharp
tracing.AddWcfInstrumentation(options =>
{
    options.Enrich = (activity, eventName, message) =>
    {
        if (eventName == WcfEnrichEventNames.AfterReceiveRequest)
            activity.SetTag("custom.tenant", message.Properties["TenantId"]);
    };
});
```

**Async Operations:**
CoreWCF supports `async`/`await`. Ensure `IOperationInvoker` implementations handle async correctly:

```csharp
public IAsyncResult InvokeBegin(object instance, object[] inputs, AsyncCallback callback, object state)
{
    // Wrap with async policy
    return policy.ExecuteAsync(() => inner.InvokeBegin(instance, inputs, callback, state));
}
```

---

## Common Mistakes

**Wrong ordering:**

- Validation before authorization → leaks information to unauthorized callers
- Resilience outside telemetry → retries not captured in traces
- Logging after authentication → failed auth attempts not logged

**Leaking internal details:**

- Returning raw exception messages over the wire
- Exposing stack traces or connection strings in faults

**Missing correlation:**

- Not propagating correlation IDs to downstream services
- Logs without correlation IDs are useless in distributed systems

**Blocking async operations:**

- Using `.Result` or `.Wait()` in `IOperationInvoker` causes deadlocks
- Always implement `InvokeBegin`/`InvokeEnd` for async operations

---

## Example: Complete Interceptor Stack

```csharp
public class EnterpriseInterceptorBehavior : IServiceBehavior
{
    public void ApplyDispatchBehavior(ServiceDescription desc, ServiceHostBase host)
    {
        foreach (ChannelDispatcher cd in host.ChannelDispatchers)
        foreach (EndpointDispatcher ed in cd.Endpoints)
        {
            var runtime = ed.DispatchRuntime;

            // Layer 1-4: Message inspectors (ordered)
            runtime.MessageInspectors.Add(new TelemetryInspector());
            runtime.MessageInspectors.Add(new LoggingInspector());
            runtime.MessageInspectors.Add(new CorrelationInspector());
            runtime.MessageInspectors.Add(new AuthenticationInspector());

            // Layer 5-8: Operation invokers and parameter inspectors (per operation)
            foreach (var op in runtime.Operations)
            {
                // Wrap invoker in reverse order (innermost first)
                var invoker = op.Invoker;
                invoker = new ExceptionNormalizationInvoker(invoker);      // Layer 8
                invoker = new ResilienceInvoker(invoker);                   // Layer 7
                invoker = new AuthorizationInvoker(invoker);                // Layer 5
                op.Invoker = invoker;

                // Layer 6: Validation
                op.ParameterInspectors.Add(new ValidationInspector());
            }
        }
    }
}
```

---

## Key Takeaways

1. **Eight layers, strict order:** Telemetry → Logging → Correlation → Authentication → Authorization → Validation → Resilience → Exception Normalization.
2. **Rationale matters:** Each layer depends on the previous ones. Wrong order breaks observability, security, or reliability.
3. **Message inspectors for infrastructure:** Telemetry, logging, correlation, authentication.
4. **Operation invokers for business logic:** Authorization, resilience, exception normalization.
5. **Parameter inspectors for validation:** Validate inputs before operation invocation.
6. **Map to VBD layers:** Transport handles observability/auth, Manager handles authorization/validation, Engine handles resilience.
7. **CoreWCF modernization:** Use built-in OpenTelemetry, async invokers, and .NET 6+ patterns.

This stack is proven in high-throughput, distributed systems. It ensures deterministic behavior, complete observability, and defense-in-depth security.
