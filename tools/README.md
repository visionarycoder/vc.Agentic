---
metadata-version: "1.0.0"
title: "Skill maintenance"
description: "Maintain consistent skill metadata, navigation, and package structure."
document-type: "index"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Skill maintenance

Use Python 3.10 or later. These tools use the standard library and do not execute
bundled skill helpers, contact cloud services, or change third-party license text.
Run commands from the repository root, or supply `--root` before the subcommand.

## Validate

```text
python tools/validate_frontmatter.py
python tools/skills.py check
python -m unittest discover -s tests -p "test_*.py"
```

The dedicated validator checks every skill entrypoint's extended header. The full
check adds directory/name parity, nested entrypoints, Markdown formatting, local
navigation, unwanted package artifacts, and inventory consistency. Both return a
nonzero exit code on errors. Validation does not prove semantic usefulness or
runtime compatibility.

## Extended skill header

```yaml
---
name: "example-skill"
description: "Describe the capability and when it applies."
metadata:
  metadata-version: "1.0.0"
  title: "Example Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---
```

The required skill fields stay at the top level. Extended maintenance fields live
inside `metadata`, which keeps the package agent-neutral. `title` matches the first
H1 heading. `updated` records maintenance, not original authorship or source dates.
Collections are defined in the tool and shown in the generated catalog.

This profile uses a deliberately restricted YAML subset: JSON double-quoted string
values, unique kebab-case keys, and two-space indentation under `metadata`. It does
not accept YAML lists, aliases, tags, booleans, or multiline scalar syntax. Optional
standard scalar fields such as `license`, `compatibility`, and `allowed-tools` are
preserved. Do not set `license: MIT` on imported material without a basis for it.
Supporting references and source assets retain their own formats; the skill-header
profile applies to `SKILL.md`, not every Markdown example or third-party file.

## Add and normalize

```text
python tools/skills.py new example-skill --description "Describe the capability." --collection optional
python tools/skills.py new example-skill --description "Describe the capability." --collection optional --apply
python tools/skills.py normalize
python tools/skills.py normalize --apply
python tools/skills.py refresh
```

`new` and `normalize` preview changes unless `--apply` is present. A new entrypoint
is a draft scaffold; write its actual workflow before publication. Normalization
preserves names, descriptions, standard optional fields, and extra string metadata.
It updates the maintenance date, makes the title explicit, and normalizes header
and body formatting. It never invents a creation date or changes license files.
Use `--date YYYY-MM-DD` before the subcommand for an explicit maintenance date.

`refresh` rebuilds the inventory and both catalogs from current files. It does not
scan the computer, recover deleted skills, rewrite skill instructions, or recreate
collection snapshots. Review and commit generated catalog changes with the skills.

## Rename, remove, and clean links

```text
python tools/skills.py rename old-name new-name
python tools/skills.py rename old-name new-name --apply
python tools/skills.py remove obsolete-name
python tools/skills.py remove obsolete-name --apply
python tools/skills.py fix-links
python tools/skills.py fix-links --apply
```

Mutating commands validate package names and resolved boundaries before changing
files. Renames update current path references and invocation names, then refresh
the inventory. Removal previews targets, requires `--apply`, removes links to absent
files, and refreshes the catalogs. Link cleanup strips unavailable link targets while
retaining labels; it does not invent replacement files or inspect fenced examples.
Use the rename command before moving a skill so valid references can be updated.

## Review overlaps

```text
python tools/skills.py audit
```

The audit reports exact normalized-body duplicates and description-similarity
candidates. Similarity is a review aid, not permission to merge. Distinct provider,
framework, domain, authoring, and review modes can have similar descriptions.
Keep executable fixtures under `tests`, outside the discoverable skill directory.
