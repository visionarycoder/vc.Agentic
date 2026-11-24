---
name: "dotnet-telemetry-standards"
description: "Govern OpenTelemetry setup, correlation, metrics, and safe observability patterns across .NET services."
metadata:
  metadata-version: "1.0.0"
  title: ".NET Telemetry Standards"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# .NET Telemetry Standards

Agent keeps traces, metrics, and correlation stable across service calls. Agent keeps telemetry useful without leaking sensitive data or generating incompatible names.

## When to Use

| Condition | Use |
|---|---|
| Agent configures OpenTelemetry in web app, function, worker, or library code | Use this skill |
| Agent adds spans, metrics, or correlation-aware logs | Use this skill |
| Agent reviews telemetry completeness, naming, or privacy | Use this skill |
| Agent standardizes reusable observability helpers | Use this skill |

## When Not to Use

| Condition | Use |
|---|---|
| Task is logging-only | Route to logging skill |
| Task is temporary local diagnostics | Delete temporary instrumentation before completion |
| Task is one-time profiling without persistent instrumentation | Route to performance or trace collection skill |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Service type | Yes | Web API, function, worker, library, or shared component |
| Export target | Yes | OTLP, Application Insights, console, or approved exporter |
| Service identity | Yes | Stable service name, version, and component name |
| Custom telemetry need | No | Domain metric, span tag, redaction rule, or correlation key |

## Workflow

1. Select service identity (name, version, component) and export target before writing instrumentation.
2. Reuse one stable `ActivitySource` and `Meter` per component; configure OpenTelemetry centrally with `AddOpenTelemetry()`.
3. Emit metrics (counters and histograms for count, duration, error rate) in addition to traces and logs; logs do not replace metrics.
4. Keep correlation intact across calls, queues, and logs: pass current activity context and scope data, and use shared trace and request keys rather than ad hoc keys.
5. Keep tags and labels low-cardinality; omit, hash, or sanitize sensitive values such as user identifiers.
6. Verify with `dotnet build [project].csproj`.

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [dotnet-telemetry-standards-alternative-1](references/contexts/dotnet-telemetry-standards-alternative-1/guide.md)
