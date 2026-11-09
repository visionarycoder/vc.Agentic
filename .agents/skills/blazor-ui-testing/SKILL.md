---
name: "blazor-ui-testing"
description: "Test Blazor user journeys in a real browser with accessible selectors, deterministic data, and focused end-to-end assertions."
metadata:
  metadata-version: "1.0.0"
  title: "Blazor UI Testing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Blazor UI Testing

Agent tests Blazor user journeys in a real browser when component unit tests do not prove hosting, navigation, or browser behavior.

## When to Use

| Condition | Use |
|---|---|
| User requests browser tests for a Blazor application | Use this skill |
| The behavior depends on routing, render modes, browser storage, or JS interop | Use this skill |
| A critical journey needs coverage across navigation, forms, and visible outcomes | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| The test targets isolated component rendering | Use `blazor-unit-testing` |
| The task tests a pure service or view model | Use `xunit-test-generation` |
| The application is WPF, MAUI, or WinUI | Use `ui-testing-patterns` |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| User journey | Yes | Agent identifies start state, actions, and visible success or failure outcome. |
| Application host | Yes | Agent identifies startup command, URL, authentication, and render mode. |
| Selector strategy | Yes | Agent identifies accessible roles, labels, names, and stable test IDs. |
| Data setup | Yes | Agent identifies deterministic seed, reset, or fixture behavior. |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent reads existing browser tests and application startup configuration. | Inspect test project, host settings, and routes. | Runner and environment are explicit. |
| 2 | Agent selects accessible selectors before writing actions. | Review selectors against rendered markup. | Selectors survive styling and layout changes. |
| 3 | Agent starts the application with deterministic configuration. | Probe the health or landing route. | The host responds before the journey begins. |
| 4 | Agent drives one critical journey with explicit checkpoints. | Run the targeted browser test. | Navigation, input, and visible outcomes pass. |
| 5 | Agent covers one invalid input or recovery path. | Run the negative path. | The user-visible error and recovery behavior are asserted. |

## UI Test Matrix

| Surface | Test | Pass |
|---|---|---|
| Routing | Navigate through the supported link or route. | URL and page heading match the destination. |
| Forms | Fill fields by label and submit through the visible action. | Validation or success state is visible and specific. |
| Render modes | Exercise the mode that owns the behavior. | Server, WebAssembly, or auto behavior stays observable. |
| Browser APIs | Exercise storage, download, or interop through the real browser path. | Browser outcome is asserted without timing guesses. |
| Accessibility | Query roles, labels, names, and keyboard flow. | Journey remains available to assistive technology users. |

## Verification Checklist

- [ ] The application starts through an existing repository command.
- [ ] Selectors use roles, labels, accessible names, or stable test IDs.
- [ ] Tests assert URL, visible state, and user-facing errors.
- [ ] Tests avoid fixed sleeps and uncontrolled external data.
- [ ] Targeted browser tests pass in the supported environment.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Browser tests repeat every component unit assertion | Keep browser scope on hosting and user-visible integration behavior. |
| Selectors depend on CSS classes or element order | Use semantic selectors or explicit test IDs. |
| Authentication and data state vary between runs | Use a deterministic test identity and resettable fixtures. |
| Tests pass only with long fixed delays | Wait on URL, role, text, or network-ready state. |
