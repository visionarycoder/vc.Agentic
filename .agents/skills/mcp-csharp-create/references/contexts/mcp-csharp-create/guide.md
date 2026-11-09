---
metadata-version: "1.0.0"
title: "C# MCP Server Creation"
description: "Preserve scoped source guidance for mcp-csharp-create."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# C# MCP Server Creation

Agent creates MCP servers by selecting one transport path, scaffolding one project shape, and wiring discoverable server metadata.

## When to Use

| Condition | Agent Action |

|---|---|

| New C# MCP server starts | Use this skill |

| Existing server needs local troubleshooting | Use `mcp-csharp-debug` |

| Server needs automated tests | Use `mcp-csharp-test` |

| Server needs packaging or deployment | Use `mcp-csharp-publish` |

## Workflow

| Step | Agent Action | Test | Pass |

|---|---|---|---|

| 1. Choose transport | Agent selects stdio for local subprocess use or HTTP for remote service use. Agent reads `references/transport-config.md` for transport-specific host, auth, and observability patterns. | Agent records selected transport. | One transport path is selected for the new server. |

| 2. Scaffold project | Agent uses `dotnet new mcpserver -n <ProjectName>` or `dotnet new web -n <ProjectName>` plus required MCP package. | Run scaffold command. | Project files are created with the intended transport shape. |

| 3. Add MCP surface | Agent adds tool, prompt, or resource types with clear `[Description]` metadata. Agent reads `references/api-patterns.md` for attribute, return type, DI, and builder patterns. | Inspect changed source files. | Every public MCP callable member has description metadata. |
| 4. Configure hosting | Agent uses `.WithStdioServerTransport()` for stdio or HTTP MCP registration plus `MapMcp()` for web hosting. Agent reads `references/transport-config.md` for concrete hosting patterns. | Inspect `Program.cs`. | Transport registration matches the selected project shape. |

| 5. Verify startup | Agent builds and starts the server with the existing toolchain. | Run `dotnet build` and `dotnet run` in scope. | Zero build errors and server startup succeeds. |

## Transport Matrix

| Transport | Agent Uses When | Required Configuration | Pass |

|---|---|---|---|

| Stdio | Local CLI, IDE, or Copilot subprocess scenarios | `AddMcpServer().WithStdioServerTransport()` and stderr-only logging | Server waits for JSON-RPC on stdin with no stdout log noise. |

| HTTP | Remote service, container, or shared-client scenarios | HTTP MCP registration plus `app.MapMcp()` | MCP endpoint is reachable on the configured route. |

## Verification Matrix

| Test | Run | Pass |

|---|---|---|

| Build verification | `dotnet build` for the touched project | Zero build errors. |

| Metadata verification | Inspect tool, prompt, and resource members. | Description metadata exists on each exposed MCP surface. |

| Startup verification | `dotnet run` for the touched project | Server starts with the intended transport path. |

## Reference Files

| File | Covers | Agent Reads When |
|---|---|---|
| `references/api-patterns.md` | MCP SDK attributes, return types, injected parameters, builder APIs, and package selection. | Agent reads this file when adding or reviewing tool, prompt, or resource implementations and SDK registration patterns. |
| `references/transport-config.md` | Stdio and HTTP transport setup, custom paths, auth, and observability configuration. | Agent reads this file when choosing or wiring the server transport and host configuration. |

## Guardrails

- Agent keeps stdio logs on stderr so stdout stays protocol-clean.

- Agent keeps HTTP hosting explicit with `MapMcp()`.

- Agent exposes only intentional tool, prompt, and resource types.
