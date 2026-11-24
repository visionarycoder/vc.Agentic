---
name: "api-versioning-aspnetcore"
description: "Configure ASP.NET Core API versioning with URL, header, or query readers plus deprecation and Sunset signaling."
metadata:
  metadata-version: "1.0.0"
  title: "ASP.NET Core API Versioning"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# ASP.NET Core API Versioning

Configure explicit API version negotiation with `Asp.Versioning.Http` and compatibility signaling for ASP.NET Core endpoints.

## When to Use

| Condition | Agent Action |
|---|---|
| Public or partner API introduces a breaking contract change | Use this skill |
| API needs URL, header, or query string version negotiation | Use this skill |
| API lifecycle needs deprecation and Sunset signaling | Use this skill |
| Endpoint set needs parallel v1 and v2 behavior during migration | Use this skill |

## When Not to Use

Additive changes, non-HTTP transports, and internal endpoints without external callers.

## Required Inputs

Reader strategy, baseline version and default behavior, compatibility scope, and optional deprecation schedule (retirement date, migration link).

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1 | Select one negotiation strategy or one combined reader and records the default-version rule. | Read service registration. | Version readers and default-version behavior are explicit. |
| 2 | Agent registers `AddApiVersioning()` and version metadata on controllers or minimal API endpoint sets. | Run `rg -n "AddApiVersioning|ApiVersion|MapToApiVersion|WithApiVersionSet" <scope>`. | Service registration and endpoint version metadata both exist. |
| 3 | Separate behavior by version only where the contract breaks. | Read handlers or controllers for changed endpoints. | Breaking behavior maps to a distinct version. |
| 4 | Agent reports supported and deprecated versions in response headers. | Call versioned endpoints and inspect headers. | Response headers expose supported and deprecated versions. |
| 5 | Add deprecation and Sunset signaling for retiring versions. | Call a deprecated version and inspect headers. | Deprecated responses include deprecation and Sunset metadata. |
| 6 | Agent runs targeted compatibility checks across active versions. | Run existing API tests or scripted HTTP calls for each active version. | Each active version returns the intended contract and route mapping. |

## Implementation Patterns

```csharp
using Asp.Versioning;

builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = false;
    options.ReportApiVersions = true;
    options.ApiVersionReader = ApiVersionReader.Combine(
        new UrlSegmentApiVersionReader(),
        new HeaderApiVersionReader("api-version"),
        new QueryStringApiVersionReader("api-version"));
});

var ordersVersionSet = app.NewApiVersionSet()
    .HasApiVersion(new ApiVersion(1, 0))
    .HasApiVersion(new ApiVersion(2, 0))
    .ReportApiVersions()
    .Build();

app.MapGroup("/api/v{version:apiVersion}/orders")
    .WithApiVersionSet(ordersVersionSet)
    .MapGet("/", GetOrdersV1).MapToApiVersion(new ApiVersion(1, 0));
```

```csharp
app.Use(async (context, next) =>
{
    await next();
    if (context.GetRequestedApiVersion() == new ApiVersion(1, 0))
    {
        context.Response.Headers.Append("Deprecation", "true");
        context.Response.Headers.Append("Sunset", "Wed, 31 Dec 2026 23:59:59 GMT");
    }
});
```

## Rules

| Rule | Agent Verifies | Fix |
|---|---|---|
| AV-001 | One breaking contract change maps to one explicit version boundary. | Split divergent behavior into distinct versioned handlers. |
| AV-002 | Version negotiation logic stays explicit and documented in code. | Configure one reader or one combined reader in `AddApiVersioning()`. |
| AV-003 | Default version behavior matches the compatibility policy. | Set `AssumeDefaultVersionWhenUnspecified` and `DefaultApiVersion` intentionally. |
| AV-004 | Deprecated versions emit both report headers and lifecycle metadata. | Enable `ReportApiVersions` and append deprecation or Sunset headers. |
| AV-005 | Active versions keep independent route or handler mapping. | Add `MapToApiVersion()` or controller attributes per version. |
| AV-006 | OpenAPI grouping matches the active version set when API docs are in scope. | Add version-aware API explorer configuration. |

## Outputs

- Explicit API version reader configuration
- Versioned controller or minimal API endpoint mappings
- Deprecation and Sunset response signaling for retiring versions
- Compatibility verification across every active version
