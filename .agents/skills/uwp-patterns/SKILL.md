---
name: "uwp-patterns"
description: "Maintain legacy UWP apps with adaptive UI, MVVM boundaries, Windows integration, and explicit migration decisions toward WinUI 3 when an agent changes user-facing features."
metadata:
  metadata-version: "1.0.0"
  title: "UWP Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# UWP Patterns

Agent maintains UWP applications with adaptive layouts, observable state, Windows contract integration, and explicit containment of legacy platform constraints while migration pressure stays visible.

## When to Use

| Condition | Use |
|---|---|
| Agent maintains an existing UWP application that remains in service. | Agent uses this skill. |
| Agent adds adaptive XAML, visual states, or Windows shell integration to UWP. | Agent uses this skill. |
| Agent stabilizes a UWP feature while migration planning continues. | Agent uses this skill. |
| Agent evaluates keep-versus-migrate direction for a touched UWP area. | Agent uses this skill. |

## When Not to Use

| Condition | Route |
|---|---|
| Agent starts a new Windows desktop application. | Agent uses `winui3-patterns`. |
| Agent builds cross-platform UI. | Agent uses `maui-patterns`. |
| Agent modernizes WPF desktop UI. | Agent uses `wpf-fluent-ui`. |
| Agent works on testing only. | Agent uses `ui-testing-patterns`. |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Current app footprint | Yes | Footprint identifies pages, controls, app model assumptions, and device-family dependencies. |
| Breakpoint map | Yes | Map identifies narrow, medium, and wide layouts. |
| Integration scope | Yes | Scope identifies notifications, file pickers, share, background tasks, or activation paths. |
| Migration pressure | No | Pressure identifies unsupported controls, packaging limits, or roadmap risks. |
| Distribution model | No | Model identifies Store, enterprise, or sideload assumptions. |

## UWP Guidance

- Layout adaptation uses `VisualStateManager`, `AdaptiveTrigger`, and flexible panels for narrow, medium, and wide states; give each width explicit visibility rules.
- Prefer `x:Bind`; view models own commands, validation, and selection; Windows contract APIs sit behind services or coordinators.
- Data-heavy surfaces use list virtualization and bounded item templates.
- Record a keep, isolate, or migrate decision for each touched area; no silent scope growth in legacy code.

## Migration Decision Matrix

| Condition | Decision |
|---|---|
| UWP-only contract behavior with no near-term replacement need | Keep and isolate; document the coupling. |
| Standard navigation, forms, lists, and dialogs with rising maintenance cost | Prepare migration to WinUI 3 with shared seams first. |
| Packaging or Store assumptions block required product changes | Escalate migration priority and state the constraints in task output. |
| Recurring control-gap workarounds | Put new investment in WinUI 3. |

## Verification Checklist

| Check | Pass |
|---|---|
| Resize across supported widths. | Each breakpoint stays usable. |
| Review changed files. | Commands and validation stay in view models; contracts stay behind services. |
| Exercise one data-heavy screen. | Interactions stay responsive. |
| Review task output. | Each touched scope has a keep, isolate, or migrate decision. |

## Outputs

- Adaptive-state map
- UWP contract containment plan
- Keep, isolate, or migrate decision summary
- Legacy risk notes for touched areas
- Focused validation steps for supported Windows targets
