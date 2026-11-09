---
metadata-version: "1.0.0"
title: "Component initialization template"
description: "Specify the requested interface and primary-constructor shape."
document-type: "template"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Component initialization template

Use Capability and VaultType as substitution tokens. VaultType is the approved Manager, Engine, or Access classification. Replace tokens consistently; do not include angle brackets or hyphens in the resulting identifier. Keep the interface and implementation in separate files.

Interface shape:

```csharp
public interface ICapabilityVaultType
{
}
```

Implementation shape for the currently inspected Ifx base API:

```csharp
using Ifx.Component;
using Microsoft.Extensions.Logging;

public class CapabilityVaultType(ILoggerFactory loggerFactory)
    : ComponentBase<CapabilityVaultType>(
        (loggerFactory ?? throw new ArgumentNullException(nameof(loggerFactory)))
            .CreateLogger<CapabilityVaultType>()),
      ICapabilityVaultType
{
}
```

Import System when implicit usings are disabled. Supply namespaces from the accepted design. The primary-constructor syntax requires C# 12 or later; follow the consuming project's approved baseline rather than changing its SDK or build settings.

The user requested an ILoggerFactory constructor. The inspected Ifx.Component.ComponentBase<T> constructor takes ILogger<T>, so CreateLogger<T>() bridges the two APIs without changing Ifx. Recheck that API when consuming a different revision. The generic argument is the concrete component type.

The empty interface is an initialization skeleton. Add only reviewed contract operations and service metadata required by the consuming design. These samples do not choose transport or hosting.

See the [concrete samples](../../samples/components/README.md). Caller-facing resolution must preserve Governance's [component proxy policy](../../../vc.Governance/docs/patterns/component-proxies.md). An empty skeleton provides no proxy chain or production registration.
