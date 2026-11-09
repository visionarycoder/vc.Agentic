---
metadata-version: "1.0.0"
title: "Engine Review Rules"
description: "Preserve scoped source guidance for vbd-engine-components."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Engine Review Rules

`code-critic` applies this checklist to code in `src/component/engine/**`.

| Check | Test | Pass criteria |
|---|---|---|
| Role | Read the public surface. | Code applies business rules and transformations only. |
| Calls | Search for references to other components. | No call to another Engine, a Manager, or a Client; Access calls only where the design approves. |
| State | Search for fields and handles. | Stateless where the design allows; no resource handles held. |
| Determinism | Search for clock, random, and environment reads. | Same inputs produce the same outputs. |
| Design | Compare to the approved proposal. | Types and contracts match the proposal. |
| Standards | Compare to `.agents/csharp-coding-standards.md`. | Code conforms. |

Rejection message names the root cause and at least two alternatives with tradeoffs.
