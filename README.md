---
metadata-version: "1.0.0"
title: "vc.Agentic"
description: "Reusable agent skills, supporting resources, task templates, and illustrative component scaffolds."
document-type: "index"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-24"
---

# vc.Agentic

vc.Agentic is a reusable library of agent skills, supporting references, scripts and assets, task templates, and illustrative component scaffolds. It helps agents carry out assigned work through discovery, planning, implementation, review, and verification within the consuming project's accepted requirements and designs.

The library is technology-neutral by design: it keeps process, quality, and decision guidance and leaves product- and framework-specific how-to to the model and the project. Main areas are planning and execution workflow, debugging and verification, testing and test quality, code review and refactoring, security scanning and hardening, volatility-based decomposition (VBD), documentation and writing, data analysis and visualization, and skill authoring and maintenance. Its maintenance tools validate skill packaging and keep the catalogs, inventory, and solution aligned with the library.

A skill supplies task guidance. It does not grant decision or approval authority, implement a production framework, or provide an agent orchestration runtime.

## How to use it

1. Point your agent harness at this repository (see [agent harnesses](#agent-harnesses)). Agents are directed to [AGENTS.md](AGENTS.md), which is the entry point.
2. Let the agent read [skill-discovery-guide](.agents/skills/skill-discovery-guide/SKILL.md) when the right skill is unclear, then [skill-selection](.agents/skills/skill-selection/SKILL.md) to choose the smallest relevant set.
3. Read only the skills the task needs. Each package has one `SKILL.md` and may include references, scripts, or assets.

You can also browse the [catalog](.agents/README.md) or [inventory CSV](.agents/inventory.csv) yourself, or start from the [recommended core and optional collections](.agents/collections.md). Client discovery and tool availability depend on the consuming environment; this repository does not imply global installation.

## Agent harnesses

| Harness | Entry mechanism |
| --- | --- |
| Codex | [AGENTS.md](AGENTS.md) (read natively) and a `SessionStart` hook in [.codex/hooks.json](.codex/hooks.json); Codex asks you to review and trust the hook on first use |
| Claude Code | [CLAUDE.md](CLAUDE.md) (imports `AGENTS.md`) and a `SessionStart` hook in [.claude/settings.json](.claude/settings.json) |
| GitHub Copilot | [.github/copilot-instructions.md](.github/copilot-instructions.md); Copilot CLI also reads `CLAUDE.md` and the Claude hook |
| Gemini CLI | [GEMINI.md](GEMINI.md) (imports `AGENTS.md`) |
| Cursor | [.cursor/rules/vc-agentic.mdc](.cursor/rules/vc-agentic.mdc) |

The hooks run [tools/agent_entry.py](tools/agent_entry.py), which prints the "Start here" section of `AGENTS.md`, so the purpose and entry point have a single source. The hooks need Python on the path.

## Version

Current version: **1.1.0**. See [VERSION.md](VERSION.md) for versioning rules and change history.

## Skills

All skills live in [.agents/skills](.agents/README.md). Skills for volatility-based decomposition use the `vbd-` prefix.

## Solution

[vc.Agentic.slnx](vc.Agentic.slnx) lists every repository file under solution folders so the library can be browsed and searched in Visual Studio. It contains no buildable projects; the component samples are illustrative. `python tools/skills.py refresh` regenerates it and `check` reports when it is stale.

## Repository boundaries

| Repository | Owns |
| --- | --- |
| vc.Agentic | Reusable skills, supporting task templates, illustrative initialization examples |
| vc.Governance | Method rules, roles, required constraints, approval routes, lifecycle and artifact contracts |
| vc.Ifx | Production libraries, generators, analyzers, code fixes, proxies, and their executable tests |
| Consuming application | Its requirements, accepted design, implementation, tests, and operational evidence |

Governance catalogs its own administrative and documentation skills. Governing specifications stay in their owning repository instead of being copied into skill instructions. Consuming projects select applicable skills and reusable Ifx capabilities under their approved designs; collection membership does not select an application architecture or technology baseline.

## Templates and examples

- [Task and initialization templates](templates/README.md)
- [Component initialization samples](samples/components/README.md)
- [Package verification](.agents/verification.md)
- [Project and host prerequisites](.agents/host-requirements.md)

The component examples illustrate the requested ILoggerFactory constructor, separate interface and class files, and adaptation to the verified Ifx base API. They are starting structures, not production implementations or accepted component designs.

## License

Original repository material uses the [MIT License](LICENSE). Imported skills and other third-party material retain their existing licenses and notices. The repository license does not replace those terms or establish permission for imported material whose original terms are unverified.

## Maintenance

Every skill uses the [extended metadata profile](tools/README.md). Run `python tools/skills.py check` to validate the library and `python tools/skills.py refresh` after changes (it also regenerates the solution). The maintenance guide covers safe scaffolding, renaming, removal, normalization, and overlap review.

See [third-party notices](THIRD_PARTY_NOTICES.md) for bundled license evidence.
