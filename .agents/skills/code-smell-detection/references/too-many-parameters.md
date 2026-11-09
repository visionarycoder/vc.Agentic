---
title: Too Many Parameters Smell Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: code-smell-detection
---

# Too Many Parameters Smell

## Description

Method or constructor accepts so many inputs that the call site loses clarity.

## Detection Signals

- Method >5 parameters
- Parameters of the same type appear in long runs
- Optional booleans and flags shape multiple behaviors
- Call sites need named arguments to stay readable

## Why This Is Problematic

- Callers swap argument order easily
- Tests need verbose setup
- Signature changes ripple through many callers
- Hidden concepts stay split across primitives

## Remediation

Use **Introduce Parameter Object** or **Builder**.

```csharp
// ❌ BEFORE: Long parameter list hides one request concept
public sealed class MeetingService
{
    public Task ScheduleAsync(
        string title,
        DateOnly date,
        TimeOnly startTime,
        TimeOnly endTime,
        string organizerEmail,
        string roomName,
        bool sendInvites,
        bool recordMeeting)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(title);
        ArgumentException.ThrowIfNullOrWhiteSpace(organizerEmail);
        ArgumentException.ThrowIfNullOrWhiteSpace(roomName);
        return Task.CompletedTask;
    }
}

// ✅ AFTER: Parameter object names the request
public sealed record MeetingScheduleRequest(
    string Title,
    DateOnly Date,
    TimeOnly StartTime,
    TimeOnly EndTime,
    string OrganizerEmail,
    string RoomName,
    bool SendInvites,
    bool RecordMeeting);

public sealed class MeetingService
{
    public Task ScheduleAsync(MeetingScheduleRequest request)
    {
        ArgumentNullException.ThrowIfNull(request);
        ArgumentException.ThrowIfNullOrWhiteSpace(request.Title);
        ArgumentException.ThrowIfNullOrWhiteSpace(request.OrganizerEmail);
        ArgumentException.ThrowIfNullOrWhiteSpace(request.RoomName);
        return Task.CompletedTask;
    }
}
```

## Verification

Test: Count parameters per signature and inspect call sites before and after refactoring.
Pass: Long parameter list becomes one named request object or builder. Call sites read clearly. Tests pass.

## Reference

[Long Parameter List - Refactoring Guru](https://refactoring.guru/smells/long-parameter-list)
