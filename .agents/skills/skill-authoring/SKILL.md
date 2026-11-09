---
name: "skill-authoring"
description: "Create or revise a focused agent-neutral skill with accurate discovery metadata, useful instructions, and required supporting resources."
metadata:
  metadata-version: "1.0.0"
  title: "Skill authoring"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "core"
---

# Skill authoring

1. Identify the repeated task, intended users, trigger conditions, inputs, expected output, and important exclusions. Reuse or extend a matching skill before creating another entrypoint.
2. Choose a clear kebab-case name. Put the skill in the target library's actual skill directory and follow its documented frontmatter profile.
3. Keep `name` and `description` accurate for discovery. Put extended maintenance fields under `metadata`. Do not add provider-specific UI or invocation-policy files.
4. Write a short self-contained workflow. Put substantial conditional detail in supporting references; add scripts or assets only when the task needs them.
5. Use actual host capabilities without hard-coding a tool API, model, skill-invocation namespace, or agent provider. Document required external capabilities and an authorized fallback where feasible.
6. Treat project layout, framework versions, ownership, approval, and publication authority as consuming-project inputs. Do not turn one project's preferences into universal rules.
7. Validate metadata, names, links, resources, and meaningful behavior. Test new executable helpers with local fixtures or mocks appropriate to their effect.
8. Update the catalog and inventory. For this repository use the documented maintenance command rather than maintaining parallel registries.
