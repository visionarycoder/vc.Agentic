---
name: "quartz-calendar-schedules"
description: "Build Quartz.NET Schedule definitions that respect holidays, payroll calendars, business-day shifts, and organization-specific date rules."
metadata:
  metadata-version: "1.0.0"
  title: "Quartz.NET Calendar-Based Schedules"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# Quartz.NET Calendar-Based Schedules

Agent defines Quartz Schedule behavior that depends on holidays, business days, payroll dates, or fiscal rules.

## When to Use

| Condition | Use |
|---|---|
| Agent excludes holidays or shutdown dates from a Schedule | Use this skill |
| Agent shifts a Schedule date forward or backward on non-business days | Use this skill |
| Agent models payroll, month-end, quarter-end, or fiscal-date recurrence | Use this skill |
| Agent combines Quartz triggers with reusable calendar rules | Use this skill |

## When Not to Use

| Condition | Use |
|---|---|
| Recurrence depends only on fixed clock timing | Use `quartz-scheduling-patterns` |
| Work runs once with no recurrence | Trigger the job directly |
| Work starts from external events | Use queue or event-driven patterns |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Schedule rule set | Yes | Holidays, business days, payroll dates, fiscal periods, or blackout dates |
| Base trigger | Yes | Cron, daily interval, or calendar interval trigger |
| Shift policy | Yes | Skip, move earlier, or move later |
| Business-day definition | Yes | Weekend set, local holidays, and exceptions |
| Validation dates | No | Boundary dates near weekends, month end, and year end |

## Required Workflow

Agent performs these steps:
1. Agent models the Schedule rule set before writing trigger code.
2. Agent selects the Quartz calendar type from the rule table.
3. Agent keeps reusable Schedule rules in shared calendar registration.
4. Agent defines one explicit shift policy for excluded dates.
5. Agent validates representative boundary dates before deployment.

Test: Agent runs `dotnet build [project].csproj` and previews representative trigger fire times against the configured calendar rules.
Pass: Agent observes zero compile errors. Agent confirms that previewed fire times match the documented Schedule rules and shift policy.

## Calendar Rule Table

| Need | Preferred pattern |
|---|---|
| Domain-specific included dates (payroll, fiscal) | Custom `BaseCalendar` implementation, or a date calculator plus trigger |
| Quarter-end with move-earlier rule | Trigger plus shift calculator so the shift policy is explicit and testable |

Standard calendars (`HolidayCalendar` for ad hoc dates, `AnnualCalendar` for fixed annual holidays, `WeeklyCalendar` for weekends) are chained and registered once, then referenced by triggers. Keep business-day logic out of cron expressions.

Use `Schedule` consistently for domain concepts. Test weekend adjacency, month end, quarter end, and year end, with each shift policy (skip, move earlier, move later) defined in one place.
