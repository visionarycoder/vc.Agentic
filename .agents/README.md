---
metadata-version: "1.0.0"
title: "Shared skill catalog"
description: "Route shared agent tasks to focused skills."
document-type: "index"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Shared skill catalog

| Skill | Inputs | Output |
| --- | --- | --- |
| [prepare-component-initialization](skills/prepare-component-initialization/SKILL.md) | Assigned capability, approved vault type, target repository, accepted design, actual base API | Interface and implementation skeleton with explicit omissions |
| [prepare-task-handoff](skills/prepare-task-handoff/SKILL.md) | Assignment, changed artifacts, verification evidence, unresolved items | Traceable handoff for the designated recipient |

These skills assist assigned work. They do not authenticate actors, confer acceptance authority, or supply an independent reviewer. They are repository-local resources; discovery and installation depend on the client.
