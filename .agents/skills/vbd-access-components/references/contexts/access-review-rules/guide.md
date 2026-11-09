---
metadata-version: "1.0.0"
title: "Access Review Rules"
description: "Preserve scoped source guidance for vbd-access-components."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Access Review Rules

`code-critic` applies this checklist to code in `src/component/access/**`.

| Check | Test | Pass criteria |
|---|---|---|
| Role | Read the public surface. | Code encapsulates access to one resource or external system and holds no business rules. |
| Calls | Search for references to other components. | No call to an Engine, a Manager, a Client, or another Access component; Utilities only. |
| Encapsulation | Read the public contract. | Connection strings, schemas, vendor types, and wire formats never leak. |
| Contract | Compare to the approved proposal. | Public interface and DTOs match the proposal and detailed design. |
| Atomic operations | Read each operation. | Each operation is a business-neutral verb on the resource, not a multi-step workflow. |
| Resource handling | Read lifetimes and async paths. | Connections, streams, and handles are disposed; cancellation tokens are honored; retries and timeouts follow the design. |
| Secrets | Search code and configuration. | No credentials; managed identity or a vault reference only. |
| Standards | Compare to `.agents/csharp-coding-standards.md`. | Code conforms. |

Rejection message names the root cause and at least two alternatives with tradeoffs.
