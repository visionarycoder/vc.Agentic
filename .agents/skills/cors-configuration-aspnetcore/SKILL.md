---
name: "cors-configuration-aspnetcore"
description: "Configure ASP.NET Core CORS policies with explicit origins, preflight behavior, credentials handling, and secure wildcard avoidance."
metadata:
  metadata-version: "1.0.0"
  title: "ASP.NET Core CORS Configuration"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# ASP.NET Core CORS Configuration

Agent configures ASP.NET Core CORS with explicit origin policies, correct preflight handling, and safe credential behavior.

Use for browser callers of an ASP.NET Core API from another origin. Skip server-to-server callers; replace any requirement for a wildcard origin with credentials by explicit trusted origins.

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Allowed origins | Yes | Exact scheme, host, and port values |
| Methods and headers | Yes | Allowed request surface for preflight and actual requests |
| Credential behavior | Yes | Cookie or auth-header use and matching origin rule |
| Scope | No | Global, controller, endpoint, or route-group policy application |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1 | Agent records the browser callers and exact origins. | Read configuration and policy names. | Every trusted origin is explicit. |
| 2 | Agent defines named CORS policies in `AddCors()`. | Run `rg -n "AddCors|WithOrigins|AllowAnyOrigin|AllowCredentials|SetIsOriginAllowed" <scope>`. | Service registration contains the intended named policies. |
| 3 | Agent applies `UseCors()` or endpoint-level policy mapping in the correct pipeline position. | Read `Program.cs`. | CORS runs before endpoint execution and aligns to the chosen scope. |
| 4 | Agent verifies preflight behavior for methods, headers, and max age. | Send `OPTIONS` preflight requests. | Preflight responses contain the intended allow headers. |
| 5 | Agent verifies credential behavior against explicit origins. | Send credentialed cross-origin requests. | Responses use explicit origin echo and credential header behavior that matches the policy. |
| 6 | Agent validates denial paths for disallowed origins. | Send the same requests from an untrusted origin. | Browser-facing CORS headers stay absent for denied origins. |

## Implementation Patterns

### Named Policy Registration

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("spa-client", policy =>
    {
        policy.WithOrigins(
                "https://portal.contoso.com",
                "https://admin.contoso.com")
            .AllowAnyMethod()
            .AllowAnyHeader()
            .AllowCredentials()
            .SetPreflightMaxAge(TimeSpan.FromMinutes(30));
    });

    options.AddPolicy("public-read", policy =>
    {
        policy.WithOrigins("https://docs.contoso.com")
            .WithMethods("GET")
            .WithHeaders("Accept", "Content-Type");
    });
});
```

### Pipeline and Endpoint Scope

```csharp
app.UseRouting();
app.UseCors();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.MapGroup("/partner")
    .RequireCors("spa-client")
    .MapGet("/status", () => Results.Ok());
```

## Rules

| Rule | Agent Verifies | Fix |
|---|---|---|
| CORS-001 | Policy lists exact trusted origins for credentialed requests. | Replace wildcard origin rules with `WithOrigins(...)`. |
| CORS-002 | `AllowAnyOrigin()` and `AllowCredentials()` never appear together. | Use explicit origins for credentialed flows. |
| CORS-003 | CORS middleware order matches routing and auth flow requirements. | Place `UseCors()` after routing setup and before auth or endpoint execution. |
| CORS-004 | Preflight allows only the methods and headers the caller needs. | Replace broad allow rules with explicit methods or headers where the prompt calls for restriction. |
| CORS-005 | Denied origins do not receive success-shaping CORS headers. | Narrow the policy scope or allowed origin list. |
| CORS-006 | Non-browser integrations do not drive unnecessary CORS expansion. | Keep CORS rules focused on browser callers only. |

