---
name: "skill-behavior-testing"
description: "Evaluate whether skill instructions improve representative task outcomes without overreach, missing prerequisites, or dependence on one agent host."
metadata:
  metadata-version: "1.0.0"
  title: "Skill behavior testing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Skill behavior testing

Use to test an existing skill's behavior. Use skill-authoring to create or revise the skill itself.

1. Define representative user tasks, required inputs, expected outputs, and boundaries. Include normal use, ambiguous input, missing capabilities, and an out-of-scope request.
2. Compare behavior with and without the relevant instructions using an available authorized evaluation method. Separate evaluator criteria from the instructions under test.
3. Check task completion, correctness, unnecessary actions, tool assumptions, authority claims, and whether failures are reported truthfully.
4. Record actual observations and explain how they relate to the skill. Do not call an imagined agent response an executed evaluation.
5. Revise the smallest instruction responsible for an observed problem, then rerun affected cases. Keep regression cases that represent distinct behavior.
6. Report tested cases, host/capability limits, remaining uncertainty, and recommendations. Subagents, paid services, or a provider-specific evaluation harness are optional and require their existing authorization.
