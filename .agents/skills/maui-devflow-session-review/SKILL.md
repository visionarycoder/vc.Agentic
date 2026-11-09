---
name: "maui-devflow-session-review"
description: "Create a privacy-safe review of a difficult MauiDevFlow debugging session. Use only when the user explicitly requests a review or accepts an offer after repeated diagnostics, connectivity workarounds, or unclear failures."
metadata:
  metadata-version: "1.0.0"
  title: "MauiDevFlow Session Review"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# MauiDevFlow Session Review

Turn a difficult debugging session into actionable product feedback without exposing application or user data.

## Consent Gate

Never run this review automatically. Offer it only after repeated retries, Android tunnel workarounds, version recovery, direct-port fallback, or an unresolved failure. Continue only after the user opts in.

Use evidence already present in the conversation first. Do not scan additional logs, files, shell history, or screenshots without separate user consent.

## Privacy Scrubbing

Before presenting or filing a report, replace or remove:

- Person and organization names
- Email addresses and account identifiers
- Local paths, usernames, machine names, and device IDs
- Session IDs, agent IDs, application IDs, and broker-specific identifiers
- Private repository, service, and request URLs
- HTTP headers, request or response bodies, and application data
- Screenshots unless the user explicitly approves the exact image
- Credentials, tokens, keys, cookies, and connection strings

Keep product versions, platform category, target framework, tool names, command shapes, and sanitized error text when they are needed to reproduce the issue.

## Review Format

Produce a concise report with:

1. **Summary** - one sentence describing the friction.
2. **Expected behavior** - what should have happened.
3. **Observed behavior** - the first meaningful failure, not every retry.
4. **Environment** - platform category, target framework, CLI/agent versions, and emulator/simulator/device category.
5. **Failure layer** - build integration, broker registration, agent reachability, or UI automation.
6. **Timeline** - minimal sequence of tool calls and state changes.
7. **Workarounds** - what was required and whether it worked.
8. **Improvement idea** - diagnostic, tooling, or documentation change that would have prevented the friction.

Clearly mark uncertain conclusions as hypotheses.

## External Reporting

Do not create an issue, upload logs, or share the report automatically. Show the sanitized draft to the user first. File or send it only after explicit approval, using the destination the user chooses.
