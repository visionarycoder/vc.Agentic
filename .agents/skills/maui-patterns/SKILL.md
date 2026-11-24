---
name: "maui-patterns"
description: "Agent implements .NET MAUI features with thin views, observable view models, Shell navigation, shared styling, and explicit seams for Android, iOS, Windows, and Mac Catalyst behavior."
metadata:
  metadata-version: "1.0.0"
  title: ".NET MAUI Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# .NET MAUI Patterns

Agent implements .NET MAUI features with thin views, observable view models, Shell navigation, shared styling, and explicit seams for Android, iOS, Windows, and Mac Catalyst behavior.

## When to Use

| Condition | Use |
|---|---|
| Agent builds or updates a MAUI page, shell flow, or cross-platform feature. | Agent uses this skill. |
| Agent adds MVVM state, validation, or async command flow to a MAUI screen. | Agent uses this skill. |
| Agent adds platform-specific behavior through handlers, partial classes, or services. | Agent uses this skill. |
| Agent aligns one feature across Android, iOS, Windows, and Mac Catalyst. | Agent uses this skill. |

## When Not to Use

| Condition | Route |
|---|---|
| Agent works on WinUI 3 desktop-only UI. | Agent uses `winui3-patterns`. |
| Agent works on WPF desktop UI. | Agent uses `wpf-fluent-ui`. |
| Agent works on backend APIs or domain logic only. | Agent uses the matching backend skill. |
| Agent focuses on UI automation only. | Agent uses `ui-testing-patterns`. |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Feature workflow | Yes | Workflow identifies pages, dialogs, commands, and state transitions. |
| Navigation map | Yes | Map identifies Shell routes, query contracts, and back-stack rules. |
| Platform scope | Yes | Scope identifies Android, iOS, Windows, and Mac Catalyst differences. |
| Theme tokens | No | Tokens identify colors, spacing, typography, and imagery. |
| Device capabilities | No | Capabilities identify file pickers, permissions, sensors, and notifications. |

## Project-Specific Rules

- Pass compact identifiers through Shell query parameters and reload detail data in the destination view model; never pass large objects.
- Wrap device APIs behind interfaces with platform implementations instead of calling them from view models.
- Build every targeted platform in scope and exercise one success path and one failure path.

## GitHub MCP Hooks

| Task | GitHub MCP Tool | Assistance |
|---|---|---|
| Find Shell routes, handlers, platform folders, and XAML views | `github-mcp-server-search_code` | Locates route registration, partial classes, and platform-service seams. |
| Inspect checked-in MAUI assets and project files | `github-mcp-server-get_file_contents` | Reads `.csproj`, resource dictionaries, app manifests, and launch settings. |
| Review mobile or desktop build workflow runs | `github-mcp-server-actions_list` and `github-mcp-server-get_job_logs` | Exposes Android, iOS, Windows, or Mac build failures tied to UI changes. |
| Review cross-platform feature diffs | `github-mcp-server-pull_request_read` | Surfaces changed views, handlers, and platform-specific files together. |

## Outputs

- Page and route ownership map
- View-model and command pattern selection
- Platform seam plan for Android, iOS, Windows, and Mac Catalyst
- Shared styling and theming plan
- Focused verification steps per platform in scope
