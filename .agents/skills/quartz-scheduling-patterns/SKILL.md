---
name: "quartz-scheduling-patterns"
description: "Configure Quartz.NET triggers with explicit cron, interval, timezone, and misfire patterns."
metadata:
  metadata-version: "1.0.0"
  title: "Quartz.NET Scheduling Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# Quartz.NET Scheduling Patterns

Agent configures Quartz triggers with explicit timing, timezone, and recovery behavior.

## When to Use

Use for recurring trigger timing, trigger type selection, timezone or misfire review, and fire-time validation. For holiday or business-day rules use `quartz-calendar-schedules`; for immediate or event-driven work, or sub-second precision, do not use Quartz triggers.

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Trigger intent | Yes | Fixed time, fixed interval, business window, or calendar interval |
| Expression or interval | Yes | Cron string or interval settings |
| Timezone | Yes | Explicit production timezone |
| Misfire policy | Yes | Skip, catch up once, or catch up aggressively |
| Validation window | No | Range of future fire times to inspect |

## Required Workflow

Agent performs these steps:
1. Agent selects the trigger type (cron, simple, calendar interval, or daily interval) before writing code.
2. Agent sets an explicit timezone for production triggers.
3. Agent sets a misfire policy that matches business impact.
4. Agent previews future fire times before deployment.
5. Agent documents the intended firing pattern beside the trigger definition.

Test: Agent runs `dotnet build [project].csproj` and evaluates representative future fire times with Quartz trigger preview code.
Pass: Agent observes zero compile errors. Agent confirms that previewed fire times match the intended recurrence.

## Cron Patterns

| Intent | Expression |
|---|---|
| First Monday at 08:00 | `0 0 8 ? * MON#1` |
| Quarter start at 00:00 | `0 0 0 1 1,4,7,10 ?` |

## Misfire Policy

| Concern | Preferred pattern | Avoid |
|---|---|---|
| Missed fire with safe skip | `WithMisfireHandlingInstructionDoNothing()` | Catch-up flood for non-critical work |
| Missed fire with one catch-up run | `WithMisfireHandlingInstructionFireAndProceed()` | Silent loss when one catch-up run matters |
| Flood-tolerant replay | `WithMisfireHandlingInstructionIgnoreMisfires()` | Use on expensive or stateful work |

## Verification Matrix

| Test | Run | Pass |
|---|---|---|
| Compile verification | `dotnet build [project].csproj` | Zero compile errors |
| Cron validation | `CronExpression.IsValidExpression("...")` in existing test or preview code | Expression returns `true` |
| Fire-time preview | `GetFireTimeAfter(...)` loop for representative dates | Preview matches documented intent |
| Timezone verification | Existing scheduler test or trigger preview under configured timezone | Preview reflects the configured timezone |

Bind each trigger to its job with `.ForJob(jobKey)` and give it an explicit unique identity.
