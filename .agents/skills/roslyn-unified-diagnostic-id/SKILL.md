---
name: "roslyn-unified-diagnostic-id"
description: "Allocate and maintain diagnostic IDs consistently across Roslyn analyzers, code fixes, tests, and documentation."
metadata:
  metadata-version: "1.0.0"
  title: "Roslyn diagnostic IDs"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# Roslyn diagnostic IDs

Use for new diagnostic allocation, category/range changes, constant extraction, and analyzer/code-fix alignment.

1. Read the target repository's current diagnostic registry, category/range rules, and compatibility requirements. Use the actual registry path and namespace; do not assume an older vc.Analyzers layout.
2. Check the entire registry for collisions and reserve an unused ID within its owning category. Preserve IDs already exposed to consumers unless a migration is explicitly accepted.
3. Define one semantically named constant for the ID. Reuse it in DiagnosticDescriptor declarations, CodeFixProvider.FixableDiagnosticIds, tests, and relevant documentation. Remove duplicated literal definitions.
4. Keep descriptor severity, message, category, help link, and supported fix behavior aligned with the accepted rule. An ID cleanup does not authorize changing diagnostic behavior.
5. Verify uniqueness, allocation format, expected diagnostics, fix registration, and supported language/runtime configurations using the repository's existing checks. Do not change the SDK or suppress diagnostics to pass.
6. Report allocated IDs, registry ownership, affected analyzers/fixes/tests, compatibility impact, and verification results.

Diagnostic registry and reference documents belong to the consuming project. If absent, identify the missing contract rather than inventing a globally authoritative allocation scheme.
