---
name: "maui-safe-area"
description: ".NET 10 introduces a **brand-new, cross-platform safe area API** that replaces the legacy iOS-only `UseSafeArea` and the layout-level `IgnoreSafeArea` properties. The new `SafeAreaEdges` property and `SafeAreaRegions` flags enum give you per-edge, per-control safe area management on Android, iOS, and Mac Catalyst from a single API surface."
metadata:
  metadata-version: "1.0.0"
  title: "Safe Area & Edge-to-Edge Layout (.NET 10+)"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# Safe Area & Edge-to-Edge Layout (.NET 10+)

.NET 10 introduces a **brand-new, cross-platform safe area API** that replaces the legacy iOS-only `UseSafeArea` and the layout-level `IgnoreSafeArea` properties. The new `SafeAreaEdges` property and `SafeAreaRegions` flags enum give you per-edge, per-control safe area management on Android, iOS, and Mac Catalyst from a single API surface.

> **This is new API surface in .NET 10.** If the project targets .NET 9 or earlier, these APIs do not exist. Guide the developer to the legacy `ios:Page.UseSafeArea` and `Layout.IgnoreSafeArea` properties instead.

## When to Use

- Content overlaps status bar, notch, Dynamic Island, or home indicator after upgrading to .NET 10
- Implementing edge-to-edge / immersive layouts (photo viewers, video players, maps)
- Keyboard avoidance for chat or form UIs
- Migrating from `ios:Page.UseSafeArea`, `Layout.IgnoreSafeArea`, or `WindowSoftInputModeAdjust.Resize`
- Blazor Hybrid apps that need CSS `env(safe-area-inset-*)` coordination
- Mixed layouts with an edge-to-edge header but a safe-area-respecting body

## When Not to Use

- Projects targeting .NET 9 or earlier — use the legacy iOS-specific APIs
- General page layout questions unrelated to system bars or keyboard — use standard layout guidance
- App lifecycle or navigation structure — use maui-app-lifecycle or Shell guidance
- Theming or visual styling — use the **maui-theming** skill

## Inputs

- Target framework: must be `net10.0-*` or later for the new APIs
- Target platforms: Android, iOS, Mac Catalyst (Windows does not have system bar insets)
- UI approach: XAML/C#, Blazor Hybrid, or MauiReactor

## SafeAreaRegions and SafeAreaEdges

`SafeAreaRegions` values: `None`, `SoftInput`, `Container`, `Default`, `All`. Only `SoftInput` and `Container` combine as flags. `SafeAreaEdges` accepts uniform, horizontal/vertical, or Left/Top/Right/Bottom comma-separated values, for example `SafeAreaEdges="Container, Container, Container, SoftInput"` for a keyboard-aware chat bottom.

## Control Defaults

| Control | Default | Notes |
|---------|---------|-------|
| `ContentPage` | `None` | Edge-to-edge. **Breaking change from .NET 9 on Android.** |
| `Layout` (Grid, StackLayout, etc.) | `Container` | Respects bars/notch, flows under keyboard |
| `ScrollView` | `Default` | iOS maps to automatic content insets. Only `Container` and `None` take effect. |
| `ContentView` | `None` | Inherits parent behavior |
| `Border` | `None` | Inherits parent behavior |

After upgrading from .NET 9, Android `ContentPage` content goes under the status bar; set `SafeAreaEdges="Container"` to restore the old behavior.

## Usage Patterns

### Mixed: edge-to-edge header + safe body + keyboard footer

```xaml
<ContentPage SafeAreaEdges="None">
    <Grid RowDefinitions="Auto,*,Auto">
        <Grid BackgroundColor="{StaticResource Primary}">
            <Label Text="App Header" TextColor="White" Margin="20,40,20,20" />
        </Grid>
        <ScrollView Grid.Row="1" SafeAreaEdges="Container">
            <!-- Use Container, not All — ScrollView only honors Container and None -->
            <VerticalStackLayout Padding="20">
                <Label Text="Main content" />
            </VerticalStackLayout>
        </ScrollView>
        <Grid Grid.Row="2" SafeAreaEdges="SoftInput"
              BackgroundColor="LightGray" Padding="20">
            <Entry Placeholder="Type a message..." />
        </Grid>
    </Grid>
</ContentPage>
```

### Programmatic (C#)

```csharp
var page = new ContentPage
{
    SafeAreaEdges = SafeAreaEdges.All
};

var grid = new Grid
{
    SafeAreaEdges = new SafeAreaEdges(
        left: SafeAreaRegions.Container,
        top: SafeAreaRegions.Container,
        right: SafeAreaRegions.Container,
        bottom: SafeAreaRegions.SoftInput)
};
```

## Decision Framework

| Scenario | SafeAreaEdges value |
|----------|---------------------|
| Forms, critical inputs | `All` |
| Photo viewer, video player, game | `None` (on page **and** layout) |
| Scrollable content with fixed header/footer | `Container` |
| Chat/messaging with bottom input bar | Per-edge: `Container, Container, Container, SoftInput` |
| Blazor Hybrid app | `None` on page; CSS `env()` for insets |

## Blazor Hybrid Integration

Set page `SafeAreaEdges="None"`, add `viewport-fit=cover` to the `index.html` viewport meta tag (otherwise iOS `env(safe-area-inset-*)` is zero), and pad with CSS `env()`. Do not also set XAML `Container`; insets double.

## Migration from Legacy APIs

| Legacy (.NET 9 and earlier) | New (.NET 10+) |
|-----------------------------|----------------|
| `ios:Page.UseSafeArea="True"` | `SafeAreaEdges="Container"` |
| `Layout.IgnoreSafeArea="True"` | `SafeAreaEdges="None"` |
| `WindowSoftInputModeAdjust.Resize` | `SafeAreaEdges="All"` on ContentPage |

The legacy properties still compile but are obsolete. `IgnoreSafeArea="True"` maps internally to `SafeAreaRegions.None`.

## Common Pitfalls

1. **Layout not set to `None`.** Child layouts default to `Container`; set `None` on both page and layout for immersive content.
2. **`SoftInput` on ScrollView.** ScrollView honors only `Container` and `None`. Wrap it in a Grid or StackLayout and apply `SoftInput` there.
3. **`Default` is not `None`.** `Default` is the platform default for the control type; on iOS ScrollView it enables automatic content insets.
4. **New code using legacy `ios:Page.UseSafeArea`.** Use `SafeAreaEdges`.