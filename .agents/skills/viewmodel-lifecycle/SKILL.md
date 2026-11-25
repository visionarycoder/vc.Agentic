---
name: "viewmodel-lifecycle"
description: "Manage initialization, navigation state, cleanup, and memory-safety boundaries when agent implements or reviews presentation-model lifecycles in UI applications."
metadata:
  metadata-version: "1.0.0"
  title: "View Model Lifecycle"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-24"
  collection: "optional"
---

# View Model Lifecycle

Agent manages presentation-model creation, activation, navigation data, state preservation, and cleanup so long-lived screens stay correct and leak-free.

## When to Use

- Work initializes a screen model from navigation, activation, or shell events.
- Work preserves or restores screen state across navigation or suspension.
- Work disposes subscriptions, message registrations, timers, streams, or async resources.
- Work investigates stale-event or memory-retention defects.

Do not use for stateless views with no retained resources or for server-side request lifecycles.

## Required Inputs

Record the creation and navigation path, the state-preservation scope, the resource inventory (events, messengers, timers, streams, disposables), the platform lifecycle hooks, and any caching policy (reuse, eviction, recreation).

## Rules

| Topic | Rule |
|---|---|
| Startup | Keep constructors free of async or I/O work. Load in an explicit initialization or activation method. |
| Parameters | Pass stable identifiers or compact records. Never pass live services, controls, or views in navigation payloads. |
| Reentry | Distinguish first activation from resumed activation and align reload behavior with the cache policy. |
| Cache policy | Choose recreate, cache-per-route, or shell-singleton and record reuse, reset, and eviction before implementing state restore. |
| State restore | Restore only durable, user-meaningful state such as filters, selection, and form input. Never restore transient or unsafe state. |
| Cancellation | Link long-running initialization to screen lifetime and ignore late results after deactivation. |
| Cleanup | Unsubscribe events and message registrations on deactivation or disposal unless the registration is weak by default. Avoid cached instances acting as event roots. |
| Platform hooks | Use the native lifecycle surface of the target platform and keep ownership of each hook explicit. |

## Workflow

1. Map creation, activation, navigation, suspension, and disposal points.
2. Implement initialization and parameter handling with compact payloads.
3. Select the cache policy and navigate away and back to confirm the behavior.
4. Preserve durable state and reject unsafe restore paths.
5. Add disposal, message cleanup, weak events, and cancellation handling; close the screen and trigger late activity.
6. Repeat open-close or navigation cycles and confirm resource counts and event activity stay stable.

## Verification Checklist

- No duplicate initial load occurs outside the selected policy.
- Payloads contain no live control or service references.
- Resumed or recreated screens return only meaningful user state.
- Closed screens receive no late events or messages.
- Repeated navigation or tab activation leaves cached behavior stable.

## Outputs

- Lifecycle map for creation, activation, navigation, and disposal
- Cache-versus-recreate decision record
- State preservation and restoration plan
- Cleanup plan for events, messengers, disposables, and weak references
- Verification steps for lifecycle correctness and memory safety
