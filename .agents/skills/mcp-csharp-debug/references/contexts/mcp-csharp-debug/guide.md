---
metadata-version: "1.0.0"
title: "C# MCP Server Debugging"
description: "Preserve scoped source guidance for mcp-csharp-debug."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# C# MCP Server Debugging

Agent debugs MCP servers by proving startup, configuration, protocol visibility, and tool invocation one layer at a time.

## When to Use

| Condition | Agent Action |

|---|---|

| Existing C# MCP server fails to start or register tools | Use this skill |

| IDE or inspector setup needs verification | Use this skill |

| Server creation work is still in progress | Pair with `mcp-csharp-create` only for missing scaffolding |

| Automated test creation is the main task | Use `mcp-csharp-test` |

## Workflow

| Step | Agent Action | Test | Pass |

|---|---|---|---|

| 1. Prove startup | Agent runs the server locally with the intended transport. | Run `dotnet run` in scope. | Server starts without build or host failure. |

| 2. Verify client config | Agent checks `mcp.json`, launch settings, or HTTP endpoint configuration. Agent reads `references/ide-config.md` for VS Code and Visual Studio configuration patterns. | Inspect local MCP client configuration in scope. | Configuration points to the correct command or URL. |
| 3. Inspect protocol surface | Agent uses MCP Inspector or equivalent configured client to list tools, prompts, and resources. Agent reads `references/mcp-inspector.md` for the inspector workflow and connection modes. | Run existing inspection flow in scope. | Expected MCP surface is discoverable. |

| 4. Reproduce one failing call | Agent invokes one representative failing tool or prompt path. | Run the failing scenario in scope. | Failure reproduces deterministically or success proves the fix. |

| 5. Fix diagnostics path | Agent aligns stderr logging, breakpoints, and HTTP diagnostics with the chosen transport. Agent reads `references/ide-config.md` for debugger and logging configuration details. | Inspect logging and debugger configuration. | Logs reveal server state without corrupting protocol output. |

| 6. Re-verify end to end | Agent reruns startup and the representative call. | Repeat build, run, and inspector checks. | Startup, discovery, and one representative call succeed. |

## Failure Matrix

| Symptom | Agent Checks | Likely Fix |

|---|---|---|

| Stdio server hangs or emits invalid protocol output | Stdout logging and host startup noise | Move logs to stderr and keep stdout protocol-only |

| Tool is missing from discovery | Missing attributes or missing server registration | Add MCP attributes and assembly registration |

| HTTP endpoint returns 404 or handshake fails | Route mapping and base URL | Add or correct `MapMcp()` and client URL |

| Tool call fails at runtime | Dependency injection, serialization, or transport input shape | Fix service registration or request contract |

## Verification Matrix

| Test | Run | Pass |

|---|---|---|

| Build verification | `dotnet build` for the touched project | Zero build errors. |

| Discovery verification | Run MCP Inspector or existing client discovery flow in scope. | Expected tools, prompts, or resources are listed. |

| Repro verification | Invoke one representative MCP operation in scope. | Operation succeeds or reproduces the target defect deterministically. |

## Reference Files

| File | Covers | Agent Reads When |
|---|---|---|
| `references/ide-config.md` | VS Code and Visual Studio MCP registration, launch profiles, attach flows, and logging setup. | Agent reads this file when validating local client configuration, debugger setup, or logging behavior. |
| `references/mcp-inspector.md` | MCP Inspector installation, connection steps, tool testing, and protocol inspection. | Agent reads this file when the debugging workflow uses interactive MCP discovery or one-call reproduction. |

## Guardrails

- Agent debugs one failing layer at a time.

- Agent keeps stdio protocol output free of logging noise.

- Agent preserves existing MCP surface names unless the task explicitly changes the contract.
