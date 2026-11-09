---
metadata-version: "1.0.0"
title: "Package verification"
description: "Validate extended metadata, current catalogs, and portable package structure."
document-type: "index"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Package verification

Run these commands from the repository root:

```text
python tools/validate_frontmatter.py
python tools/skills.py check
python -m unittest discover -s tests -p "test_*.py"
```

The frontmatter validator checks all skill entrypoints against the extended profile. The full check adds name/folder parity, unique entrypoints, local links, Markdown LF formatting, package artifacts, and inventory consistency. The tests exercise local maintenance operations without running bundled cloud helpers.

After an addition, rename, removal, or resource change, run `python tools/skills.py refresh`. Use the dry-run mutation commands in the [maintenance guide](../tools/README.md) to preview changes before applying them.

Keep one-time computer inventories, migration ledgers, merge evidence, interpreter caches, and vendor UI files out of published packages. The maintained tools and their isolated tests are intentional repository infrastructure.

[Project prerequisites](host-requirements.md) and runtime compatibility still need task-specific checks in the consuming environment. Structural validation does not certify every SDK, emulator, cloud integration, or component sample.
