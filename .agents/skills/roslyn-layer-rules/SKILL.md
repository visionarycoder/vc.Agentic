---
name: "roslyn-layer-rules"
description: "Define the layer-call diagnostics, platform limits, and Gate 2 design needs when the developer layer is roslyn."
metadata:
  metadata-version: "1.0.0"
  title: "Roslyn Layer Rules"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Roslyn Layer Rules

Load this skill when the `developer` agent works in layer `roslyn` (write scope `src/ifx/**`). Also load `roslyn-analyzer-authoring`, `roslyn-codefix-authoring`, and `roslyn-source-generator-authoring`.

The Roslyn developer builds the guardrails: analyzers that turn the layer call rules and manager logic limits into compile errors, plus code fixes and generators the team needs.

## Platform

- Target `netstandard2.0`.
- Set `<LangVersion>14.0</LangVersion>` and reference `PolySharp` with `PrivateAssets="all"`. Use C# 14 features.
- Do not use runtime-dependent features: default interface members, static abstract interface members, generic math, or `Span<T>` collection-expression targets.
- Verify that every BCL API exists in `netstandard2.0`.
- Never raise the target framework.

## Rules To Enforce (severity: error)

| Rule | Check |
|---|---|
| Client calls Engine or Access | Report |
| Client calls Client | Report |
| Engine calls Engine, Manager, or Client | Report |
| Engine calls Access without a design approval marker | Report |
| Access calls anything but its own resource | Report |
| Any upward call | Report |
| Manager calls Manager synchronously | Report |
| Manager holds business logic beyond `if`/`else` and loops, when a proxy project handles mapping | Report |

Utilities (logging, configuration, telemetry) are callable from any layer.

## Design Needs

- The Engine-to-Access exception needs a machine-readable marker, such as an attribute on the approved call or a design-approved allowlist. Submit the marker design to `application-architect` at Gate 2.
- Proxy project detection needs a project naming convention or project property. Submit the detection design to `application-architect` at Gate 2.
- Report diagnostics with clear messages that name the violated rule and a fix.
