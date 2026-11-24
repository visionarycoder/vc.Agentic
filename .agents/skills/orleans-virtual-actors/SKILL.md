---
name: "orleans-virtual-actors"
description: "Build Orleans grains, clustering, persistence, and silo configuration when agent work involves virtual actor architecture or grain lifecycle behavior."
metadata:
  metadata-version: "1.0.0"
  title: "Microsoft Orleans Virtual Actors"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Microsoft Orleans Virtual Actors

Implement Orleans virtual actor systems with explicit grain contracts, silo configuration, persistence choices, and lifecycle validation.

## When to Use

| Condition | Use |
|---|---|
| Agent authors grain interfaces, grain classes, or silo registration | Use this skill |
| Add stateful grains with Orleans persistence providers | Use this skill |
| Configure clustering, membership, or storage for an Orleans host | Use this skill |
| Agent reviews activation, deactivation, or stateless worker behavior | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Work targets message brokers without actor identity or placement concerns | Use broker or queue guidance |
| Work targets local in-memory objects with no distributed runtime | Use ordinary .NET service patterns |
| Work targets Quartz recurrence semantics | Use Quartz skills |
| Work targets ASP.NET request handlers only | Use Web API or web app guidance |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Grain responsibility | Yes | One business capability per grain type |
| Grain identity model | Yes | Key type, tenancy boundary, or aggregate boundary |
| State model | Yes | Stateless, persisted state, or externalized storage |
| Hosting topology | Yes | Local silo, clustered silo, or hosted client plus silo |
| Validation scope | No | Build, tests, dashboard checks, or lifecycle inspection |

## Workflow

| Step | Action | Pass |
|---|---|---|
| 1 | Map one business capability to one grain interface and implementation. | Grain names and contracts keep one responsibility. |
| 2 | Pick regular, persistent, or stateless-worker grain behavior before editing. | Grain type matches execution and state needs. |
| 3 | Register clustering, storage, and serialization services in host startup. | Host configuration resolves every changed grain dependency. |
| 4 | Keep grain methods async, idempotent where replay matters, and free of blocking waits. | Changed Orleans code has no sync-over-async calls. |
| 5 | Verify activation, persistence, and deactivation. | Build passes and lifecycle behavior matches the selected pattern. |

## Grain Rules

| Topic | Rule |
|---|---|
| Stateless worker | Use `[StatelessWorker]` for CPU-bound fan-out with no durable state; it must not hold persistent state or mutable request-specific fields (use method scope or a regular grain). |
| Grain interfaces | Do not expose transport or controller types; use grain-specific contracts or DTOs. |
| Grain methods | Stay async; no blocking sync-over-async waits. |
| Persistence | Keep the `[PersistentState]` provider name equal to the name registered on the silo; write state only on mutation paths. |
| Cleanup | `await state.ClearStateAsync(); DeactivateOnIdle();` for terminal cleanup. |

## Outputs List

| Output | Description |
|---|---|
| Grain contract plan | Identities, responsibilities, and contract boundaries |
| Pattern selection | Chosen regular, stateless, or persistent grain mapping |
| Silo delta | Clustering, storage, and serialization registrations |
| Verification evidence | Build, test, and lifecycle results |
