---
name: "mstest-wpf-testing-patterns"
description: "Test WPF view models and desktop logic through MSTest v4, command-based assertions, and view-only boundaries that avoid fragile UI coupling."
metadata:
  metadata-version: "1.0.0"
  title: "WPF Testing Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# WPF Testing Patterns

Agent protects WPF behavior with fast tests around view models, commands, validation, and service boundaries instead of relying on broad UI automation.

## When to Use

| Condition | Use |
|---|---|
| Agent adds or changes view-model behavior in a WPF feature. | Agent uses this skill. |
| Agent needs regression coverage for commands, property changes, or validation. | Agent uses this skill. |
| Agent needs MSTest v4 coverage without launching full WPF windows. | Agent uses this skill. |

## When Not to Use

| Condition | Use |
|---|---|
| Agent changes only pure styling with no state or command behavior. | Agent uses manual visual verification. |
| Agent needs a broad test-suite generation workflow. | Agent uses a dedicated testing bundle. |
| Agent focuses on UI automation for rendering-only issues. | Agent limits work to targeted UI checks. |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Target class | Yes | Target identifies the view model or service under test. |
| Expected interactions | Yes | Interactions identify commands, notifications, and collaborator effects. |
| Test doubles | No | Doubles identify fakes or mocks for collaborators. |
| Coverage goals | No | Goals identify risky paths and boundary conditions such as null input, empty collections, and selection changes. |
| UI smoke scope | No | Scope identifies any small rendering checks outside unit tests. |

## Workflow

| Step | Agent action | Output | Test | Pass |
|---|---|---|---|---|
| 1. Isolate testable logic | Agent extracts dialogs, navigation, dispatcher work, and transport dependencies behind interfaces. | Test seam map | Agent instantiates the target in a test. | The target runs without WPF runtime dependencies. |
| 2. Use MSTest v4 | Agent places tests in an MSTest v4 project that matches repository conventions. | Test project | Agent runs targeted tests. | Test discovery succeeds. |
| 3. Use simple fakes | Agent uses deterministic fakes for straightforward collaborators and uses mocks only where interaction verification needs them. | Test doubles | Agent inspects collaborator effects. | Tests read behavior directly and stay easy to diagnose. |
| 4. Drive public behavior | Agent exercises commands, properties, and validation through the public surface instead of private helpers. | Behavior tests | Agent runs the target tests. | Failures map to user-visible behavior. |
| 5. Cover async and error flows | Agent tests busy flags, cancellations, failed service calls, and recovery state. | Async-path tests | Agent forces failures and cancellations. | The target resets state correctly after non-happy paths. |
| 6. Limit UI automation | Agent reserves UI automation for WPF-only concerns such as keyboard traversal, accessibility, or virtualization quirks. | UI smoke scope | Agent reviews the scope. | UI automation remains small and justified. |

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Agent tests private helpers instead of user-visible behavior. | Agent drives tests through public commands and properties. |
| Agent keeps WPF globals inside view models. | Agent extracts those concerns behind interfaces. |
| Agent stops at null checks and shallow assertions. | Agent asserts state transitions and collaborator effects. |
| Agent uses UI automation for every rule. | Agent keeps UI automation for WPF-specific concerns only. |

## Verification Matrix

| Test | Run | Pass |
|---|---|---|
| Targeted tests | `dotnet test [test-project].csproj` | All targeted tests pass |
| Coverage check | `dotnet test [test-project].csproj --collect:"XPlat Code Coverage"` when the project already uses coverage | Coverage run succeeds |
| Manual smoke pass | Small keyboard or binding pass when required | No WPF-only regression remains |

## Verification Checklist

- [ ] Agent tests commands through their public command surface.
- [ ] Agent asserts property changes, validation states, and collaborator effects.
- [ ] Agent covers one failure or cancellation path for each changed behavior.
- [ ] Agent keeps most coverage outside UI automation.
- [ ] Agent uses MSTest v4 conventions.

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [wpf-testing-patterns-alternative-1](references/contexts/wpf-testing-patterns-alternative-1/guide.md)
