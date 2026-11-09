# Testing Strategies for Roslyn Generators

Comprehensive testing ensures generators produce correct, consistent code across scenarios.

## Test Pyramid for Generators

1. **Unit tests** — Verify individual transformation logic (70%)
2. **Integration tests** — Verify full compilation and semantic correctness (25%)
3. **Snapshot tests** — Verify generated output matches expectations (5%)

## Unit Testing Transformations

Test the core logic that transforms syntax/symbols into output:

```csharp
[Fact]
public void ExtractsBoundaryNameFromAttribute()
{
    var attribute = ParseAttribute("[ServiceBoundary(\"Billing\")]");
    var name = BoundaryExtractor.GetName(attribute);
    Assert.Equal("Billing", name);
}

[Fact]
public void IdentifiesContractInterfaces()
{
    var classDecl = ParseClass("""
        [ServiceBoundary("Test")]
        public class TestDef
        {
            [Contract] public interface ITestService { }
        }
        """);

    var contracts = BoundaryExtractor.GetContracts(classDecl);
    Assert.Single(contracts);
    Assert.Equal("ITestService", contracts[0].Name);
}
```

## Integration Testing with Compilation

Verify that generated code compiles and produces correct semantics:

```csharp
[Fact]
public void GeneratedCodeCompiles()
{
    var source = """
        [ServiceBoundary("Billing")]
        public class BillingDef { }
        """;

    var compilation = CreateCompilation(source);
    var driver = CreateDriver(compilation, new ServiceBoundaryGenerator());
    var result = driver.RunGenerators(compilation);

    Assert.Empty(result.Diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error));
}

[Fact]
public void GeneratedClassIsAccessible()
{
    var source = "[ServiceBoundary(\"Test\")] public class TestDef { }";
    var compilation = RunGeneratorAndCompile(source);

    var generatedType = compilation.GetTypeByMetadataName("Test.Contracts.ITestService");
    Assert.NotNull(generatedType);
    Assert.True(generatedType.DeclaredAccessibility == Accessibility.Public);
}
```

## Snapshot Testing with Verify

Capture and review generated output:

```csharp
[Fact]
public Task GeneratesExpectedBoundaryStructure()
{
    var source = """
        [ServiceBoundary("Billing")]
        public class BillingDef
        {
            [Contract] public interface IBillingService { }
        }
        """;

    var output = RunGenerator(source);
    return Verify(output)
        .UseDirectory("Snapshots")
        .ScrubLinesContaining("GeneratedCode"); // Remove version stamps
}
```

Store snapshots in `*.verified.cs` files. Review diffs when tests fail.

## Testing Incremental Generation

Verify that generators only regenerate what changed:

```csharp
[Fact]
public void OnlyRegeneratesChangedBoundary()
{
    var source1 = "[ServiceBoundary(\"A\")] public class A { }";
    var source2 = "[ServiceBoundary(\"B\")] public class B { }";

    var compilation1 = CreateCompilation(source1, source2);
    var driver1 = CreateDriver(compilation1);
    var result1 = driver1.RunGenerators(compilation1);

    // Modify only source1
    var compilation2 = compilation1.ReplaceSyntaxTree(
        compilation1.SyntaxTrees.First(),
        ParseTree("[ServiceBoundary(\"A\")] public class AModified { }"));

    var driver2 = driver1.RunGenerators(compilation2);
    var result2 = driver2.GetRunResult();

    // Verify only A-related files were regenerated
    var changedFiles = result2.GeneratedTrees
        .Where(t => !result1.GeneratedTrees.Contains(t));

    Assert.All(changedFiles, f => Assert.Contains("A.", f.FilePath));
    Assert.DoesNotContain(changedFiles, f => f.FilePath.Contains("B."));
}
```

## Testing Cross-Project Dependencies

Verify that generated projects reference each other correctly:

```csharp
[Fact]
public void ServiceProjectReferencesContractProject()
{
    var source = "[ServiceBoundary(\"Test\")] public class TestDef { }";
    var output = RunGenerator(source);

    var serviceProject = output.Projects.Single(p => p.Name.EndsWith(".Service"));
    var contractProject = output.Projects.Single(p => p.Name.EndsWith(".Contracts"));

    Assert.Contains(serviceProject.ProjectReferences,
        pr => pr.ProjectId == contractProject.Id);
}

[Fact]
public void UIProjectOnlyReferencesContracts()
{
    var source = """
        [ServiceBoundary("Test")]
        [Projection(ProjectionType.Vue)]
        public class TestDef { }
        """;

    var output = RunGenerator(source);
    var uiProject = output.Projects.Single(p => p.Name.EndsWith(".UI.Vue"));
    var references = uiProject.ProjectReferences.Select(pr => pr.Name);

    Assert.Contains("Test.Contracts", references);
    Assert.DoesNotContain("Test.Service", references);
    Assert.DoesNotContain("Test.Manager", references);
}
```

## Testing Analyzer Integration

Verify that generated analyzers detect violations:

```csharp
[Fact]
public void AnalyzerDetectsCrossBoundaryViolation()
{
    var source = """
        // In UI project
        using Billing.Service; // Should be Billing.Contracts

        public class BillingView
        {
            private readonly BillingEngine _engine; // Violation!
        }
        """;

    var diagnostics = RunAnalyzer<BoundaryIsolationAnalyzer>(source);

    var violation = Assert.Single(diagnostics);
    Assert.Equal("VBD001", violation.Id);
    Assert.Contains("cross-boundary reference", violation.GetMessage());
}
```

## Performance Testing

Ensure generators remain fast:

```csharp
[Fact]
public void GeneratesLargeBoundaryInUnder100ms()
{
    var source = GenerateLargeBoundaryDefinition(100); // 100 contracts

    var sw = Stopwatch.StartNew();
    var output = RunGenerator(source);
    sw.Stop();

    Assert.True(sw.ElapsedMilliseconds < 100,
        $"Generation took {sw.ElapsedMilliseconds}ms");
}

[Fact]
public void IncrementalGenerationIsSubLinear()
{
    var sources = Enumerable.Range(0, 10)
        .Select(i => $"[ServiceBoundary(\"Boundary{i}\")] public class B{i} {{ }}");

    var compilation = CreateCompilation(sources.ToArray());
    var driver = CreateDriver(compilation);

    // Time full generation
    var sw1 = Stopwatch.StartNew();
    driver.RunGenerators(compilation);
    sw1.Stop();

    // Modify one boundary
    var newCompilation = compilation.ReplaceSyntaxTree(
        compilation.SyntaxTrees.First(),
        ParseTree("[ServiceBoundary(\"Boundary0\")] public class B0Modified { }"));

    // Time incremental generation
    var sw2 = Stopwatch.StartNew();
    driver.RunGenerators(newCompilation);
    sw2.Stop();

    // Incremental should be much faster
    Assert.True(sw2.ElapsedMilliseconds < sw1.ElapsedMilliseconds / 5);
}
```

## Testing Error Handling

Verify generators handle invalid input gracefully:

```csharp
[Fact]
public void ReportsErrorForInvalidBoundaryName()
{
    var source = "[ServiceBoundary(\"Invalid Name!\")] public class Test { }";
    var diagnostics = RunGenerator(source).Diagnostics;

    var error = Assert.Single(diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error));
    Assert.Equal("VBD100", error.Id);
    Assert.Contains("invalid boundary name", error.GetMessage());
}

[Fact]
public void ReportsErrorForDuplicateBoundaryNames()
{
    var source = """
        [ServiceBoundary("Test")] public class A { }
        [ServiceBoundary("Test")] public class B { }
        """;

    var diagnostics = RunGenerator(source).Diagnostics;
    Assert.Contains(diagnostics, d =>
        d.Id == "VBD101" &&
        d.GetMessage().Contains("duplicate boundary"));
}
```

## Test Helpers

Common utilities for generator testing:

```csharp
public static class GeneratorTestHelpers
{
    public static Compilation CreateCompilation(params string[] sources)
    {
        var syntaxTrees = sources.Select(s => CSharpSyntaxTree.ParseText(s));
        return CSharpCompilation.Create(
            "TestAssembly",
            syntaxTrees,
            new[] { MetadataReference.CreateFromFile(typeof(object).Assembly.Location) },
            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));
    }

    public static GeneratorDriverRunResult RunGenerator<TGenerator>(
        string source) where TGenerator : IIncrementalGenerator, new()
    {
        var compilation = CreateCompilation(source);
        var generator = new TGenerator();
        var driver = CSharpGeneratorDriver.Create(generator);
        return driver.RunGenerators(compilation).GetRunResult();
    }

    public static ImmutableArray<Diagnostic> GetDiagnostics(
        this GeneratorDriverRunResult result)
    {
        return result.Diagnostics
            .Concat(result.Results.SelectMany(r => r.Diagnostics))
            .ToImmutableArray();
    }
}
```

## CI Integration

Run generator tests in CI:

```yaml
- name: Test Generators
  run: dotnet test Generators.Tests/

- name: Verify Snapshots
  run: |
    dotnet test Generators.Tests/ --filter Category=Snapshot
    if [ -n "$(git status --porcelain)" ]; then
      echo "Snapshot verification failed"
      git diff
      exit 1
    fi
```

## Debugging Failed Tests

When tests fail:

1. **Check diagnostics** — Look for errors in `result.Diagnostics`
2. **Inspect generated code** — Use `result.GeneratedTrees[0].ToString()`
3. **Compare snapshots** — Review `.verified.cs` diffs
4. **Attach debugger** — Set breakpoints in generator code
5. **Emit intermediate files** — Enable `EmitCompilerGeneratedFiles` in test project
