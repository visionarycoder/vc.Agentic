---
metadata-version: "1.0.0"
title: "vc.Agentic"
description: "Reusable agent skills, supporting resources, task templates, and illustrative component scaffolds."
document-type: "index"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-09"
---

# vc.Agentic

vc.Agentic is a reusable library of agent skills, supporting references, scripts and assets, task templates, and illustrative component scaffolds. It helps agents carry out assigned work through discovery, planning, implementation, review, and verification within the consuming project's accepted requirements and designs.

The library covers software engineering, volatility-based decomposition, .NET, Roslyn, Azure, and additional data and domain workflows. Its maintenance tools validate skill packaging and keep the catalogs and inventory aligned with the library.

A skill supplies task guidance. It does not grant decision or approval authority, implement a production framework, or provide an agent orchestration runtime.

## Skills

All skills live in [.agents/skills](.agents/README.md). Start with the [recommended core and optional collections](.agents/collections.md). Use the [catalog](.agents/README.md) or [inventory CSV](.agents/inventory.csv) to find a capability. Related skills use `accounting-`, `azure-`, `bio-`, `msbuild-`, `mstest-`, `roslyn-`, and `trading-` prefixes.

Each package has one `SKILL.md` and may include supporting references, scripts, or assets. Read only the resources needed for the task. Client discovery and tool availability depend on the consuming environment; this repository does not imply global installation.

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

Every skill uses the [extended metadata profile](tools/README.md). Run `python tools/skills.py check` to validate the library and `python tools/skills.py refresh` after changes. The maintenance guide covers safe scaffolding, renaming, removal, normalization, and overlap review.

See [third-party notices](THIRD_PARTY_NOTICES.md) for bundled license evidence.
