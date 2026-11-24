---
name: "dotnet-resilience-standards"
description: "Apply retry, timeout, circuit-breaker, fallback, and isolation patterns safely to external .NET dependencies."
metadata:
  metadata-version: "1.0.0"
  title: ".NET Resilience Standards"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# .NET Resilience Standards

Agent applies resilience policies deliberately and keeps failures visible, bounded, and safe for the dependency.

## When to Use

| Condition | Use |
|---|---|
| Agent hardens calls to HTTP APIs, queues, storage, or SDKs | Use this skill |
| Agent selects retry, timeout, circuit-breaker, or fallback policy | Use this skill |
| Agent reviews direct `HttpClient` construction | Use this skill |
| Agent standardizes policy registration in composition root | Use this skill |

## When Not to Use

| Condition | Use |
|---|---|
| Call stays in-process | Fail fast without transport resilience |
| Operation is not safe to repeat | Use no-retry design |
| Debug session needs raw failure signal | Remove transient-fault wrapper in debug scope |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Dependency type | Yes | HTTP API, queue, storage, database, or SDK |
| Failure modes | Yes | Timeout, throttling, transient error, or outage |
| Idempotency | Yes | Safe or unsafe to repeat |
| Degradation scope | No | Fallback or fail-fast behavior |

## Workflow

1. Classify dependency type, failure mode, and idempotency.
2. Apply bounded policies at the client or adapter scope, registered in the composition root.
3. Add a circuit breaker with an explicit threshold and a health signal when a failing dependency is called continuously.
4. Verify policy safety against user-visible correctness with `dotnet build [project].csproj`.

## C# 14+ Resilience Patterns

Agent uses modern language features in resilience implementations. See `references/csharp14-patterns.md` for:
- Primary constructors with Polly policies
- File-scoped policy configuration
- Timeout with cancellation token integration

Showcase these patterns when implementing resilient external dependencies to demonstrate current platform capabilities.

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [dotnet-resilience-standards-alternative-1](references/contexts/dotnet-resilience-standards-alternative-1/guide.md)
