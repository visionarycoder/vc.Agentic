---
name: "ui-testing-patterns"
description: "Implement UI automation and visual verification for WPF, .NET MAUI, and WinUI 3 with platform-fit tools, stable selectors, deterministic data, and observable waits."
metadata:
  metadata-version: "1.0.0"
  title: "UI Testing Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# UI Testing Patterns

Agent implements UI automation around stable user journeys, platform-fit tooling, deterministic data, and observable waits so desktop and cross-platform UI stays verifiable without fragile screen-driving scripts.

## When to Use

| Condition | Use |
|---|---|
| Agent verifies end-to-end behavior across WPF, MAUI, or WinUI 3 surfaces. | Agent uses this skill. |
| Agent adds coverage for focus, keyboard flow, dialogs, navigation, or rendered state. | Agent uses this skill. |
| Agent selects Appium, FlaUI, WinAppDriver, or an existing visual-regression stack. | Agent uses this skill. |
| Agent needs assertions on real UI behavior that unit tests do not cover. | Agent uses this skill. |

## When Not to Use

| Condition | Route |
|---|---|
| Agent tests pure view-model logic or service coordination. | Agent uses the matching unit-test or MVVM skill. |
| Agent changes only static documentation or non-UI code. | Agent uses the matching area skill. |
| Agent seeks snapshot-only coverage with no behavioral assertion. | Agent adds behavior assertions first. |
| Agent keeps a legacy coded UI suite alive with no new investment. | Agent contains work to maintenance-only scope. |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Target platforms | Yes | Platforms identify WPF, MAUI, WinUI 3, or mixed scope. |
| User journeys | Yes | Journeys identify navigation, input, dialogs, and expected outcomes. |
| Test environment | Yes | Environment identifies emulator, simulator, desktop host, CI agent, and display constraints. |
| Selector strategy | Yes | Strategy identifies automation IDs, accessibility IDs, names, or semantic properties. |
| Visual scope | No | Scope identifies screenshot baselines, tolerance, and golden-path surfaces. |

## Tool Selection Matrix

| Platform | Preferred Tool | Pass |
|---|---|---|
| WPF | FlaUI | Controls resolve through stable UIA properties. |
| MAUI | Appium | Accessibility identifiers drive the journey. |
| WinUI 3 | WinAppDriver or the Appium Windows path already present in the repo | Startup and control lookup are deterministic. |
| Shared rendering | Visual-regression tool already in the repo; no new tool | Baselines only for layout- or brand-critical surfaces. |
| Legacy coded UI | Existing harness, maintenance-only | No new suite growth on deprecated tooling. |

## Test Design

| Concern | Pattern | Test |
|---|---|---|
| Data setup | Fixtures, launch arguments, or seeded services | Run the same journey twice; initial state is identical. |
| Waiting | Wait on visible or enabled state or window readiness, never fixed sleeps | Run once under load; search touched tests for sleeps. |
| Dialogs | Assert title, content, action result, and the state returned to after close | Complete one dialog path. |
| Failure paths | Assert visible recovery state and blocked invalid actions | Trigger one negative case. |
| Visual checks | Snapshot only layout- or brand-critical surfaces | Compare one approved baseline. |

Add behavior assertions before any snapshot-only coverage.

## GitHub MCP Hooks

| Task | GitHub MCP Tool | Assistance |
|---|---|---|
| Find automation IDs, accessibility IDs, and existing UI tests | `github-mcp-server-search_code` | Locates selectors, driver setup, and test harness utilities. |
| Inspect checked-in test configs and baselines | `github-mcp-server-get_file_contents` | Reads test project files, run settings, and screenshot assets. |
| Review UI test pull request diffs | `github-mcp-server-pull_request_read` | Surfaces changed selectors, tests, and baseline files together. |
| Diagnose CI failures for UI automation | `github-mcp-server-actions_list` and `github-mcp-server-get_job_logs` | Exposes host startup, emulator, desktop runner, or screenshot failures. |

## Verification Checklist

| Check | Pass |
|---|---|
| Tool fits platform; selectors are automation IDs or accessibility identifiers, not coordinates or index lookups. | Host and driver connect reliably. |
| Tests assert visible success, failure, or recovery states and avoid sleep-based timing. | Snapshots cover only high-value surfaces. |

## Outputs

- Platform-to-tool selection matrix
- Stable selector strategy
- Core user-journey automation plan
- Visual regression scope summary
- Host and CI verification steps
