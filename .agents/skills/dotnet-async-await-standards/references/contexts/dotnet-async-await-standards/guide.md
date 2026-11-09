---
metadata-version: "1.0.0"
title: ".NET Async Await Standards"
description: "Preserve scoped source guidance for dotnet-async-await-standards."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# .NET Async Await Standards

Agent keeps I/O call chains async end-to-end. Agent avoids blocking waits and accidental task lifetime defects.

## When to Use

| Condition | Use |
|---|---|
| Agent adds database, HTTP, file, stream, or queue calls | Use this skill |
| Agent refactors sync I/O into async code | Use this skill |
| Agent fixes dropped cancellation token flow or blocking waits | Use this skill |
| Agent reviews library await patterns or hot-path task cost | Use this skill |

## When Not to Use

| Condition | Use |
|---|---|
| Work is CPU-bound and stays local | Use synchronous code or explicit parallelism |
| Code is fire-and-forget with no owned lifetime | Define owned lifetime before using async |
| API is truly synchronous and cannot route to async I/O | Keep the API synchronous |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Work type | Yes | I/O-bound or CPU-bound |
| Cancellation source | Yes | Request token, job token, or explicit token source |
| Code scope | Yes | App code, library code, Roslyn tooling, or UI handler |
| Measurement data | No | Use when `ValueTask<T>` or pooling is under consideration |

## Workflow

Agent follows these steps:

1. Agent classifies work type before changing method shape.
2. Agent routes I/O call chains to async APIs from entry point to leaf call.
3. Agent applies the rule matrix to awaits, cancellation flow, and task return types.
4. Agent verifies correctness, cancellation, and measurement data before using advanced optimizations.

Test: Run `dotnet build [project].csproj`.
Pass: Zero compile errors. Zero sync-over-async defects in changed scope.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| `Task.Run` wraps sync I/O | Route to true async API or keep sync code |
| Async leaf call keeps sync caller | Write the caller chain to async too |
| `ConfigureAwait(false)` appears everywhere | Limit it to reusable library scope |
| `ValueTask<T>` appears without evidence | Use `Task<T>` |

## Rule Matrix

| Rule | Agent verifies | Detection Pattern | Fix |
|---|---|---|---|
| ASYNC-001 | I/O calls use async APIs | Sync database, HTTP, file, or stream calls in request paths | Route to true async APIs |
| ASYNC-002 | Callers do not block on tasks | `.Result`, `.Wait()`, `GetAwaiter().GetResult()` | Await task directly |
| ASYNC-003 | Async methods use async suffix | `Task` or `ValueTask` method without `Async` | Rename method and callers |
| ASYNC-004 | Cancellation token flows through every owned async hop | Token accepted but not forwarded | Pass token to nested async calls |
| ASYNC-005 | `ConfigureAwait(false)` appears only in library-style scope | Blind use in app entry code | Keep default await in app code. Use `ConfigureAwait(false)` in reusable libraries |
| ASYNC-006 | `ValueTask<T>` appears only with measurement data | Premature `ValueTask<T>` use | Use `Task<T>` by default |
| ASYNC-007 | `async void` appears only on event handlers | Fire-and-forget methods returning `void` | Return `Task` |
| ASYNC-008 | Background task lifetime stays observable | Started task has no owner, logging, or exception path | Route work through owned service or await path |

## Pattern Matrix

| Concern | Use | Avoid |
|---|---|---|
| Method shape | `Task<T>` with token last | Sync wrapper over async call |
| Library await | `await call.ConfigureAwait(false)` | Context capture by habit |
| App await | `await call` | `ConfigureAwait(false)` by habit |
| Hot path | Measurement before advanced optimization | Speculative `ValueTask<T>` or pooling |

## Verification Matrix

| Test | Run | Pass |
|---|---|---|
| Compile verification | `dotnet build [project].csproj` | Zero compile errors |
| Async behavior verification | `dotnet test [test-project].csproj --filter Async` when async tests exist | Zero failing tests |
| Blocking scan verification | Search changed files for `.Result`, `.Wait()`, `GetAwaiter().GetResult()` | Zero matches in changed scope |

## Verification Checklist

Agent verifies:
- [ ] I/O paths stay async end-to-end
- [ ] Blocking waits are absent
- [ ] Async methods use `Async` suffix
- [ ] Cancellation token flow reaches nested async calls
- [ ] `async void` stays limited to event handlers
- [ ] Advanced optimization has measurement data

## Example Defects and Fixes

**ASYNC-002: Blocking on task**
```csharp
// ✗ Anti-pattern: .Result blocks thread
var user = _userService.GetUserAsync(userId).Result;
return Ok(user);

// ✓ Fix: Await the task
var user = await _userService.GetUserAsync(userId);
return Ok(user);
```

**ASYNC-004: Cancellation token not forwarded**
```csharp
// ✗ Anti-pattern: Token accepted but not used
public async Task<User> GetUserAsync(int id, CancellationToken ct) {
    var response = await _httpClient.GetAsync($"https://api.example.com/users/{id}");
    return await response.Content.ReadAsAsync<User>();
}

// ✓ Fix: Pass token to nested async calls
public async Task<User> GetUserAsync(int id, CancellationToken ct) {
    var response = await _httpClient.GetAsync($"https://api.example.com/users/{id}", ct);
    return await response.Content.ReadAsAsync<User>(ct);
}
```

**ASYNC-005: ConfigureAwait(false) in app entry code**
```csharp
// ✗ Anti-pattern: Unnecessary ConfigureAwait in controller
[HttpGet("{id}")]
public async Task<IActionResult> GetUser(int id) {
    var user = await _userService.GetUserAsync(id).ConfigureAwait(false);
    return Ok(user);
}

// ✓ Fix: Keep default await in ASP.NET app code
[HttpGet("{id}")]
public async Task<IActionResult> GetUser(int id) {
    var user = await _userService.GetUserAsync(id);
    return Ok(user);
}
```

**ASYNC-007: async void outside event handlers**
```csharp
// ✗ Anti-pattern: async void fire-and-forget
public async void ProcessUserLogin(int userId) {
    await _auditService.LogLoginAsync(userId);
}

// ✓ Fix: Return Task and let caller await or observe
public async Task ProcessUserLoginAsync(int userId) {
    await _auditService.LogLoginAsync(userId);
}
```
