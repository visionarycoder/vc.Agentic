---
title: "VERSION"
description: "Version and change history of the vc.Agentic skill library."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
version: "1.1.0"
updated: "2026-11-24"
---

# VERSION

1.1.0

This is the version of the **vc.Agentic** repository: the agent skill library, its templates and samples, and the maintenance tooling. It is the value shown in the [README](README.md).

## Versioning rules

- The version follows `MAJOR.MINOR.PATCH`.
- **MAJOR** – a change to repository purpose, skill layout, or metadata profile that breaks existing consumers.
- **MINOR** – skills added, removed, or consolidated, or new tooling and agent entry points.
- **PATCH** – corrections, clarifications, and link or formatting fixes.
- When the version changes, update this file and the `updated` date of every changed document, then run `python tools/skills.py refresh`.

## Change history

| Version | Date | Summary |
|---------|------|---------|
| 1.1.0 | 2026-11-24 | Removed technology-specific and creative-production skills (225 to 208 skills), removed empty collections, normalized line endings to LF, and repaired stale cross-references. |
| 1.0.0 | 2026-11-24 | Technology-neutral library of 225 skills after novelty audits and removal of licensed, vendor, bio, trading, and technology-specific skills; added `vc.Agentic.slnx`, session-start hooks for Codex and Claude Code, and entry files for Copilot, Gemini, and Cursor. |
