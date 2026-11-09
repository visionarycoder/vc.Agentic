---
metadata-version: "1.0.0"
title: "Environment Provider Skill"
description: "Preserve scoped source guidance for env-provider-skill."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Environment Provider Skill

This skill creates testable configuration-access abstractions over environment and configuration sources.
This skill favors typed reads, clear validation, and dependency-injection registration.

## Pattern Table

| Concern | Preferred pattern | Example |
|---|---|---|
| Access surface | Interface-backed provider | `IEnvironmentProvider` |
| Required value | Throw descriptive startup exception | `GetRequiredString("PayrollApi:Url")` |
| Typed parsing | Parse in one location | `GetInt`, `GetBool`, `GetEnum<T>` |
| Tests | In-memory test provider | Dictionary-backed fake |
| Composition | Register via DI | `AddSingleton<IEnvironmentProvider, EnvironmentProvider>()` |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Classify | Agent inventories configuration reads and groups them by required, optional, and typed values. | Access map |
| 2. Define | Agent defines the interface and the smallest useful typed accessor set. | Provider contract |
| 3. Implement | Agent wraps `IConfiguration` or the relevant source with validation and logging. | Production provider |
| 4. Test | Agent adds a fake or stub provider for unit tests. | Test provider |
| 5. Register | Agent wires the provider into DI and updates consumers. | Integrated configuration surface |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Typed access | Review changed consumers. | Consumers read configuration through the provider instead of ad hoc parsing. |
| Validation | Run startup path or targeted tests. | Required keys fail fast with descriptive messages. |
| Testability | Review unit tests or fakes. | Tests supply configuration without mutating process-wide environment state. |
| Registration | Review service registration. | Exactly one canonical provider registration exists per composition root. |
