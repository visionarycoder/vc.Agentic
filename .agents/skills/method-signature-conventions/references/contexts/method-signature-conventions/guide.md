---
metadata-version: "1.0.0"
title: "Method Signature Conventions"
description: "Preserve scoped source guidance for method-signature-conventions."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Method Signature Conventions

This skill standardizes .NET method signatures for readability, consistency, and async correctness.
This skill preserves compatibility unless the request explicitly allows signature-breaking changes.

## Signature Pattern Table

| Concern | Preferred pattern | Example |
|---|---|---|
| Async naming | Async suffix on asynchronous methods | `Task SaveAsync(...)` |
| Return shape | `Task` or `Task<T>` for async flows | `Task<Result>` |
| Cancellation | `CancellationToken cancellationToken = default` last | `GetAsync(id, cancellationToken)` |
| Parameter order | Required inputs first, optional inputs after, cancellation token last | `FindAsync(id, filter, cancellationToken)` |
| Nullability | Explicit nullable annotations | `string? note` |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Inspect | Agent reviews the current API surface and local conventions. | Signature inventory |
| 2. Align | Agent applies the consistent return, naming, and parameter-order pattern. | Updated signatures |
| 3. Propagate | Agent updates overrides, interface implementations, and call sites in scope. | Consistent callers |
| 4. Validate | Agent builds and runs targeted tests. | Verified API surface |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Async correctness | Review every changed async method. | Async methods use `Task` or `Task<T>` and carry the `Async` suffix when appropriate. |
| Cancellation position | Review signatures that accept a cancellation token. | The cancellation token is last and defaults only when the API surface supports that pattern. |
| Compatibility | Review public contract impact. | No unintended breaking signature change remains. |
| Validation | Run the smallest targeted build or test command. | Changed callers compile and tests pass. |
