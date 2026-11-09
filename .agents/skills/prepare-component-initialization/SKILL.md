---
name: "prepare-component-initialization"
description: "Prepare component interface and implementation skeletons from an assigned design using the shared initialization samples."
metadata:
  metadata-version: "1.0.0"
  title: "Prepare component initialization"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Prepare component initialization

Read the target repository instructions, current assignment, and accepted detailed design. Identify the capability, approved Manager/Engine/Access classification, namespaces, contract operations, and actual ComponentBase signature. Do not infer a component boundary from a suffix alone.

Read the [initialization template](../../../templates/components/component-initialization.md) and [samples](../../../samples/components/README.md). Preserve the requested ILoggerFactory constructor; adapt it to the verified base API. Keep each interface and class in its own file. Add only operations specified by the accepted contract.

If the assignment requests a sketch, provide a clearly labeled sketch. If required construction inputs or authority are absent, identify what is missing and prepare only the authorized draft. Route design refinements to the Application Architect before construction under them.

Do not add direct caller-to-target DI registrations. Use the approved proxy chain and existing Ifx mechanisms when composition is in scope. Do not create a local replacement for missing Ifx infrastructure.

Return changed artifacts, placeholder substitutions, verification performed, and remaining omissions. Do not claim that a skeleton is an accepted component or a completed lifecycle phase.
