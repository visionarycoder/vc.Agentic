---
metadata-version: "1.0.0"
title: ".NET AOT Compatibility"
description: "Preserve scoped source guidance for dotnet-aot-compat."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# .NET AOT Compatibility

Agent uses this skill to make .NET 8+ code safe for trimming and Native AOT.

## When to Use

| User prompt | Use |

|---|---|

| User enables `IsAotCompatible` or `PublishAot` | Agent uses this skill |

| User asks to fix `IL2026`, `IL2067`, `IL2070`, `IL2072`, or `IL3050` | Agent uses this skill |

| User asks to replace reflection-heavy serializer code | Agent uses this skill |

## When Not to Use

| User prompt | Route |

|---|---|

| User targets .NET Framework only | Agent uses a non-AOT workflow |

| User asks for publish-size tuning after warnings reach zero | Agent uses a performance workflow |

| User asks for broad library replacement with no IL warnings | Agent uses a separate refactor workflow |

## Required Inputs

| Input | Required | Notes |

|---|---|---|

| Target project | Yes | Project targets `net8.0` or later for active AOT analysis. |

| Build warning output | Yes | Agent uses warning output to choose edits. |

| Reflection or serialization hotspot | No | Agent uses this input to batch related fixes. |

| Multi-targeting scope | No | Agent uses this input to scope `IsAotCompatible`. |

## Workflow

| Step | Agent action | Test | Pass |

|---|---|---|---|

| 1 | Agent enables trim or AOT analysis in the target project. | Run `rg -n "IsAotCompatible|PublishAot|PublishTrimmed" <project>.csproj`. | The project file contains the intended property for the intended TFM scope. |

| 2 | Agent runs one clean build and groups IL warnings by code. | Run `dotnet build <project-or-solution>`. | Build output lists warning codes or reports zero IL warnings. |

| 3 | Agent fixes the dominant warning pattern first and reads `references/polyfills.md` when older TFMs need trim-analysis attribute polyfills. | Read the edited call sites. | Edits use annotations, refactors, or source generation instead of suppression. |

| 4 | Agent rebuilds after each small batch. | Run `dotnet build <project-or-solution>`. | Warning count decreases or reaches zero. |

| 5 | Agent repeats until target TFMs are warning-clean. | Run `dotnet build <project-or-solution> -f <tfm>`. | Target `net8.0+` TFMs report zero IL trim and AOT warnings. |

## Reference Files

| File | Covers | Agent Reads |
|---|---|---|
| `references/polyfills.md` | Local polyfills for trim-analysis attributes on older target frameworks. | Agent reads it during warning fixes when multi-targeted older TFMs need recognized trim attributes. |

## Fix Matrix

| Warning pattern | Agent action |

|---|---|

| Reflection on `Type` values | Agent adds `[DynamicallyAccessedMembers]` at the narrowest useful call site and propagates the contract outward. |

| Annotation flow lost through `object` or untyped collections | Agent replaces the untyped path with strongly typed values. |

| `JsonSerializer` drives warning clusters | Agent adds a source-generated `JsonSerializerContext` and updates call sites. |

| Dynamic behavior has no static contract | Agent adds `[RequiresUnreferencedCode]` or `[RequiresDynamicCode]` only after narrower fixes fail. |

| External SDK offers an AOT-safe serializer path | Agent uses the SDK path instead of reflection-based defaults. |

## Validation Checklist

- [ ] Agent scoped trim or AOT properties to supported TFMs.

- [ ] Agent used build warnings to choose files.

- [ ] Agent fixed warnings with annotations, refactors, or source generation.

- [ ] Agent avoided pragma and suppression-based fixes.

- [ ] Agent ran build verification for each target `net8.0+` TFM.

- [ ] Agent left older TFMs buildable when the project multi-targets.

## Common Pitfalls

| Pitfall | Agent fix |

|---|---|

| Agent reads the whole repo before the first build | Agent starts with build warnings. |

| Agent boxes `Type` values and breaks annotation flow | Agent keeps annotated values strongly typed. |

| Agent suppresses warnings that still fail at publish time | Agent fixes the underlying reflection or serialization contract. |

| Agent adds broad `Requires*` attributes first | Agent uses narrower annotations or source generation first. |
