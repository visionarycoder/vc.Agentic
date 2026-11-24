---
name: "maui-theming"
description: "Apply light/dark mode support, custom branded themes, and runtime theme switching in .NET MAUI apps using AppThemeBinding, ResourceDictionary swapping, and system theme detection APIs."
metadata:
  metadata-version: "1.0.0"
  title: ".NET MAUI Theming"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# .NET MAUI Theming

Apply light/dark mode support, custom branded themes, and runtime theme switching in .NET MAUI apps using AppThemeBinding, ResourceDictionary swapping, and system theme detection APIs.

## When to Use

- Adding light and dark mode support to a .NET MAUI app
- Creating custom branded themes with ResourceDictionary
- Detecting and responding to system theme changes at runtime
- Letting users choose a preferred theme (light, dark, or system default)
- Combining OS-driven theme response with custom color palettes

## When Not to Use

- Localization or language switching — see [.NET MAUI localization docs](https://learn.microsoft.com/dotnet/maui/fundamentals/localization)
- Accessibility-specific visual adjustments — see [.NET MAUI accessibility docs](https://learn.microsoft.com/dotnet/maui/fundamentals/accessibility)
- App icon or splash screen configuration — see [.NET MAUI app icon docs](https://learn.microsoft.com/dotnet/maui/user-interface/images/app-icons)
- Bootstrap-style class theming — see the `Plugin.Maui.BootstrapTheme` NuGet package

## Inputs

- A .NET MAUI project targeting .NET 8 or later
- XAML pages or C# UI code that need theme-aware styling

## Workflow

1. Detect the current theme approach in the project (AppThemeBinding, ResourceDictionary, or none).
2. Choose the appropriate strategy: AppThemeBinding for simple light/dark, ResourceDictionary swap for custom/multiple themes, or both combined.
3. Define theme resources — inline `AppThemeBinding` values or separate `ResourceDictionary` files with matching keys.
4. Replace hardcoded colors with `DynamicResource` bindings (or `AppThemeBinding` markup) throughout XAML pages.
5. Add system theme detection via `Application.Current.RequestedTheme` and the `RequestedThemeChanged` event.
6. Implement user preference persistence with `Preferences.Set` / `Preferences.Get` and apply on startup.
7. Verify Android `ConfigChanges.UiMode` is set on `MainActivity` to avoid activity restarts on theme change.
8. Test both light and dark themes on at least one target platform, confirming all UI elements respond correctly.

## Approach

Use `AppThemeBinding` for two themes, `ResourceDictionary` swapping with `DynamicResource` for custom or more themes, or both combined. Theme dictionaries that use `x:Class` need a code-behind that calls `InitializeComponent()`. When clearing `MergedDictionaries` to swap a theme, move non-theme dictionaries (for example converters) to `Application.Resources` directly.

## System Theme Detection

### Read the Current Theme

```csharp
AppTheme currentTheme = Application.Current!.RequestedTheme;
// Returns AppTheme.Light, AppTheme.Dark, or AppTheme.Unspecified
```

### Override the System Theme

```csharp
// Force dark mode regardless of OS setting
Application.Current!.UserAppTheme = AppTheme.Dark;

// Reset to follow system theme
Application.Current!.UserAppTheme = AppTheme.Unspecified;
```

### React to Theme Changes

```csharp
Application.Current!.RequestedThemeChanged += (s, e) =>
{
    AppTheme newTheme = e.RequestedTheme;
    // Update UI or switch ResourceDictionaries
};
```

## Pitfalls

- Android `MainActivity` needs `ConfigChanges.UiMode` in `ConfigurationChanges`, or toggling dark mode restarts the activity.
- CSS-based themes cannot be swapped at runtime; use `ResourceDictionary` theming.
- Every `x:Key` must exist in all theme dictionaries; a missing key silently falls back to the default value and produces inconsistent appearance.
- Replace hardcoded inline colors with theme-aware resources.
