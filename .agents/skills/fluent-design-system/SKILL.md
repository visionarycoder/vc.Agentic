---
name: "fluent-design-system"
description: "Agent applies Fluent Design System 2 patterns so Windows-aligned interfaces feel calm, layered, readable, and native on current Windows surfaces."
metadata:
  metadata-version: "1.0.0"
  title: "Fluent Design System"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Fluent Design System

Agent applies Fluent Design System 2 patterns so Windows-aligned interfaces feel calm, layered, readable, and native on current Windows surfaces.

> **For comprehensive Fluent 2 reference:** Agent uses `fluent2-design-comprehensive` when work needs detailed design tokens, cross-platform component guidance, Copilot/AI patterns, content engineering, or complete accessibility specifications.

## When to Use

| Condition | Use |
|---|---|
| Agent designs a Windows desktop surface, shell, dialog, menu, or page. | Agent uses this skill. |
| Agent updates Mica, Acrylic, Smoke, elevation, or reveal treatment. | Agent uses this skill. |
| Agent tunes motion, tokens, or control states to match Fluent 2. | Agent uses this skill. |
| Agent aligns a product surface with Windows 11 visual expectations. | Agent uses this skill. |

## When Not to Use

| Condition | Route |
|---|---|
| Agent works on cross-platform layout with no Windows-specific design system. | Agent uses `ui-design-principles`. |
| Agent works on WCAG conformance, focus, narration, or keyboard support as the primary goal. | Agent uses `ui-accessibility-standards`. |
| Agent updates only backend services or non-visual code. | Agent uses the matching backend skill. |
| Agent targets Apple, Material, or web-brand design language over Fluent. | Agent uses the matching platform design skill. |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Surface inventory | Yes | Inventory identifies app shell, content surfaces, transient surfaces, and action surfaces. |
| Theme scope | Yes | Scope identifies light, dark, or high-contrast coverage. |
| Platform target | Yes | Target identifies WinUI 3, WPF, MAUI on Windows, or Windows-aligned web scope. |
| Motion scope | No | Scope identifies transitions, connected animations, and reduced-motion boundaries. |
| Brand constraints | No | Constraints identify accent, icon, or typography limits. |

## Foundation Matrix

| Principle | Preferred Pattern | Avoid | Pass |
|---|---|---|---|
| Depth | Use a small elevation scale with consistent layer roles. | Many ad hoc shadow values. | Users distinguish base, active, and transient layers instantly. |
| Motion | Use short entrance, exit, and connected motion tied to task continuity. | Decorative motion that competes with content. | Motion explains change and ends quickly. |
| Tokens | Use shared color, radius, spacing, and typography tokens. | One-off visual constants in each view. | Sibling surfaces render as one system. |

## Component Decision Matrix

| Area | Select | Select When | Pass |
|---|---|---|---|
| Transition | Connected or content continuity motion | Navigation preserves object or place continuity. | Users track what changed. |
| Focus treatment | Strong ring or reveal tied to control state | Keyboard or assistive input path enters the control. | Focus remains visible in every theme. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1 | Agent maps surface roles, layer roles, and action priority before edits. | Review changed views and shell structure. | Each region has one clear purpose. |
| 2 | Agent assigns Fluent 2 materials, elevation, and token usage by role. | Compare root, content, and transient surfaces. | Material use matches surface role. |
| 3 | Agent applies control states for rest, hover, focus, pressed, disabled, and selected behavior. | Trigger each state once. | States remain clear in every theme. |
| 4 | Agent tunes motion for entrance, exit, continuity, and reduced-motion support. | Exercise one navigation flow and one transient surface. | Motion stays brief and purposeful. |
| 5 | Agent validates theme parity, contrast, and visual calmness. | Review light, dark, and high-contrast output. | The same information hierarchy stays intact. |

## GitHub MCP Hooks

| Task | GitHub MCP Tool | Assistance |
|---|---|---|
| Locate XAML, CSS, token maps, and component templates | `github-mcp-server-search_code` | Finds theme dictionaries, brush keys, motion settings, and control-state definitions. |
| Inspect checked-in style and asset files | `github-mcp-server-get_file_contents` | Reads resource dictionaries, icon sets, and design-token files without a local clone of another repo. |
| Review UI-focused pull request diffs | `github-mcp-server-pull_request_read` | Surfaces changed visual assets, XAML, and review comments tied to Fluent updates. |
| Inspect build or UI test workflow failures | `github-mcp-server-actions_list` and `github-mcp-server-get_job_logs` | Exposes packaging, screenshot, or Windows runner failures. |

## Verification Checklist

| Check | Test | Pass |
|---|---|---|
| Motion quality | Trigger navigation and transient interactions. | Motion explains change without distraction. |
| Theme parity | Review light, dark, and high-contrast output. | Meaning and hierarchy persist in each theme. |
| Token reuse | Inspect changed styling assets. | Shared tokens replace one-off values. |

## Common Pitfalls

| Pitfall | Agent Fix |
|---|---|
| Elevation values drift across screens. | Agent reduces the layer scale to repeatable roles. |
| Motion length exceeds task value. | Agent shortens duration and removes non-informational movement. |

## Outputs

- Fluent 2 surface-role map
- Material and elevation decision table
- Motion and state treatment plan
- Theme-parity validation summary
- Concrete remediation list for non-native or noisy surfaces
