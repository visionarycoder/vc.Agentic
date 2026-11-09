---
name: "ifx-proxies-interceptors"
description: "Route cross-cutting concern requests to existing Ifx.Proxies interceptors instead of hand-rolled code for boundary-intercepted services in this repository."
metadata:
  metadata-version: "1.0.0"
  title: "Ifx.Proxies Interceptor Routing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Ifx.Proxies Interceptor Routing

Agent checks this table before writing new cross-cutting logic in `AzureAPI/src/` or `src/`. `Ifx.Proxies` implements these concerns as boundary-proxy interceptors. Agent reuses the existing attribute or interceptor instead of duplicating the concern in application code.

## When to Use

| Condition | Use |
|---|---|
| Developer or agent adds caching, retry, timeout, circuit breaking, authentication, redaction, sanitization, idempotency, correlation, rate limiting, telemetry, or validation to a service behind `AddBoundaryInterceptedScoped<TContract,TImplementation>()` | Use this skill |
| A task description mentions "cache this call," "retry on failure," "add auth to this method," "mask this field in logs," "prevent duplicate calls," or "throttle this endpoint" for a boundary-intercepted contract | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Target type is not registered through `AddBoundaryInterceptedScoped` and adding that registration is out of scope | Implement the concern directly with the matching generic skill in `related_skills` |
| Concern is HTTP-request-level rather than method-call-level | Use `rate-limiting-aspnetcore`, `cors-configuration-aspnetcore`, or `health-checks-aspnetcore` |
| Concern needs a wholly new interceptor category | Add the new interceptor under `src\ifx\Ifx\Proxies\Interceptors\<Concern>\`, then update this table |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Target contract interface | Yes | Must be registered through `AddBoundaryInterceptedScoped<TContract,TImplementation>()` |
| Cross-cutting concern | Yes | One row from the Decision Table |
| Configuration values | Yes | Attribute constructor arguments such as duration, thresholds, or scheme |

## Decision Table

| Developer intent | Avoid | Use instead | Location |
|---|---|---|---|
| Cache an expensive read-through call | Inline `IMemoryCache` or `HybridCache` calls in the service | `[Cacheable(durationSeconds, tier, maximumPayloadBytes, tags)]` on the contract method or interface | `Interceptors\Caching\CacheableAttribute.cs` |
| Override the cache key for a method | Custom key-building code | `[CacheKeyResolver(typeof(TResolver))]` implementing `ICacheKeyResolver` | `Interceptors\Caching\ICacheKeyResolver.cs` |
| Retry a transient failure | Manual `Task.Delay` retry loops | `[Retry(maxAttempts, delayMilliseconds)]` | `Interceptors\Retry\RetryAttribute.cs` |
| Bound the duration of a call | Manual timeout wiring | `[Timeout(milliseconds)]` | `Interceptors\Timeout\TimeoutAttribute.cs` |
| Stop cascading failures to a failing dependency | Manual failure counter or state machine | `[CircuitBreaker(failureThreshold, breakSeconds, samplingSeconds, minimumThroughput, failureRatio)]` | `Interceptors\CircuitBreaker\CircuitBreakerAttribute.cs` |
| Validate a bearer token, API key, mTLS certificate, or OIDC/Entra ID identity | New authentication middleware or inline token parsing | `[AuthenticationScheme(AuthenticationSchemeKind.Jwt \| OpenIdConnect \| EntraId \| ApiKey \| MutualTls \| Anonymous)]` resolving a keyed `IAuthenticationSchemeValidator` | `Interceptors\Authentication\AuthenticationSchemeAttribute.cs` |
| Require an authorization check before invocation | Inline `IAuthorizationService` calls in the service | `[RequireAuthorization(...)]` | `Interceptors\Authorization\RequireAuthorizationAttribute.cs` |
| Mask sensitive output in logs or telemetry | Ad hoc string scrubbing or regex | `ISensitive` and `[Sensitive]` consumed by `IRedactor` and `AttributeRedactor` | `Ifx.Abstractions\Attributes\SensitiveAttribute.cs`, `Ifx\Redaction\` |
| Neutralize untrusted input | Manual encoding scattered across services | `[Sanitize(strategy)]` on method or parameter, resolving `ISanitizationStrategy` | `Ifx.Abstractions\Attributes\SanitizeAttribute.cs`, `Interceptors\Sanitization\` |
| Prevent duplicate side effects from a retried call | Manual dedupe table or flag | `[Idempotent]` backed by `IIdempotencyStore` and `IIdempotencyKeyResolver` | `Interceptors\Idempotency\IdempotentAttribute.cs` |
| Correlate a call chain end-to-end with timing metadata | Custom envelope types | `System.Diagnostics.Activity` through `ProxyActivitySource` and `CorrelationInterceptor` | `Interceptors\Correlation\` |
| Emit call metrics and traces | Manual `Stopwatch` and custom log lines | `TelemetryInterceptor` using `ProxyTelemetryMeter` and `Activity.Current` tags | `Interceptors\Telemetry\` |
| Validate method arguments against data annotation rules | Manual argument validation | `ValidationInterceptor` using `Microsoft.Extensions.Validation` and `[ValidatableType]` | `Interceptors\Validation\ValidationInterceptor.cs` |
| Throttle call rate per caller or method | Hand-rolled token bucket or sliding-window counter | `[RateLimit(algorithm, permitLimit, windowSeconds, ...)]` resolving a cached `PartitionedRateLimiter<string>` (`System.Threading.RateLimiting`); override the partition key via `[RateLimitPartitionKeyResolver]` | `Interceptors\RateLimiting\RateLimitAttribute.cs` |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Match the requested concern against the Decision Table. | Read the developer's stated intent. | One row matches. |
| 2 | Confirm the target contract is or will be registered through `AddBoundaryInterceptedScoped`. | Search for `AddBoundaryInterceptedScoped<TContract` in the caller's DI setup. | Registration exists or the change adds it. |
| 3 | Apply the attribute from the matched row to the contract method or interface. | Read the attribute constructor signature in its source file. | Arguments compile with correct types. |
| 4 | Build the affected project. | Run the relevant `dotnet build` command. | Zero compile errors. |
| 5 | Run the matching interceptor tests when they exist. | Run the relevant unit test project. | Zero failing tests. |

## Verification Checklist

- [ ] Agent checked this table before writing new cross-cutting logic for a boundary-intercepted contract.
- [ ] Agent applied the existing attribute rather than duplicating interceptor logic in application code.
- [ ] Agent did not introduce a second caching, retry, auth, redaction, sanitization, idempotency, correlation, rate limiting, telemetry, or validation mechanism alongside an existing interceptor for the same contract.
- [ ] Agent updated this table when adding a new interceptor category.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| New service adds its own retry, cache, auth, or redaction logic instead of an attribute | Remove the inline logic and apply the matching Ifx.Proxies attribute |
| Redaction and sanitization are treated as the same concern | Redaction masks sensitive output; sanitization neutralizes untrusted input |
| A new interceptor is added without a row in this table | Add the row so future agents discover it |
| Cache/retry/auth override attribute is duplicated per call site | Apply the attribute once at the interface level; override at the method level only when the method differs |
