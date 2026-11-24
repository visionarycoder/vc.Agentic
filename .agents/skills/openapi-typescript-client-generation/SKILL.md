---
name: "openapi-typescript-client-generation"
description: "Generate deterministic TypeScript clients from ASP.NET Core OpenAPI documents by using pinned tools, versioned outputs, and runtime wrappers."
metadata:
  metadata-version: "1.0.0"
  title: "OpenAPI TypeScript Client Generation"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# OpenAPI TypeScript Client Generation

Agent treats the OpenAPI document as the server contract authority and keeps generated client code isolated from handwritten application logic.

## When to Use

| Condition | Agent Action |

|---|---|

| TypeScript or Vue app consumes ASP.NET Core REST APIs | Use this skill |

| Routes, DTOs, or API versions already exist in OpenAPI | Use this skill |

| Server has no stable machine-readable contract | Do not use this skill |

| Streaming JSON-seq client is the main task | Use protocol-specific guidance instead |

## Contract Rules

| Rule | Agent Verifies | Fix |

|---|---|---|

| OAPI-001 | One versioned OpenAPI document exists per API version | Export or generate versioned document |

| OAPI-002 | Operation IDs are stable and unique | Fix server-side operation metadata |

| OAPI-003 | Generated output lives in a dedicated folder | Isolate generated code from handwritten code |

| OAPI-004 | Generator version is pinned | Pin NSwag or OpenAPI Generator version |

| OAPI-005 | Auth and correlation stay in handwritten wrappers | Add client factory or transport wrapper |

| OAPI-006 | Error mapping preserves Problem Details | Parse `application/problem+json` in wrapper code |

| OAPI-007 | CI detects drift | Add regeneration and diff check |

## Workflow

1. Export one versioned OpenAPI document per API version (committed or reproducible).
2. Pin the generator (NSwag or OpenAPI Generator) version.
3. Generate into a dedicated versioned folder; keep prior versions side by side during migrations.
4. Keep auth, correlation, and Problem Details mapping in handwritten wrappers.
5. Run existing generation, diff, and TypeScript build commands in scope. Pass: clean regeneration yields zero diff and zero compile errors.

Fix contract problems at the OpenAPI source; never hand-edit generated files.
