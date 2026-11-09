---
name: "xunit-test-generation"
description: "Create focused xUnit tests for .NET behavior while matching repository conventions and proving meaningful outcomes."
metadata:
  metadata-version: "1.0.0"
  title: "xUnit Test Generation"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# xUnit Test Generation

Agent creates or updates xUnit tests for .NET production behavior.

## When to Use

| Condition | Use |
|---|---|
| User requests xUnit tests or a new xUnit test class | Use this skill |
| A .NET change needs focused unit coverage in an xUnit project | Use this skill |
| Existing xUnit tests need additional edge or failure coverage | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| The project uses MSTest as its established runner | Use `mstest-test-authoring` or `mstest-test-authoring` |
| The task tests rendered Blazor markup | Use `blazor-unit-testing` |
| The task tests a browser journey | Use `blazor-ui-testing` |
| The user requests execution only | Use `run-tests` |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Production behavior | Yes | Agent identifies the public method, component service, or endpoint under test. |
| Test project | Yes | Agent identifies the xUnit project and its target framework. |
| Existing conventions | No | Agent reads nearby tests, fixtures, traits, and assertion libraries. |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent reads the production path and neighboring xUnit tests. | Inspect source, project file, and sibling tests. | Naming, fixture, and runner conventions are explicit. |
| 2 | Agent maps direct dependencies and selects the smallest isolation boundary. | Review constructor and collaborator setup. | Tests avoid live infrastructure unless the test is integration-scoped. |
| 3 | Agent writes happy-path, edge, and failure cases that prove observable behavior. | Review test cases and assertions. | Each requested behavior has a meaningful assertion. |
| 4 | Agent uses xUnit fixtures, `Theory` data, traits, and async assertions only when they clarify the test. | Inspect test structure. | Shared setup stays bounded and cases remain readable. |
| 5 | Agent runs the smallest existing build and test commands. | Execute the touched test project. | Build succeeds and targeted tests pass. |

## Test Design Rules

| Concern | Pattern | Pass |
|---|---|---|
| Naming | Use `{ProductionType}Tests` and `Method_Scenario_Result`. | Test names communicate behavior. |
| Data variation | Use `[Theory]` for equivalent cases with explicit `[InlineData]` or class data. | Data describes the scenario without hidden fixture state. |
| Exceptions | Use `Assert.Throws` or `Assert.ThrowsAsync` with the expected exception type and relevant state. | Failure behavior is explicit. |
| Collaborators | Mock external boundaries and keep pure domain objects real. | Tests isolate only unstable dependencies. |
| Async behavior | Await production calls and use async test methods. | No blocking `.Result` or `.Wait()` calls exist. |

## Verification Checklist

- [ ] Test project uses xUnit packages and the repository test runner.
- [ ] Tests cover the requested success, edge, and failure behavior.
- [ ] Assertions prove outcomes, state, or collaborator inputs.
- [ ] Tests avoid timing, network, database, and filesystem coupling unless required.
- [ ] The touched project builds and targeted tests pass.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| One test contains many unrelated scenarios | Split cases by behavior and use `[Theory]` only for equivalent data. |
| Assertions inspect private implementation details | Assert public outcomes and observable collaborator calls. |
| Fixture state leaks between tests | Use isolated fixture state or immutable test data. |
| Async tests block the runner | Await all asynchronous operations. |
