---
name: "vbd-dto-authoring"
description: "Define immutable VBD DTO records with scope ownership, fluent builders, and explicit mapper boundaries for Manager, Engine, and Access components."
metadata:
  metadata-version: "1.0.0"
  title: "VBD DTO Authoring"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "vbd"
---

# VBD DTO Authoring

Agent keeps VBD DTOs immutable, scope-owned, and business-aligned. Agent uses records for contracts and fluent builders for safe construction when inputs are staged.

## When to Use

| Condition | Use |
|---|---|
| Agent writes Manager, Engine, or Access contract DTOs | Use this skill |
| Agent needs immutable VBD records with staged creation | Use this skill |
| Agent fixes cross-boundary DTO leakage | Use this skill |
| Agent standardizes builder patterns for scope-owned DTOs | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Type is a persistence entity or ORM model | `vbd-access-components` |
| Type owns behavior or identity-rich invariants | `dotnet-value-object-standards` |
| Type is generic .NET DTO guidance outside VBD boundaries | `dotnet-dto-standards` |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Owning scope | Yes | Manager, Engine, Access, or integration boundary |
| DTO role | Yes | Request, response, command, event, query result, or adapter payload |
| Business term | Yes | Ontology-aligned noun or verb phrase |
| Builder need | Yes | `required`, `staged`, or `not-needed` |
| Mapping seam | No | Upstream source, downstream target, or both |

## Workflow

1. Agent assigns the DTO to one receiving boundary only.
2. Agent names the record from business ontology, not persistence or UI trivia.
3. Agent defines immutable record members with explicit nullability and scope-safe collections.
4. Agent adds a fluent builder when creation is staged, conditional, or discriminator-driven.
5. Agent keeps mapping and persistence logic outside the DTO and outside the builder.

Test: Run `dotnet build [project].csproj`.
Pass: Zero compile errors. Zero mutable DTO state. Zero business behavior inside DTOs.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| One DTO reused by several layers | Split by boundary and map |
| Builder becomes service locator | Keep builder data-only |
| DTO names follow tables or transport trivia | Rename from business ontology |
| Builder hides validation plus persistence | Move validation to owning boundary and persistence to Access |

## Rule Matrix

| Rule | Agent verifies | Detection pattern | Fix |
|---|---|---|---|
| VDTO-001 | VBD DTOs are immutable records | Mutable fields, public setters, mutable collections | Use record with required or init-only members |
| VDTO-002 | Each DTO has one owning boundary | Same DTO reused across Manager, Engine, or Access | Create scope-owned record and map |
| VDTO-003 | Names follow business ontology | Persistence, transport, or bag-style names | Rename to business-aligned request, result, command, or event |
| VDTO-004 | Builder is fluent and side-effect free | Builder writes storage, resolves services, or mutates shared state | Keep builder local, deterministic, and data-only |
| VDTO-005 | Builder exists only when it earns its complexity | Builder wraps one constructor with no staged value | Remove builder and use direct record construction |
| VDTO-006 | Mapping stays outside DTO and builder | DTO or builder constructs entities or invokes mappers | Move conversion to mapper layer |
| VDTO-007 | Collections and nullability stay explicit | Hidden null assumptions or mutable `List<T>` | Use explicit nullability and `IReadOnlyList<T>` or arrays |

## Pattern Matrix

| Scenario | Use | Avoid |
|---|---|---|
| Stable request contract | Immutable record with required members | Mutable request bag |
| Staged assembly from several inputs | Fluent builder returning immutable record | Partially initialized mutable DTO |
| Cross-boundary adaptation | Local record plus mapper | Shared DTO reused across scopes |
| Discriminator-driven shape | Builder composes valid record from staged inputs | Switch logic embedded in DTO |

## Example Pattern

```csharp
public sealed record InterfaceWorkflowRequest(
    required int InterfaceNumber,
    required string SourceSystem,
    required string TargetSystem,
    required IReadOnlyList<string> Steps);

public sealed class InterfaceWorkflowRequestBuilder
{
    private int? interfaceNumber;
    private string? sourceSystem;
    private string? targetSystem;
    private readonly List<string> steps = [];

    public InterfaceWorkflowRequestBuilder WithInterfaceNumber(int value)
    {
        interfaceNumber = value;
        return this;
    }

    public InterfaceWorkflowRequestBuilder FromSource(string value)
    {
        sourceSystem = value;
        return this;
    }

    public InterfaceWorkflowRequestBuilder ToTarget(string value)
    {
        targetSystem = value;
        return this;
    }

    public InterfaceWorkflowRequestBuilder AddStep(string value)
    {
        steps.Add(value);
        return this;
    }

    public InterfaceWorkflowRequest Build()
    {
        return new InterfaceWorkflowRequest(
            InterfaceNumber: interfaceNumber ?? throw new InvalidOperationException("InterfaceNumber is required."),
            SourceSystem: sourceSystem ?? throw new InvalidOperationException("SourceSystem is required."),
            TargetSystem: targetSystem ?? throw new InvalidOperationException("TargetSystem is required."),
            Steps: [.. steps]);
    }
}
```

## Verification Checklist

Agent verifies:
- [ ] DTO is an immutable record
- [ ] DTO belongs to one VBD boundary only
- [ ] Builder is present only when staged creation is real
- [ ] Builder returns immutable DTO and performs zero side effects
- [ ] Mapping logic stays outside DTOs and builders

## References

- Detailed examples and patterns: `references/patterns.md`
