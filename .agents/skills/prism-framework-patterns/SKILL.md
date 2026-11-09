---
name: "prism-framework-patterns"
description: "Apply Prism modules, navigation, dialogs, event aggregation, and DI patterns when MVVM work needs structured composition across large desktop or MAUI apps."
metadata:
  metadata-version: "1.0.0"
  title: "Prism Framework Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Prism Framework Patterns

Agent implements Prism with modular composition, navigation services, dialogs, event aggregation, and container-backed view-model activation so large MVVM applications stay organized.

## When to Use

| Condition | Use |
|---|---|
| Agent works on a large WPF or MAUI application with many modules or bounded feature areas. | Agent uses this skill. |
| Agent needs region navigation, module catalogs, or late-loaded features. | Agent uses this skill. |
| Agent needs centralized dialog, navigation, and event aggregation services across many screens. | Agent uses this skill. |
| Agent needs a framework-level ViewModelLocator convention. | Agent uses this skill. |

## When Not to Use

| Condition | Route |
|---|---|
| Agent needs lightweight MVVM with generated properties and commands only. | Agent uses `communitytoolkit-mvvm`. |
| Agent authors a custom MVVM generator or analyzer package. | Agent uses `roslyn-mvvm-source-generators`. |
| Agent works on WinUI 3 without an established Prism stack. | Agent uses `winui3-patterns` or `communitytoolkit-mvvm`. |
| Agent edits one small screen with no modular composition needs. | Agent uses the matching platform MVVM skill. |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Platform target | Yes | Identify WPF, MAUI, or mixed solution boundaries. |
| Module boundaries | Yes | Identify feature packages, shell ownership, and shared services. |
| Navigation map | Yes | Identify pages, regions, routes, and dialog entry points. |
| Container choice | No | Identify `Prism.DryIoc`, `Prism.Unity`, or the project default. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1 | Agent maps module boundaries, shell ownership, navigation routes, and dialog entry points. | Review the feature map. | Composition ownership stays explicit. |
| 2 | Agent aligns startup with one Prism container path. | Build and inspect startup registration. | Package references and container setup stay coherent. |
| 3 | Agent converts touched view models to Prism patterns and locator activation. | Run targeted tests or one screen pass. | View-model activation and command behavior succeed. |
| 4 | Agent wires regions, modules, dialogs, and typed events for the touched scope. | Navigate one region path and one dialog path. | Composition and dialog flow behave as designed. |
| 5 | Agent verifies module load order and confirmation paths. | Start the shell and leave one dirty screen. | Startup and guarded navigation stay stable. |

## Prism Pattern Matrix

| Concern | Pattern | Pass |
|---|---|---|
| Observable state | `BindableBase` | `SetProperty` updates state and notifications once per change |
| Commands | `DelegateCommand` or `DelegateCommand<T>` | Command enablement follows view-model state |
| View activation | `ViewModelLocator` and registration conventions | Intended view model activates without code-behind wiring |
| Region navigation | Named regions and `IRegionManager` | Region content changes without hard references between views |
| Module composition | `IModule` and module catalogs | Views and services load in the intended order |
| Dialogs and events | `IDialogService` and typed `PubSubEvent<T>` contracts | Interaction stays explicit, typed, and bounded |

## Module Matrix

| Area | Pattern | Pass |
|---|---|---|
| Module registration | Register services, views, and region targets inside each `IModule`. | Each module loads without startup ordering defects. |
| Region naming | Keep region names stable and explicit. | Host and target names match exactly. |
| Navigation parameters | Pass compact parameters or IDs. | Target views resolve required state without singleton coupling. |
| Confirmation | Wire confirmation into navigation interfaces or dialog services. | User intent stays explicit and state loss stays controlled. |

## Reference Files

| File | Purpose |
|---|---|
| [references/framework-comparison-and-examples.md](references/framework-comparison-and-examples.md) | Package guidance, Prism-versus-CommunityToolkit comparison, examples, platform hooks, MCP hooks, pitfalls, and outputs. |

## Verification Checklist

| Item | Test | Pass |
|---|---|---|
| One container package owns startup. | Inspect startup and package references. | `Prism.DryIoc` or `Prism.Unity` owns registration, not both. |
| ViewModelLocator resolves touched views. | Open or resolve one touched view. | The intended view model activates automatically. |
| Region names and targets align. | Inspect XAML hosts and navigate once. | Region navigation resolves the expected content. |
| Dialog contracts stay explicit. | Trigger one dialog and inspect result handling. | Request and result data stay bounded. |
| Event contracts stay typed. | Publish one event path. | Subscribers depend on `PubSubEvent<T>` contracts only. |
