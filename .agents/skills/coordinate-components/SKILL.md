---
name: "coordinate-components"
description: "Read `AGENTS.md` at the workspace root to learn the project's conventions before making changes."
metadata:
  metadata-version: "1.0.0"
  title: "Coordinate Components"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Coordinate Components

## Step 1 — Read AGENTS.md

Read `AGENTS.md` at the workspace root to learn the project's conventions before making changes.

## Step 2 — Decide the scope

| Need | Mechanism | When to use |
|------|-----------|-------------|
| Subtree (same render mode) | `CascadingValue` component | Theme, layout config within a layout |
| App-wide (all render modes) | `CascadingValueSource<T>` via DI | Current user, feature flags, theme shared globally |
| Mutable shared state within a circuit | Scoped service + `Action` event | Shopping cart, notification count, selected filters |

For parent→child one level: use `[Parameter]` / `EventCallback` (see `author-component` skill).
For persisting state across prerender→interactive: see `support-prerendering` skill.

## Workflow (quick reference)

1. Choose the mechanism from the table in Step 2
2. If crossing render mode boundaries → use `CascadingValueSource<T>`
3. Register in `Program.cs` with `AddCascadingValue(...)` and `isFixed: false`
4. Consume via `[CascadingParameter]` in child components
5. Update via `NotifyChangedAsync(newValue)` — never page reload
6. For additional mutable state within a circuit → add a scoped service
7. Wrap any `StateHasChanged` from background threads in `InvokeAsync`
8. Implement `IDisposable` — dispose timers, cancel tokens, unsubscribe events

## Shared state notes

- `CascadingValue` does not cross render mode boundaries. Use a DI `CascadingValueSource<T>` (`isFixed: false`, update with `NotifyChangedAsync`) or a scoped service.
- For Auto/WebAssembly, register the source or state service in both server and `.Client` `Program.cs`, with the type in a shared assembly.
- Keep cascaded types granular; each `NotifyChangedAsync` re-renders all subscribers.
- Use scoped, not singleton, for per-user state on Server.

## Scoped state service events

If the state-service event fires outside the Blazor sync context (timer, background task, SignalR hub), calling `StateHasChanged` directly throws `InvalidOperationException` (thread not associated with the Dispatcher). Wrap it in `InvokeAsync`:

```csharp
private Action? _handler;

protected override void OnInitialized()
{
    _handler = () => InvokeAsync(StateHasChanged);
    Cart.OnChange += _handler;
}

public void Dispose() => Cart.OnChange -= _handler;
```

Store the delegate in a field so you can unsubscribe the exact same instance. State created during prerender does not survive the switch to the interactive runtime; use `support-prerendering`.
