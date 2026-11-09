---
metadata-version: "1.0.0"
title: "Manager Review Rules"
description: "Preserve scoped source guidance for vbd-manager-components."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Manager Review Rules

`code-critic` applies this checklist to code in `src/component/manager/**`.

| Check | Test | Pass criteria |
|---|---|---|
| Control flow only | Read each method. | Code holds `if`/`else` and loops that act on object state. |
| No business logic | Search for rules and transformations. | None in the Manager. |
| Calls | Search for references to other components. | Calls only Engines, Access components, and other Managers; Manager-to-Manager calls are queued or async. |
| Mapping | Locate the mapping code. | With a proxy project, the proxy maps; without one, the Manager maps native and caller DTOs. |
| Design | Compare to the approved proposal. | Types and contracts match the proposal. |
| Standards | Compare to `.agents/csharp-coding-standards.md`. | Code conforms. |

Rejection message names the misplaced logic and the Engine that owns it, with at least two alternatives and tradeoffs.
