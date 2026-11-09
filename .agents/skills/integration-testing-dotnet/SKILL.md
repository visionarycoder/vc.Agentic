---
name: "integration-testing-dotnet"
description: "Write integration tests that exercise components together across layers against real or emulated resources."
metadata:
  metadata-version: "1.0.0"
  title: "Integration Testing in .NET"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Integration Testing in .NET

Load this skill when `integration-tester` writes tests in `tests/integration/**`. Also load `mstest-test-authoring` and `efcore-testing-patterns`.

## When to use

Use an integration test when the behavior depends on two or more components working together or on a real resource. Do not re-test unit logic.

## Procedure

1. Read the test specification row for each ID. Name each test `<Component>_<Behavior>_<Expected>` and tag it with the ID using the `test-tagging` skill.
2. Name the project `*.IntegrationTests`. Reference `*.TestCommon` for fixtures, fakes, and builders. Never create a private copy of harness code.
3. Build the system under test through the real dependency-injection composition. Replace only external systems the specification names with fakes from `tests/common/Fakes/`.
4. Arrange data with builders. Isolate each test with a transaction rollback or a per-test schema.
5. Act through the public contract of the entry component (Manager for a use case, Access for a resource test). Never call internals.
6. Assert on the observable result: return value, persisted state, emitted message, or Problem Details body. Assert on one behavior per test.
7. Cover for each use case: the happy path, a failure path across a layer boundary, and a cancellation path.

## Layer-Specific Checks

| Flow | Verify |
|---|---|
| Client → Manager | Request mapping, authorization result, error contract |
| Manager → Engine | Control flow follows Engine results; no business rule in the Manager |
| Manager → Access | Persisted state matches the design after the operation |
| Access → resource | Queries return expected rows; migrations apply cleanly to an empty database |

## Rules

- Use no production data or connections.
- Clean up after every run. A leftover resource is a defect.
- Never use `Thread.Sleep`. Wait on a condition with a timeout.
- A flaky test is a defect. Fix the cause or return it to `test-architect`. Never add retries to hide it.
