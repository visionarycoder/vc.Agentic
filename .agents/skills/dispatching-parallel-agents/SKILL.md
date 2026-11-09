---
name: "dispatching-parallel-agents"
description: "Coordinate authorized parallel work on independent tasks when the host supports delegation."
metadata:
  metadata-version: "1.0.0"
  title: "Parallel work coordination"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Parallel work coordination

Use when the assignment contains independent tasks and delegation is authorized by the user or applicable workflow. If the host lacks delegation, perform the tasks sequentially.

1. Identify task dependencies, shared files/state, and acceptance checks. Keep tightly coupled tasks together.
2. Allocate disjoint scopes with a concrete result, relevant context, constraints, and verification requirements. Use the host's available delegation mechanism; do not assume a provider-specific API or required model.
3. Choose inherited or isolated context according to the task. Give each worker enough evidence to understand the assignment without unrelated history.
4. Coordinate shared edits, builds, and integration explicitly. Parallel execution does not permit overlapping writes without coordination or bypass repository approval rules.
5. Review returned evidence and integrate changes under the existing assignment. Verify combined behavior rather than relying only on separate worker reports.
6. Report results, unresolved dependencies, and actual checks. Delegation itself is neither independent acceptance nor authority to commit or deploy.
