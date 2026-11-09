---
metadata-version: "1.0.0"
title: "Roslyn VBD Generator Suite"
description: "Preserve scoped source guidance for roslyn-vbd-generator-suite."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Roslyn VBD Generator Suite

This skill helps you design and implement production-ready Roslyn source generators that enforce volatility-based decomposition (VBD) principles and automate enterprise architecture patterns.

## Core Philosophy

VBD generators exist to:
- **Enforce boundaries** — Prevent accidental coupling across volatility boundaries
- **Automate structure** — Generate complete service topologies from definitions
- **Ensure consistency** — Make correct architecture the path of least resistance
- **Eliminate boilerplate** — Generate repetitive patterns once, correctly

A good generator makes the right thing automatic and the wrong thing difficult.

## Quick Start

**For boundary generators:**
1. Identify the volatility boundary (what changes together)
2. Define the boundary contract (interface + DTOs)
3. Generate the full project set (Contract, Service, Access, Manager, Engine, Tests, UI, Deployment)
4. Wire dependencies according to VBD rules

**For specialized generators:**
1. Identify the repetitive pattern causing friction
2. Design the attribute/marker that triggers generation
3. Emit minimal, focused code that solves exactly that problem
4. Ensure generated code integrates cleanly with hand-written code

## Generator Architecture

All generators follow incremental generation patterns:

```csharp
[Generator]
public class YourGenerator : IIncrementalGenerator
{
    public void Initialize(IncrementalGeneratorInitializationContext context)
    {
        // 1. Filter to relevant syntax nodes
        var candidates = context.SyntaxProvider
            .CreateSyntaxProvider(
                predicate: static (node, _) => IsCandidateNode(node),
                transform: static (ctx, _) => TransformNode(ctx))
            .Where(static m => m is not null);

        // 2. Combine with compilation
        var combined = candidates.Combine(context.CompilationProvider);

        // 3. Generate output
        context.RegisterSourceOutput(combined, static (spc, source) => Execute(spc, source));
    }
}
```

**Key principles:**
- Use incremental pipelines — only regenerate what changed
- Filter early — reject irrelevant nodes in predicate
- Keep transforms pure and static when possible
- Emit one file per logical unit
- Use meaningful file names: `{TypeName}.g.cs` or `{BoundaryName}.{Component}.g.cs`

## Boundary Definition Patterns

VBD generators read boundary definitions from either attributes or JSON.

**Attribute-based:**
```csharp
[ServiceBoundary("Billing")]
public class BillingDefinition
{
    [Contract]
    public interface IBillingService { }

    [Entity]
    public class Invoice { }

    [Projection(ProjectionType.Vue)]
    public class InvoiceView { }

    [Deployment(DeploymentTarget.AppService)]
    public class BillingDeployment { }
}
```

**JSON-based:**
```json
{
  "name": "Billing",
  "contracts": ["IBillingService"],
  "entities": ["Invoice"],
  "ui": ["Vue"],
  "deployment": ["AppService", "KeyVault"]
}
```

Both produce the same output: a complete service boundary with all required projects.

## Project Topology

A complete VBD boundary generates:

```
{Boundary}.Contracts/        — Public interfaces + DTOs only
{Boundary}.Service/          — Engines (volatility-isolated logic)
{Boundary}.Manager/          — Orchestration layer
{Boundary}.Access/           — External dependencies (DB, APIs)
{Boundary}.Emulator/         — Offline testing doubles
{Boundary}.Simulator/        — Behavior modeling
{Boundary}.Tests/            — Regression harnesses
{Boundary}.UI.{Framework}/   — Frontend projection
{Boundary}.Deployment/       — Bicep infrastructure
```

**Dependency rules (enforced by analyzers):**
- Contracts: zero dependencies
- Service: depends on Contracts only
- Manager: depends on Service + Contracts
- Access: depends on Contracts only
- UI: depends on Contracts only
- Tests: depends on Contracts + Emulator

Cross-boundary references must go through Contracts only.

## Generator Catalog

See `references/generator-catalog.md` for the complete list of 100+ specialized generators across:
- Service boundaries and topology
- Domain modeling and aggregates
- Data access and persistence
- API and web scaffolding
- Frontend projections (Vue, Angular, MAUI, WPF, WinUI)
- Azure Bicep deployment
- Messaging and integration
- CLI tooling (Spectre.Console)
- Regression testing
- Configuration and DI

## Code Emission Patterns

See `references/emission-patterns.md` for:
- String interpolation vs. StringBuilder vs. syntax factories
- Namespace and using directive generation
- Attribute preservation and forwarding
- Nullable reference type handling
- XML documentation generation
- Partial class and method scaffolding

## Testing Generators

See `references/testing-strategies.md` for:
- Snapshot testing with Verify
- Incremental generator testing
- Compilation and semantic model validation
- Cross-project dependency verification
- Performance benchmarking

## Common Patterns

**Emit immutable DTOs:**
```csharp
public record {TypeName}(
    {string.Join(",\n    ", properties)}
);
```

**Emit registration methods:**
```csharp
public static IServiceCollection Add{BoundaryName}Services(
    this IServiceCollection services)
{
    services.AddScoped<I{Service}, {Service}>();
    return services;
}
```

**Emit boundary proxies:**
```csharp
public class {BoundaryName}Proxy : I{BoundaryName}Service
{
    private readonly HttpClient _client;
    // Only depends on contract, never on implementation
}
```

## Analyzer Integration

Generators should pair with analyzers that prevent violations:

- **VBD001**: Cross-boundary reference bypasses contract
- **VBD002**: UI project references Service implementation
- **VBD003**: Contract project has external dependencies
- **VBD004**: Manager directly calls Access (must go through Engine)

See `references/analyzer-patterns.md` for implementation guidance.

## Deployment Generation

Bicep generators emit infrastructure as code:

```bicep
resource {boundaryName}AppService 'Microsoft.Web/sites@2022-03-01' = {
  name: {boundaryName}AppServiceName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        { name: 'BoundaryName', value: '{boundaryName}' }
      ]
    }
  }
}
```

See `references/bicep-generation.md` for complete patterns.

## UI Projection Strategy

Frontend generators produce framework-specific projections from the same contract:

**Vue:** Components + Pinia stores + Axios clients
**Angular:** Components + services + reactive forms
**MAUI:** Pages + ViewModels + navigation
**WPF:** Views + ViewModels + commands
**WinUI:** Pages + ViewModels + bindings

See `references/ui-projections.md` for framework-specific patterns.

## Performance Considerations

- **Cache semantic models** — Don't recompute symbol information
- **Filter syntax early** — Reject 99% of nodes in predicate
- **Use static transforms** — Avoid closures in pipelines
- **Batch file generation** — One RegisterSourceOutput per logical group
- **Minimize allocations** — Reuse builders, avoid LINQ in hot paths

Generators run on every keystroke in the IDE. Keep them fast.

## Debugging Generators

Add to your `.csproj`:
```xml
<EmitCompilerGeneratedFiles>true</EmitCompilerGeneratedFiles>
<CompilerGeneratedFilesOutputPath>$(BaseIntermediateOutputPath)\GeneratedFiles</CompilerGeneratedFilesOutputPath>
```

Generated files appear in `obj/GeneratedFiles/` for inspection.

Attach debugger:
```csharp
#if DEBUG
if (!Debugger.IsAttached) Debugger.Launch();
#endif
```

## When to Generate vs. Hand-Write

**Generate when:**
- The pattern repeats 10+ times with minimal variation
- Correctness depends on mechanical consistency
- The structure enforces architectural boundaries
- Developers frequently get it wrong

**Hand-write when:**
- Logic is genuinely unique
- Flexibility matters more than consistency
- The pattern is still evolving
- Generated code would be harder to understand than hand-written

Generators are architecture enforcement tools, not a replacement for thought.

## Integration with Build

Generators are NuGet packages referenced as analyzers:

```xml
<ItemGroup>
  <ProjectReference Include="..\YourGenerator\YourGenerator.csproj"
                    OutputItemType="Analyzer"
                    ReferenceOutputAssembly="false" />
</ItemGroup>
```

Or packaged and distributed:
```xml
<ItemGroup>
  <PackageReference Include="YourCompany.Generators.VBD" Version="1.0.0"
                    PrivateAssets="all" />
</ItemGroup>
```

## Versioning and Evolution

Generators are part of your API surface:
- **Breaking change**: Altering generated code signatures that consumers depend on
- **Non-breaking**: Adding new generated members, improving internal implementation
- Version generator packages independently from the libraries they target
- Use `[GeneratedCode]` attributes to mark generated code with version info

## Resources

- **Generator Catalog**: `references/generator-catalog.md` — Full list of 100+ specialized generators
- **Emission Patterns**: `references/emission-patterns.md` — Code generation techniques and best practices
- **Testing Strategies**: `references/testing-strategies.md` — How to test generators thoroughly
- **Analyzer Patterns**: `references/analyzer-patterns.md` — Building analyzers that enforce VBD rules
- **Bicep Generation**: `references/bicep-generation.md` — Azure infrastructure generation patterns
- **UI Projections**: `references/ui-projections.md` — Framework-specific frontend generation
- **VBD Principles**: `references/vbd-principles.md` — Understanding volatility-based decomposition

Start with the generator catalog to find the pattern closest to your needs, then adapt.
