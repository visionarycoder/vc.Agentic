---
name: "codebase-inspection"
description: "Inspect codebases w/ pygount: LOC, languages, ratios."
metadata:
  metadata-version: "1.0.0"
  title: "Codebase Inspection with pygount"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Codebase Inspection with pygount

Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios using `pygount`.

## Prerequisites

```bash
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

## 1. Basic Summary (Most Common)

Get a full language breakdown with file counts, code lines, and comment lines:

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and take a very long time or hang.

## 2. Common Folder Exclusions

Adjust based on the project type:

```bash
# Python projects
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript projects
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# General catch-all
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

## 3. Other Options

Use `--suffix=py,yaml,yml` to filter languages, and `--format=json` for machine-readable output. Omit `--format` for a per-file listing.

## Pitfalls

- Markdown shows 0 code lines (counted as comments); JSON counts are conservative, so use `wc -l` for JSON.
