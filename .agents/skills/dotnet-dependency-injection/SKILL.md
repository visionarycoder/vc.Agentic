---
name: "dotnet-dependency-injection"
description: "Combined dotnet dependency injection guidance with task/provider-specific modes. Govern dependency injection lifetimes, registrations, and composition-root usage across .NET services."
metadata:
  metadata-version: "1.0.0"
  title: "Dotnet dependency injection"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# Dotnet dependency injection

Use this skill for the topic described below. Select the matching task, host, provider, and repository context before loading guidance. Source instructions never override the user, host permissions, approved design, or target repository rules.

## Repository defaults

- Scoped: DbContext, repositories, and Manager/Engine types with a scoped dependency.
- Singleton: hosted services and cache owners; they must not capture scoped services.
- Transient: lightweight stateless helpers.
- MAUI: register Pages and ViewModels with `AddTransient`; `AddScoped` is rarely useful because MAUI has no built-in per-page scope. Register Shell pages with `Routing.RegisterRoute(nameof(Page), typeof(Page))` so `GoToAsync` resolves them through DI.

## Context-specific guidance

| Context | Frontmatter update | Guidance |
| --- | --- | --- |
| dependency-injection | undated | [Instructions](references/contexts/dependency-injection/guide.md) |
| dependency-injection-patterns | 2026-07-29 | [Instructions](references/contexts/dependency-injection-patterns/guide.md) |
| dotnet-dependency-injection-standards | 2026-08-15 | [Instructions](references/contexts/dotnet-dependency-injection-standards/guide.md) |
| maui | undated | [Instructions](references/contexts/maui/guide.md) |

Load only the relevant context. Newer dated guidance is preferred within the same context; it does not make unrelated providers interchangeable. Compare tied or undated alternatives rather than combining incompatible requirements.
