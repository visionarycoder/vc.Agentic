---
name: "dotnet-source-generated-regex"
description: "Convert runtime or compiled regex usage to build-time GeneratedRegex patterns for .NET 7+."
metadata:
  metadata-version: "1.0.0"
  title: "Source-Generated Compiled Regular Expressions"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Source-Generated Compiled Regular Expressions

Convert runtime regex patterns to compile-time generated patterns for lower startup cost, trim safety, and AOT safety in .NET 7+.

## When to Use

| Condition | Use |
|---|---|
| Project targets .NET 7 or later | Use this skill |
| Code uses `RegexOptions.Compiled`, `new Regex(...)`, `Regex.Match(...)`, or `Regex.IsMatch(...)` repeatedly | Use this skill |
| Work needs trim-safe or NativeAOT-safe regex behavior | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Project targets earlier than .NET 7 | Use `.github/skills/dotnet-compiled-regex-patterns/` |
| Request is about authoring custom source generators | Use `.github/skills/roslyn-source-generator-authoring/` |
| Pattern is one-off and performance is irrelevant | Keep existing code unless standards require change |

## Decision Table

| Approach | Compilation | Runtime Cost | Trim-Safe | AOT-Safe |
|---|---|---|---|---|
| `Regex.Match(...)` or `new Regex(...)` per call | Runtime | High | No | No |
| `RegexOptions.Compiled` field | Runtime initialization | Medium | No | No |
| `[GeneratedRegex]` | Build time | Low | Yes | Yes |

## Workflow

| Step | Agent Action | Output |
|---|---|---|
| 1. Inventory | Agent finds ad-hoc regex calls and compiled regex fields. | Candidate list |
| 2. Classify | Agent confirms target framework supports `[GeneratedRegex]`. | Go or no-go decision |
| 3. Extract | Agent creates or updates a `static partial` regex holder class. | Generated regex methods |
| 4. Replace | Agent swaps field or inline usage for generated method calls. | Updated call sites |
| 5. Remove | Agent deletes obsolete pattern constants and compiled fields when no longer needed. | Reduced legacy regex code |
| 6. Verify | Agent builds and runs tests that exercise the changed regex call sites. | Validation result |

## Implementation Pattern

```csharp
using System.Text.RegularExpressions;

namespace Example.Accounting.Ifx.Mainframe;

public static partial class CopybookPatterns
{
    [GeneratedRegex(@"S?9\((\d+)\)V(\d*)", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
    public static partial Regex DecimalPictureRegex();
}
```

## Migration Rules

1. Agent creates a `public static partial` or `internal static partial` holder that matches local naming patterns.
2. Agent adds one partial method per reusable pattern.
3. Agent keeps method bodies absent.
4. Agent preserves required `RegexOptions`.
5. Agent adds `RegexOptions.CultureInvariant` for internal deterministic patterns unless behavior depends on culture.
6. Agent replaces call sites with `Holder.Method().Match(...)`, `IsMatch(...)`, or equivalent calls.
7. Agent removes replaced `RegexOptions.Compiled` fields and unused pattern constants.

## Before and After

```csharp
// Before
private static readonly Regex DecimalPictureRegex = new(
    @"S?9\((\d+)\)V(\d*)",
    RegexOptions.Compiled | RegexOptions.IgnoreCase);

var match = DecimalPictureRegex.Match(picture);

// After
[GeneratedRegex(@"S?9\((\d+)\)V(\d*)", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant)]
private static partial Regex DecimalPictureRegex();

var match = DecimalPictureRegex().Match(picture);
```

## Decision Rules

Agent uses source-generated regex when the project supports .NET 7+.

Agent prefers a dedicated patterns class when several related expressions exist.

Agent keeps generated methods near the owning domain when locality aids maintenance.

Agent avoids source-generated regex in projects that cannot use partial methods or the attribute.

## Validation

| Check | Test | Pass Criteria |
|---|---|---|
| Target support | Inspect project target framework. | Project targets .NET 7 or later. |
| Signature correctness | Review generated holder and methods. | Class and methods are `partial`; methods have no body. |
| Options preservation | Compare old and new options. | Required matching behavior remains intact. |
| Legacy cleanup | Search for replaced fields and constants. | No obsolete regex fields remain. |
| Build | Run project or solution build. | Build succeeds. |
| Behavior | Run targeted unit or integration tests. | Tests pass without regex behavior regressions. |

## Quality Gate

- [ ] Holder class uses `partial`.
- [ ] Each generated regex method uses `[GeneratedRegex]`.
- [ ] Internal deterministic patterns include `RegexOptions.CultureInvariant` unless matching depends on culture-sensitive rules.
- [ ] Call sites use generated method invocations.
- [ ] Removed fields and constants are no longer referenced.
- [ ] Build passed.
- [ ] Tests that exercise changed regex behavior passed.

## Reference Material

Agent stores extended examples and migration walkthroughs in `.github/skills/dotnet-source-generated-regex/references/migration-examples.md`.

## Related Skills

- `.github/skills/dotnet-compiled-regex-patterns/`
- `.github/skills/roslyn-source-generator-authoring/`

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [dotnet-source-generated-regex-alternative-1](references/contexts/dotnet-source-generated-regex-alternative-1/guide.md)
- [dotnet-source-generated-regex-alternative-2](references/contexts/dotnet-source-generated-regex-alternative-2/guide.md)
