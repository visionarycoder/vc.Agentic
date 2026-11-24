---
name: "quartz-job-authoring"
description: "Author Quartz.NET jobs with explicit DI, execution context, cancellation, and failure handling."
metadata:
  metadata-version: "1.0.0"
  title: "Quartz.NET Job Authoring"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# Quartz.NET Job Authoring

Agent authors Quartz jobs that stay thin, cancellable, and observable.

## When to Use

Use when creating an `IJob`, adding DI-backed scheduled processing, passing runtime data through Quartz context, or defining retry or failure behavior. Do not use for event-driven work, Azure Functions or WebJobs, or continuous hosted services.

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Job responsibility | Yes | One clear business outcome |
| Dependencies | Yes | Services, repositories, clients, and options |
| Job data contract | No | Keys and expected types in `JobDataMap` |
| Failure policy | Yes | Retry now, fail, or log-and-stop |
| Runtime duration | No | Use with cancellation and checkpoint design |

## Required Workflow

Agent performs these steps:
1. Agent implements a stateless `IJob` that delegates domain work to injected services.
2. Agent reads runtime parameters from `context.MergedJobDataMap` with explicit keys.
3. Agent passes `context.CancellationToken` through every async dependency.
4. Agent maps transient and terminal failures to explicit Quartz behavior.
5. Agent verifies manual triggering, cancellation, and failure logging.

Test: Agent runs `dotnet build [project].csproj` and existing job tests or targeted execution tests.
Pass: Agent observes zero compile errors. Agent confirms one successful execution path and one failure path in the changed scope.

## Failure and Duration

- Transient failure: `JobExecutionException(ex, refireImmediately: true)` only for idempotent or guarded work.
- Terminal failure: `JobExecutionException(ex, refireImmediately: false)`, paired with alerting or operator review.
- Runtime parameters: `UsingJobData(...)` with typed reads from `context.MergedJobDataMap`.
- Long work: pair with a checkpoint strategy and route to `long-running-job-patterns` when duration grows.

## Verification Matrix

| Test | Run | Pass |
|---|---|---|
| Compile verification | `dotnet build [project].csproj` | Zero compile errors |
| Unit verification | Existing MSTest project for the job | Happy-path test passes |
| Failure verification | Existing MSTest project with mocked dependency failure | Failure path logs and throws expected Quartz exception |
| Trigger verification | Existing app path or targeted scheduler test | Job executes from its trigger or manual `TriggerJob` call |
