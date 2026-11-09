---
name: "roslyn-intake-router"
description: "Route Roslyn and Ifx requests to the minimum correct authoring skill by separating analyzers, code fixes, and source generators for C# 8-safe src/ifx work."
metadata:
  metadata-version: "1.0.0"
  title: "Roslyn Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Roslyn Intake Router

Agent routes Roslyn work to one primary authoring skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for analyzer, code fix, or source generator work and the exact authoring type is unclear | Use this skill |
| Request touches `src/ifx` Roslyn authoring | Use this skill |
| User asks which Roslyn skill owns the work | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is already narrowed to analyzer, code fix, or generator authoring | Use that specific Roslyn skill |
| Request is normal application code and not Roslyn tooling | Use the non-Roslyn suite that matches the target technology |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad Roslyn routing belongs here |
| Authoring split | Choose analyzer, code fix, or generator first based on the requested output |
| Ifx constraint | Keep Roslyn routing specific to `src/ifx` C# 8-safe authoring patterns |
| Specialist loading | Do not stack Roslyn authoring types unless the request explicitly requires more than one |

## Verification

- [ ] Agent chose one primary Roslyn skill
- [ ] Agent kept `src/ifx` routing specific to analyzer, codefix, or generator scope
- [ ] Agent avoided mixing Roslyn authoring types unless the request explicitly required more than one

## Routing Table

| Intent | Primary skill |
|---|---|
| Diagnostic rule authoring | `roslyn-analyzer-authoring` |
| Automated source edit or fix provider | `roslyn-codefix-authoring` |
| Generated code from compile-time inputs | `roslyn-source-generator-authoring` |
