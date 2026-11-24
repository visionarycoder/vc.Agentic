---
name: "angular-to-vue3-migration"
description: "Map Angular components, templates, services, guards, and forms to Vue 3 patterns with parity-focused validation."
metadata:
  metadata-version: "1.0.0"
  title: "Angular to Vue 3 Migration"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-11"
  collection: "optional"
---

# Angular to Vue 3 Migration

Agent ports Angular features to Vue 3 without feature drift.

## When to Use

| Condition | Route |
|---|---|
| Team migrates an Angular feature to Vue 3 | Agent uses this skill |
| Team needs full program planning across many features | Agent uses `angular-vue-migration-orchestrator` |
| Team needs Angular cleanup before porting | Agent uses `angular-anti-patterns` |

## Concept Map

| Angular source | Vue target | Test | Pass |
|---|---|---|---|
| `@Component` class | `<script setup lang="ts">` SFC | Build migrated feature | Component compiles |
| `@Input()` | `defineProps()` | Run component tests | Props bind as defined |
| `@Output()` | `defineEmits()` | Trigger emitted event | Parent receives payload |
| Service | composable or typed client | Run unit tests | Shared logic stays reusable |
| `BehaviorSubject` | `ref` or Pinia store | Run state tests | Consumers update on change |
| Route guard | Vue navigation guard | Open protected route | Guard redirects or allows access |
| Reactive form | `v-model` plus validation layer | Submit invalid and valid data | Errors and success match baseline |
| Template directives | `v-if`, `v-for`, bindings | Render migrated view | DOM output matches baseline |

## Migration Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent maps Angular routes, components, services, and tests | Review migration sheet | Each source artifact has a Vue target |
| 2. Port state | Agent converts shared state to composables or Pinia | Run state tests | State flows match Angular behavior |
| 3. Port UI | Agent converts templates and component contracts | Run component tests | Props, emits, and slots work |
| 4. Port navigation | Agent converts routes and guards | Run route smoke tests | Route access and deep links stay stable |
| 5. Port forms | Agent converts validation and submit flows | Submit form paths | Error and success flows match baseline |
| 6. Verify parity | Agent compares Angular and Vue journeys | Run parity suite | Each migrated journey passes |

## Parity Matrix

| Journey | Angular baseline | Vue target |
|---|---|---|
| Read-only list | Same records and empty state | Same records and empty state |
| Create form | Same validation messages | Same validation messages |
| Protected route | Same redirect or deny result | Same redirect or deny result |
| Error response | Same user-visible failure state | Same user-visible failure state |

## Validation

| Check | Test | Pass |
|---|---|---|
| Type health | Run `npm run type-check` | Exit code = 0 |
| Unit health | Run `npm run test` | Exit code = 0 |
| Route health | Run migrated route smoke tests | Each target route resolves |
| Form parity | Compare invalid and valid submissions | Messages and results match baseline |
| Accessibility parity | Run changed page accessibility checks | No new violation appears |
| E2E parity | Run critical Playwright suite | Critical journeys pass |

## Output

Agent returns the source-to-target map, migrated files, parity results, and remaining blockers.
