---
metadata-version: "1.0.0"
title: "C# MCP Server Testing"
description: "Preserve scoped source guidance for mcp-csharp-test."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# C# MCP Server Testing

Agent verifies MCP servers at the method, protocol, and end-to-end interaction layers.

## When to Use

| Condition | Agent Action |

|---|---|

| Tool or prompt behavior changes | Use this skill |

| Server transport or DI behavior changes | Use this skill |

| Work only debugs an interactive issue | Use `mcp-csharp-debug` |

| Work only packages a server | Use `mcp-csharp-publish` |

## Test Matrix

| Layer | Agent Verifies | Typical Scope | Pass |

|---|---|---|---|

| Unit | Tool method logic and validation | Individual tool classes | Assertions cover happy, edge, and failure paths. |

| Integration | Server registration and MCP client interaction | In-memory or local server flow | Client discovers and invokes intended MCP surface. |

| HTTP integration | HTTP host route and serialization | WebApplicationFactory or local host flow | MCP endpoint responds on the expected route. |

| Evaluation | Prompt or tool quality on representative scenarios | Curated scenario set | Outputs meet the acceptance rubric for the changed scope. |

## Workflow

| Step | Agent Action | Test | Pass |

|---|---|---|---|

| 1. Create or locate test project | Agent uses the existing test project pattern or adds one that matches repository conventions. | Inspect touched test project files. | Test project aligns with repository naming and package conventions. |

| 2. Add unit tests | Agent writes tests for tool logic, validation, cancellation, and dependency behavior. Agent reads `references/test-patterns.md` for test helpers and unit-level code patterns. | Run existing test command with focused filter when available. | Unit tests pass and cover happy, edge, and failure paths. |
| 3. Add integration tests | Agent verifies discovery and invocation by using the MCP client path already used by the project. Agent reads `references/test-patterns.md` for in-memory and HTTP integration test patterns. | Run existing integration tests in scope. | Expected MCP surface is discoverable and callable. |
| 4. Add transport checks | Agent verifies stdio protocol cleanliness or HTTP route behavior when transport code changes. Agent reads `references/test-patterns.md` for HTTP endpoint and server harness patterns. | Run existing transport-specific tests in scope. | Transport path behaves as configured. |
| 5. Verify full scope | Agent runs the smallest existing test command that covers the changed behavior. Agent reads `references/evaluations.md` when the changed scope includes prompt or tool-quality evaluation scenarios. | Run existing build and test commands in scope. | Zero build errors and zero failing tests. |

## Verification Matrix

| Test | Run | Pass |

|---|---|---|

| Unit verification | Run existing unit test command or filtered `dotnet test` in scope. | Zero failing unit tests. |

| Integration verification | Run existing MCP integration tests in scope. | Discovery and invocation succeed for changed MCP surface. |

| Build verification | Run existing build command for touched projects. | Zero build errors. |

## Reference Files

| File | Covers | Agent Reads When |
|---|---|---|
| `references/evaluations.md` | XML evaluation sets, deterministic question design, and multi-tool answer verification. | Agent reads this file when the testing scope includes prompt or tool-quality evaluations beyond unit and integration assertions. |
| `references/test-patterns.md` | Test doubles, in-memory client/server harnesses, and HTTP integration testing patterns. | Agent reads this file when writing or extending unit, integration, or transport-focused MCP tests. |

## Guardrails

- Agent keeps test focus on server behavior, not client product behavior.

- Agent verifies cancellation and failure paths when exposed tools perform async work.

- Agent uses the smallest existing test command that covers the changed behavior.
