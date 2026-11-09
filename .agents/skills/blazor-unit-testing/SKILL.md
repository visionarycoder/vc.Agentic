---
name: "blazor-unit-testing"
description: "Test Blazor component rendering and behavior with bUnit, focused dependencies, and deterministic component state."
metadata:
  metadata-version: "1.0.0"
  title: "Blazor Unit Testing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Blazor Unit Testing

Agent tests Blazor components with bUnit and the repository's established .NET test runner.

## When to Use

| Condition | Use |
|---|---|
| User requests unit tests for a `.razor` component | Use this skill |
| Component behavior depends on parameters, cascading values, or events | Use this skill |
| A Blazor component needs coverage for rendering, validation, or state changes | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| The test drives a real browser or user journey | Use `blazor-ui-testing` |
| The target is a pure service or view model | Use `xunit-test-generation` or `mstest-test-authoring` |
| The task selects a Blazor hosting model | Use `blazor-patterns` |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Component | Yes | Agent identifies the component, parameters, event callbacks, and render mode. |
| Behavior | Yes | Agent identifies the visible output, state transition, or validation outcome. |
| Test project | Yes | Agent identifies the bUnit project and its runner. |
| Service dependencies | No | Agent provides deterministic registrations or focused substitutes. |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent reads the component and neighboring bUnit tests. | Inspect markup, code-behind, project references, and fixtures. | Test setup matches local conventions. |
| 2 | Agent configures only required services, cascading values, authentication state, and JS interop. | Review the test context registrations. | Setup stays deterministic and minimal. |
| 3 | Agent renders the component with representative parameters. | Render through bUnit and inspect the DOM. | Initial markup matches the intended contract. |
| 4 | Agent exercises events, forms, validation, and state updates. | Trigger the same interaction through semantic element or component APIs. | Visible output and callbacks prove the behavior. |
| 5 | Agent covers one edge case and one failure or validation path. | Run targeted tests. | Invalid or boundary behavior remains explicit. |

## Component Test Matrix

| Surface | Test | Pass |
|---|---|---|
| Parameters | Render with required, optional, and boundary values. | Output reflects each supported parameter state. |
| Events | Trigger clicks, input, submit, and callback events. | Expected callback payload and rendered state are asserted. |
| Forms | Submit valid and invalid models. | Validation messages and submission behavior are asserted. |
| Cascading state | Provide the required cascading value or authentication state. | Component responds without hidden global state. |
| JS interop | Configure only expected calls and arguments. | Browser-bound behavior stays verifiable without a real browser. |
| Async rendering | Await scheduled renders and task completion. | Tests do not rely on arbitrary delays. |

## Verification Checklist

- [ ] bUnit renders the target component successfully.
- [ ] Tests assert semantic markup or component state instead of CSS-only details.
- [ ] Event callbacks, validation, and async state changes have coverage where applicable.
- [ ] Authentication and cascading state use deterministic test setup.
- [ ] Targeted tests pass in the repository's existing runner.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Tests assert the entire generated HTML string | Query stable semantic elements and assert the relevant contract. |
| Component setup registers every application service | Register only dependencies used by the rendered path. |
| JS interop calls remain unverified | Assert expected identifiers, arguments, and invocation count. |
| Async work is hidden behind sleeps | Await the component task or bUnit render completion. |
