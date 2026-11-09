---
name: "skill-selection"
description: "Select the smallest relevant skill set for an assigned task using actual repository guidance and available capabilities."
metadata:
  metadata-version: "1.0.0"
  title: "Skill selection"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "core"
---

# Skill selection

Use when the user asks which skill to use or when a task needs routing across multiple capabilities. Routine questions and simple edits do not require a skill ceremony.

1. Read the task and applicable repository instructions. Identify the requested result, scope, and existing constraints.
2. Use catalog names and descriptions to choose the smallest matching set. Read explicitly requested skills and the relevant entrypoints before applying them.
3. Load implementation references only when the task needs them. Do not read every process skill or add unrelated interviews, planning, or approval steps.
4. Map a skill's required capability to the actual host tools. Do not invent a Skill tool, provider namespace, background-agent API, or connector. If a required capability is unavailable, use an authorized equivalent or report the limitation.
5. Honor user intent, target-project rules, and actual permissions. Skill selection does not assign roles, authorize delegation, or approve publication.

The [collection catalog](../../collections.md) distinguishes the recommended core from optional stacks and specialist domains. These are selection aids, not automatic installation or activation controls.
