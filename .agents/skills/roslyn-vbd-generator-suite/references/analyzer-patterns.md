# Analyzer Patterns for VBD Enforcement

Analyzers detect and prevent violations of volatility-based decomposition principles at compile time.

## Core VBD Violations

### VBD001: Cross-Boundary Reference Bypasses Contract

**Rule:** UI, Manager, or external projects must reference only Contract projects, never Service implementations.

```csharp
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public class CrossBoundaryReferenceAnalyzer : DiagnosticAnalyzer
{
    private static readonly DiagnosticDescriptor Rule = new(
        id: "VBD001",
        title: "Cross-boundary reference bypasses contract",
        messageFormat: "Type '{0}' references implementation '{1}' directly. Use contract interface instead.",
        category: "Architecture",
        defaultSeverity: DiagnosticSeverity.Error,
        isEnabledByDefault: true);

    public override void Initialize(AnalysisContext context)
    {
        context.RegisterSymbolAction(AnalyzeNamedType, SymbolKind.NamedType);
    }

    private void AnalyzeNamedType(SymbolAnalysisContext context)
    {
        var type = (INamedTypeSymbol)context.Symbol;
        var projectName = context.Compilation.AssemblyName;

        // Skip if in same boundary
        if (IsInSameBoundary(type, projectName)) return;

        // Check all field/property types
        foreach (var member in type.GetMembers())
        {
            var memberType = GetMemberType(member);
            if (memberType is null) continue;

            if (IsImplementationType(memberType) && !IsContractType(memberType))
            {
                context.ReportDiagnostic(Diagnostic.Create(
                    Rule,
                    member.Locations[0],
                    type.Name,
                    memberType.Name));
            }
        }
    }
}
```

### VBD002: Contract Project Has External Dependencies

**Rule:** Contract projects must have zero dependencies except BCL.

```csharp
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public class ContractPurityAnalyzer : DiagnosticAnalyzer
{
    private static readonly DiagnosticDescriptor Rule = new(
        id: "VBD002",
        title: "Contract project has external dependencies",
        messageFormat: "Contract project references '{0}'. Contracts must have zero external dependencies.",
        category: "Architecture",
        defaultSeverity: DiagnosticSeverity.Error,
        isEnabledByDefault: true);

    public override void Initialize(AnalysisContext context)
    {
        context.RegisterCompilationAction(AnalyzeCompilation);
    }

    private void AnalyzeCompilation(CompilationAnalysisContext context)
    {
        if (!IsContractProject(context.Compilation.AssemblyName)) return;

        foreach (var reference in context.Compilation.References)
        {
            if (reference is not CompilationReference compRef) continue;

            var refName = compRef.Compilation.AssemblyName;
            if (IsExternalDependency(refName))
            {
                context.ReportDiagnostic(Diagnostic.Create(
                    Rule,
                    Location.None,
                    refName));
            }
        }
    }
}
```

### VBD003: Manager Directly Calls Access

**Rule:** Managers orchestrate Engines; only Engines call Access components.

```csharp
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public class ManagerAccessViolationAnalyzer : DiagnosticAnalyzer
{
    private static readonly DiagnosticDescriptor Rule = new(
        id: "VBD003",
        title: "Manager directly calls Access component",
        messageFormat: "Manager '{0}' calls Access component '{1}'. Route through Engine instead.",
        category: "Architecture",
        defaultSeverity: DiagnosticSeverity.Warning,
        isEnabledByDefault: true);

    public override void Initialize(AnalysisContext context)
    {
        context.RegisterOperationAction(AnalyzeInvocation, OperationKind.Invocation);
    }

    private void AnalyzeInvocation(OperationAnalysisContext context)
    {
        var invocation = (IInvocationOperation)context.Operation;
        var containingType = context.ContainingSymbol.ContainingType;

        if (!IsManagerType(containingType)) return;

        var targetType = invocation.TargetMethod.ContainingType;
        if (IsAccessType(targetType))
        {
            context.ReportDiagnostic(Diagnostic.Create(
                Rule,
                invocation.Syntax.GetLocation(),
                containingType.Name,
                targetType.Name));
        }
    }
}
```

### VBD004: UI Project References Service Implementation

**Rule:** UI projects depend only on Contracts.

```csharp
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public class UiDependencyAnalyzer : DiagnosticAnalyzer
{
    private static readonly DiagnosticDescriptor Rule = new(
        id: "VBD004",
        title: "UI project references service implementation",
        messageFormat: "UI project references '{0}'. Use contract interface from Contracts project.",
        category: "Architecture",
        defaultSeverity: DiagnosticSeverity.Error,
        isEnabledByDefault: true);

    public override void Initialize(AnalysisContext context)
    {
        context.RegisterCompilationAction(AnalyzeCompilation);
    }

    private void AnalyzeCompilation(CompilationAnalysisContext context)
    {
        if (!IsUiProject(context.Compilation.AssemblyName)) return;

        foreach (var reference in context.Compilation.References)
        {
            if (reference is not CompilationReference compRef) continue;

            var refName = compRef.Compilation.AssemblyName;
            if (IsServiceImplementationProject(refName))
            {
                context.ReportDiagnostic(Diagnostic.Create(
                    Rule,
                    Location.None,
                    refName));
            }
        }
    }
}
```

## Helper Methods

```csharp
public static class VbdAnalyzerHelpers
{
    public static bool IsContractProject(string assemblyName) =>
        assemblyName?.EndsWith(".Contracts") ?? false;

    public static bool IsServiceProject(string assemblyName) =>
        assemblyName?.EndsWith(".Service") ?? false;

    public static bool IsManagerProject(string assemblyName) =>
        assemblyName?.EndsWith(".Manager") ?? false;

    public static bool IsAccessProject(string assemblyName) =>
        assemblyName?.EndsWith(".Access") ?? false;

    public static bool IsUiProject(string assemblyName) =>
        assemblyName?.Contains(".UI.") ?? false;

    public static bool IsManagerType(INamedTypeSymbol type) =>
        type.Name.EndsWith("Manager") ||
        type.GetAttributes().Any(a => a.AttributeClass?.Name == "ManagerAttribute");

    public static bool IsAccessType(INamedTypeSymbol type) =>
        type.Name.EndsWith("Access") ||
        type.GetAttributes().Any(a => a.AttributeClass?.Name == "AccessAttribute");

    public static bool IsEngineType(INamedTypeSymbol type) =>
        type.Name.EndsWith("Engine") ||
        type.GetAttributes().Any(a => a.AttributeClass?.Name == "EngineAttribute");

    public static bool IsInSameBoundary(ISymbol symbol, string projectName)
    {
        var symbolBoundary = ExtractBoundaryName(symbol.ContainingNamespace?.ToDisplayString());
        var projectBoundary = ExtractBoundaryName(projectName);
        return symbolBoundary == projectBoundary;
    }

    public static string? ExtractBoundaryName(string? fullName)
    {
        if (string.IsNullOrEmpty(fullName)) return null;
        var parts = fullName.Split('.');
        return parts.Length > 0 ? parts[0] : null;
    }
}
```

## Code Fixes

Provide automatic fixes for violations:

```csharp
[ExportCodeFixProvider(LanguageNames.CSharp)]
public class UseBoundaryContractFix : CodeFixProvider
{
    public override async Task RegisterCodeFixesAsync(CodeFixContext context)
    {
        var diagnostic = context.Diagnostics.First();
        var root = await context.Document.GetSyntaxRootAsync(context.CancellationToken);
        var node = root.FindNode(diagnostic.Location.SourceSpan);

        context.RegisterCodeFix(
            CodeAction.Create(
                title: "Use contract interface",
                createChangedDocument: c => ReplaceWithContractAsync(context.Document, node, c),
                equivalenceKey: "UseContract"),
            diagnostic);
    }

    private async Task<Document> ReplaceWithContractAsync(
        Document document,
        SyntaxNode node,
        CancellationToken ct)
    {
        var semanticModel = await document.GetSemanticModelAsync(ct);
        var typeSymbol = semanticModel.GetSymbolInfo(node, ct).Symbol as INamedTypeSymbol;

        // Find corresponding contract interface
        var contractInterface = FindContractInterface(typeSymbol);
        if (contractInterface is null) return document;

        // Replace implementation type with interface
        var newNode = node.ReplaceNode(
            node,
            SyntaxFactory.IdentifierName(contractInterface.Name));

        var root = await document.GetSyntaxRootAsync(ct);
        var newRoot = root.ReplaceNode(node, newNode);
        return document.WithSyntaxRoot(newRoot);
    }
}
```

## Testing Analyzers

```csharp
[Fact]
public async Task DetectsCrossBoundaryViolation()
{
    var test = """
        using Billing.Service;

        public class OrderManager
        {
            private readonly BillingEngine _engine; // Violation
        }
        """;

    var expected = new DiagnosticResult
    {
        Id = "VBD001",
        Severity = DiagnosticSeverity.Error,
        Locations = new[] { new DiagnosticResultLocation("Test0.cs", 5, 9) }
    };

    await VerifyCSharpDiagnosticAsync(test, expected);
}

[Fact]
public async Task CodeFixReplacesWithContract()
{
    var test = """
        using Billing.Service;

        public class OrderManager
        {
            private readonly BillingEngine _engine;
        }
        """;

    var fix = """
        using Billing.Contracts;

        public class OrderManager
        {
            private readonly IBillingService _engine;
        }
        """;

    await VerifyCSharpFixAsync(test, fix);
}
```

## Integration with Build

Analyzers run automatically during build:

```xml
<ItemGroup>
  <PackageReference Include="YourCompany.Analyzers.VBD" Version="1.0.0"
                    PrivateAssets="all" />
</ItemGroup>
```

Configure severity:

```xml
<PropertyGroup>
  <WarningsAsErrors>VBD001;VBD002;VBD004</WarningsAsErrors>
</PropertyGroup>
```

Or in `.editorconfig`:

```ini
[*.cs]
dotnet_diagnostic.VBD001.severity = error
dotnet_diagnostic.VBD002.severity = error
dotnet_diagnostic.VBD003.severity = warning
dotnet_diagnostic.VBD004.severity = error
```
