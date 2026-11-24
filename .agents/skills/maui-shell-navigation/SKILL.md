---
name: "maui-shell-navigation"
description: "Implement page navigation in .NET MAUI apps using Shell. Shell provides URI-based navigation, a flyout menu, tab bars, and a four-level visual hierarchy — all configured declaratively in XAML."
metadata:
  metadata-version: "1.0.0"
  title: ".NET MAUI Shell Navigation"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# .NET MAUI Shell Navigation

Implement page navigation in .NET MAUI apps using Shell. Shell provides URI-based navigation, a flyout menu, tab bars, and a four-level visual hierarchy — all configured declaratively in XAML.

## When to Use

- Setting up top-level app navigation with tabs or a flyout menu
- Navigating between pages programmatically with `GoToAsync`
- Passing data between pages via query parameters or object parameters
- Registering detail-page routes for push navigation
- Guarding navigation with confirmation dialogs (e.g., unsaved changes)
- Customizing back button behavior per page

## When Not to Use

- Deep linking from external URLs or app links — see [.NET MAUI deep linking docs](https://learn.microsoft.com/dotnet/maui/fundamentals/app-links)
- Data binding on navigation target pages — use `maui-data-binding`
- Dependency injection for pages and view models — use `maui-dependency-injection`
- Apps using `NavigationPage` without Shell (different navigation API)

## Inputs

- A .NET MAUI project with `AppShell.xaml` as the root shell
- Pages (`ContentPage`) to navigate between
- Route names for detail pages not in the visual hierarchy

## Shell Visual Hierarchy

Shell uses a four-level hierarchy. Each level wraps the one below it:

```
Shell
 ├── FlyoutItem / TabBar          (top-level grouping)
 │    ├── Tab                     (bottom-tab grouping)
 │    │    ├── ShellContent        (page slot → ContentPage)
 │    │    └── ShellContent        (multiple = top tabs)
 │    └── Tab
 └── FlyoutItem / TabBar
```

- **FlyoutItem** — appears in the flyout menu; contains `Tab` children
- **TabBar** — bottom tab bar with no flyout entry
- **Tab** — groups `ShellContent`; multiple children produce top tabs
- **ShellContent** — each points to a `ContentPage`

### Implicit Conversion

You can omit intermediate wrappers. Shell auto-wraps:

| You write                    | Shell creates                         |
|------------------------------|---------------------------------------|
| `ShellContent` only          | `FlyoutItem > Tab > ShellContent`     |
| `Tab` only                   | `FlyoutItem > Tab`                    |
| `ShellContent` in `TabBar`   | `TabBar > Tab > ShellContent`         |

## Workflow: Set Up AppShell

Use `ContentTemplate` with `DataTemplate` on every `ShellContent` so pages load on demand. Register detail-page routes in the `AppShell` constructor:

```csharp
public AppShell()
{
    InitializeComponent();
    Routing.RegisterRoute("animaldetails", typeof(AnimalDetailsPage));
    Routing.RegisterRoute("editanimal", typeof(EditAnimalPage));
}
```

Route names must be unique, including against visual hierarchy routes; a duplicate throws `ArgumentException`. Always `await Shell.Current.GoToAsync(...)`. Use `//` for absolute hierarchy routes, and `../editanimal` to go back then push.

## Workflow: Pass Data Between Pages

Prefer `IQueryAttributable.ApplyQueryAttributes` on view models; `[QueryProperty]` is the alternative. Pass complex objects without string serialization through `ShellNavigationQueryParameters`:

```csharp
await Shell.Current.GoToAsync("animaldetails",
    new ShellNavigationQueryParameters { { "animal", selectedAnimal } });
```

Receive via `ApplyQueryAttributes` (`query["animal"] as Animal`). Guard async navigation with `args.GetDeferral()` in `OnNavigating`, then `args.Cancel()` if declined and `deferral.Complete()`.

## Back Button Behavior

Customize the back button per page:

```xml
<Shell.BackButtonBehavior>
    <BackButtonBehavior Command="{Binding BackCommand}"
                       IconOverride="back_arrow.png"
                       TextOverride="Cancel"
                       IsVisible="True" />
</Shell.BackButtonBehavior>
```

Properties: `Command`, `CommandParameter`, `IconOverride`, `TextOverride`, `IsVisible`, `IsEnabled`.

## Common Pitfalls

- **Relative routes without registration**: `GoToAsync("somepage")` requires `Routing.RegisterRoute`. Visual hierarchy pages use absolute `//` routes.
- **Wrong absolute route path**: Wrong paths produce silent no-ops, not exceptions.
- **Manipulating Tab.Stack directly**: The navigation stack is read-only. Use `GoToAsync`.

## References

- `references/shell-navigation-api.md` — Full API reference for Shell hierarchy, routes, tabs, flyout, and navigation
- [.NET MAUI Shell Navigation](https://learn.microsoft.com/dotnet/maui/fundamentals/shell/navigation)
- [.NET MAUI Shell Tabs](https://learn.microsoft.com/dotnet/maui/fundamentals/shell/tabs)
- [.NET MAUI Shell Flyout](https://learn.microsoft.com/dotnet/maui/fundamentals/shell/flyout)
- [.NET MAUI Shell Pages](https://learn.microsoft.com/dotnet/maui/fundamentals/shell/pages)
