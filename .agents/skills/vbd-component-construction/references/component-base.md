---
title: Component Base
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Component Base

The real Service implementation, Simulator, and Emulator inherit the shared Ifx component base.

Expected type:

```csharp
public abstract class ComponentBase<T>(ILogger<T> componentLogger)
{
    protected internal readonly ILogger<T> logger =
        componentLogger ?? throw new ArgumentNullException(nameof(componentLogger));

    public Guid Instance { get; } = Guid.NewGuid();

    public DateTime CreatedAt { get; } = DateTime.UtcNow;
}
```

Preferred placement:

```text
Ifx.Components
```

The `logger` member is intentionally a field named exactly `logger`. Do not convert it to a property and do not prefix it with an underscore.

## Prerequisite handling

Inspect the repository for `ComponentBase<T>` before generation.

If it is missing, do not silently create or redesign shared Ifx infrastructure as a side effect of constructing one vault. Report the missing prerequisite and ask whether shared infrastructure should be created separately.

Do not silently fall back to a legacy `ServiceBase<T>` name when the repository is intended to use `ComponentBase<T>`.
