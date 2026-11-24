---
name: "dotnet-webapi"
description: "Scaffold or refactor ASP.NET Core Web API projects with OpenAPI, dependency injection, typed contracts, and testable endpoint structure."
metadata:
  metadata-version: "1.0.0"
  title: ".NET Web API Project"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# .NET Web API Project

Agent uses this skill to scaffold, configure, or refactor ASP.NET Core Web API projects.

## When to Use

| User prompt | Use |

|---|---|

| User asks for a new Web API project | Agent uses this skill |

| User converts a console or library project into a Web API | Agent uses this skill |

| User asks to add OpenAPI, DTOs, routing, or endpoint structure | Agent uses this skill |
| User already routed through `webapi-intake-router` to new implementation work | Agent uses this skill |

## When Not to Use

| User prompt | Route |

|---|---|

| User asks for authorization or authentication design | Agent uses `webapi-authz-hardening` or auth skills |

| User asks for input-validation rules | Agent uses `webapi-input-validation` |

| User asks for Problem Details or exception-pipeline design only | Agent uses `webapi-error-contract-hardening` or `aspnet-exception-handler` |
| User asks for mixed Web API remediation across several concerns | Agent uses `webapi-fixes-bundle` via `webapi-intake-router` |

## Required Inputs

| Input | Required | Notes |

|---|---|---|

| Project name | Yes | Agent uses the repository naming pattern. |

| Target framework | No | Agent uses the current approved .NET target when the prompt does not specify one. |

| Style | No | Agent chooses minimal API or controllers from endpoint count and binding complexity. |

| Persistence provider | No | Agent wires persistence only when the prompt includes it. |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | New Web API implementation belongs here after `webapi-intake-router` |
| Remediation split | Mixed remediation routes to `webapi-fixes-bundle` instead of expanding this skill |
| Specialist loading | Load one specialist only when auth, validation, routing, or error contracts dominate |
| Contract scope | This skill owns API project structure and endpoint composition, not every specialist concern |

## Workflow

1. Enable nullable and implicit usings; target the current approved framework.
2. Choose one primary endpoint style: minimal APIs for up to 30 straightforward endpoints, controllers for many endpoints or heavy MVC filters.
3. Register OpenAPI, Problem Details, HTTPS redirection, and dependency injection in `Program.cs`.
4. Keep business logic out of handlers; mixed remediation across concerns goes to `webapi-fixes-bundle` instead of expanding this skill.
5. Run `dotnet build <project-or-solution>` and `dotnet test <test-project>`.

## References

- Detailed examples and patterns: `references/patterns.md`

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [dotnet-webapi-alternative-1](references/contexts/dotnet-webapi-alternative-1/guide.md)
- [dotnet-webapi-alternative-2](references/contexts/dotnet-webapi-alternative-2/guide.md)
- [dotnet-webapi-alternative-3](references/contexts/dotnet-webapi-alternative-3/guide.md)
- [dotnet-webapi-alternative-4](references/contexts/dotnet-webapi-alternative-4/guide.md)
