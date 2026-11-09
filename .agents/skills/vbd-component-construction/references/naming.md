---
title: Naming Rules
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Naming Rules

## Projects

```text
<VaultType>.<Capability>.Contract
<VaultType>.<Capability>.Service
<VaultType>.<Capability>.Host
<VaultType>.<Capability>.Simulator
<VaultType>.<Capability>.Emulator
Access.<Capability>.Orm.<SymbolicResource>
```

## Public interface

```text
I<Capability><VaultType>
```

Examples:

```text
IPortalManager
ITransformingEngine
IAdvantageAccess
```

## Real implementation

```text
<Capability><VaultType>
```

## Module

Always use the `Module` suffix:

```text
<Capability><VaultType>Module
<Capability><VaultType>SimulatorModule
<Capability><VaultType>EmulatorModule
```

## Engine gerund rule

Only Engine capabilities are normalized to gerunds.

Examples:

```text
Validation      -> Validating
Transformation  -> Transforming
Calculation     -> Calculating
Comparison      -> Comparing
Mapping         -> Mapping
Filtering       -> Filtering
```

Normalize obvious cases internally. Do not reject the developer's noun and make them learn the naming rule.

Ask only when multiple valid gerund forms would materially alter the capability meaning.

Manager and Access capabilities are not forced into gerund form.

## Resource contexts

Use the symbolic resource name and hide the current technology:

```text
<SymbolicResource>Context
```

Examples:

```text
FinancialContext
AdministrationContext
AccountingContext
```

Do not use `DbContext` in the context class name. The class may inherit `DbContext`, but its name represents the logical resource context.

## Constructor ordering

For Service, Simulator, and Emulator implementations:

1. `ILogger<T>` first
2. component/vault dependencies
3. framework/infrastructure dependencies

Use deterministic alphabetical ordering within a group when no semantic order is required.

## Identifier rule

Never generate underscore-prefixed identifiers.

Correct:

```csharp
protected internal readonly ILogger<T> logger;
```

Incorrect:

```csharp
private readonly ILogger<T> _logger;
```
