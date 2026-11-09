---
metadata-version: "1.0.0"
title: "C# MCP Server Publishing"
description: "Preserve scoped source guidance for mcp-csharp-publish."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# C# MCP Server Publishing

Agent publishes MCP servers by matching the package path to the transport path and by verifying deployable artifacts before release.

## When to Use

| Condition | Agent Action |

|---|---|

| Stdio server needs a distributable package | Use this skill |

| HTTP server needs a container or Azure deployment path | Use this skill |

| Server still fails local startup | Use `mcp-csharp-debug` first |

| Server lacks tests for core behavior | Pair with `mcp-csharp-test` |

## Publishing Matrix

| Transport | Delivery Path | Agent Verifies |

|---|---|---|

| Stdio | NuGet tool or repository package flow | Package metadata, executable entry point, and install path |

| HTTP | Docker image and hosting manifest | Container build, exposed port, and MCP endpoint route |

| Hosted registry path | MCP registry metadata | Manifest fields align with published artifact |

## Workflow

| Step | Agent Action | Test | Pass |

|---|---|---|---|

| 1. Choose release path | Agent maps server transport to NuGet, container, Azure, or registry output. Agent reads `references/nuget-packaging.md`, `references/docker-azure.md`, or `references/mcp-registry.md` for the selected release path. | Agent records selected release path. | One release path is selected per artifact. |
| 2. Produce artifact | Agent builds package or container by using the repository toolchain. Agent reads `references/nuget-packaging.md` for stdio package flows or `references/docker-azure.md` for container build and deploy flows. | Run existing publish or build command in scope. | Artifact is created successfully. |
| 3. Add release metadata | Agent sets package, image, or registry metadata that matches the MCP server contract. Agent reads `references/mcp-registry.md` and `references/nuget-packaging.md` for manifest and version-alignment details. | Inspect changed metadata files. | Artifact metadata identifies the correct server and version path. |
| 4. Check runtime shape | Agent verifies entry point, port, route, and dependency configuration for the selected path. Agent reads `references/docker-azure.md` for HTTP hosting checks or `references/nuget-packaging.md` for local tool-install validation. | Run local package install, container run, or deployment validation in scope. | Artifact starts with the intended MCP surface. |

| 5. Verify release safety | Agent checks secret handling, health path, and rollback readiness in scope. | Inspect changed deployment and config files. | Zero secrets are embedded and runtime checks exist where the platform supports them. |

## Verification Matrix

| Test | Run | Pass |

|---|---|---|

| Build or publish verification | Run existing publish command for the touched artifact path. | Zero publish errors. |

| Startup verification | Start the produced package or container in scope. | Artifact starts and exposes the intended MCP surface. |

| Metadata verification | Inspect package manifest, Dockerfile, or registry descriptor. | Metadata matches the server identity and transport path. |

## Reference Files

| File | Covers | Agent Reads When |
|---|---|---|
| `references/docker-azure.md` | Dockerfile patterns, Azure Container Registry, Azure Container Apps, App Service, and secret handling. | Agent reads this file when packaging or validating HTTP MCP servers for container or Azure deployment. |
| `references/mcp-registry.md` | MCP Registry prerequisites, `server.json` schema, namespace rules, publish flow, and version consistency. | Agent reads this file when preparing registry metadata or publishing a public MCP server listing. |
| `references/nuget-packaging.md` | NuGet tool packaging, `.csproj` metadata, local install checks, and registry integration for stdio servers. | Agent reads this file when packaging or validating a stdio MCP server as a NuGet-delivered artifact. |

## Guardrails

- Agent keeps secrets out of package metadata, Dockerfiles, and committed config.

- Agent aligns the artifact path with the server transport path.

- Agent verifies startup before treating packaging work as complete.
