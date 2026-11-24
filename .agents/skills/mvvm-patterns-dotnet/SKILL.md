---
name: "mvvm-patterns-dotnet"
description: "Establish MVVM architecture, observable state, and platform-specific boundaries when agent implements or reviews .NET UI features."
metadata:
  metadata-version: "1.0.0"
  title: ".NET MVVM Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# .NET MVVM Patterns

Agent structures .NET UI features so models hold domain data, views hold presentation markup, and view models expose observable state and commands without business logic in code-behind.

## When to Use

| Condition | Use |
|---|---|
| Agent creates a new WPF, MAUI, WinUI 3, UWP, or Avalonia screen. | Use this skill. |
| Agent moves business logic from code-behind into a testable presentation layer. | Use this skill. |
| Agent needs manual `INotifyPropertyChanged` or `ObservableCollection<T>` patterns. | Use this skill. |
| Compare MVVM against MVC or MVP for an existing UI architecture choice. | Use this skill. |

## When Not to Use

| Condition | Route |
|---|---|
| Agent edits backend services, APIs, or data access only. | Use the matching service skill. |
| Agent changes styling, layout, or control templates only. | Use the platform UI skill. |
| Agent works in a project with an established non-MVVM presentation pattern. | Follow the existing pattern. |
| Agent focuses on command wiring details only. | Use `commands-behaviors-patterns`. |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Screen workflow | Yes | Workflow identifies state, user actions, and transitions. |
| Domain model boundaries | Yes | Boundaries identify model ownership and transformation points. |
| Target platforms | Yes | Scope identifies WPF, MAUI, WinUI 3, UWP, or Avalonia. |
| Validation scope | No | Scope identifies editable fields and error rules. |
| Navigation pattern | No | Pattern identifies page, window, or shell transitions. |

## Rules

- Keep code-behind to composition only; view models expose plain state, not control types.
- Bulk refresh of a bound list: replace collection contents or the view-model instance, never mutate control state directly, so data and selection stay coherent.
- Platform binding source: WPF and Avalonia use `DataContext`; MAUI uses `BindingContext`.
- Prefer CommunityToolkit.Mvvm generators where the project already allows them; match Prism when the app already uses it; otherwise implement notifications manually.

## MCP Hooks

| Task | MCP Tool | Assistance |
|---|---|---|
| Find view, view-model, and code-behind ownership drift | `github-mcp-server-search_code` | Locates bindings, commands, notification paths, and code-behind logic. |
| Inspect versioned screen files in branches or pull requests | `github-mcp-server-get_file_contents` | Reads XAML, view-model, and project files without local branch switches. |
| Review prior MVVM architecture decisions | `github-mcp-server-search_pull_requests` | Surfaces earlier refactors, naming patterns, and reviewer guidance. |

## Outputs

| Output | Contents |
|---|---|
| Responsibility map | Model, view, and view-model ownership for the feature |
| State pattern | Observable property, collection, and validation choices |
| Platform notes | Binding, navigation, and lifecycle decisions |
| Verification plan | Focused UI update and architecture checks |
