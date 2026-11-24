---
name: "add-python-version-support"
description: "Guide changes required when a project adds a newer Python version above its current tested ceiling while preserving its existing minimum. Use when asked to support, test, certify, or prepare for a newer Python release at the upper end of the support range without dropping existing runtimes."
metadata:
  metadata-version: "1.0.0"
  title: "Add Python Version Support"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Add Python Version Support

Use this skill to extend the upper end of a project's tested Python support range while preserving compatibility with its existing minimum.

## Core Principle

Adding a newer Python version raises the tested ceiling, not the floor: do not adopt syntax or APIs from the added version while earlier versions remain supported. If the project supports exactly one version and replaces it, follow this workflow and `drop-python-version-support`.

## Workflow

### 1. Establish Scope and Existing Support

1. Identify the Python version being added.
2. Determine the project's existing minimum and highest tested versions.
3. Determine whether the target is a package, application, standalone script, or a workspace containing multiple independently configured projects.
4. Resolve each independent project separately. Do not impose one support range on unrelated project roots.
5. Read actual metadata, test configuration, and support documentation. Do not infer support from the selected interpreter.
6. Determine whether the target Python release is final or prerelease. Treat prerelease results as provisional.

If a request says only "upgrade" or "migrate" to a Python version, determine whether the user intends to add another tested version, replace older runtimes, or do both. Do not silently change the minimum when the intent is ambiguous.

This workflow assumes the target is newer than the project's highest tested version. If the target is already inside the tested range, treat the request as targeted validation rather than raising the ceiling. If it fills an untested gap, add only the missing test coverage and related support declarations. If it is below the current minimum, report that it expands support below the current compatibility floor and requires separate backward-compatibility analysis; do not lower the minimum or apply this workflow unchanged.

### 2. Inventory Support Declarations

Inspect the files the project actually uses: `requires-python` or `python_requires` (pyproject, setup.cfg, setup.py, inline script metadata), package-manager constraints, Trove classifiers, CI/tox/nox matrices, tool target versions, dependency markers, and support docs.

Keep Pyright `pythonVersion`, mypy `python_version`, Ruff `target-version`, and similar settings at the existing minimum. The development interpreter and deployment default are separate choices; do not change them.

### 3. Review Compatibility Guidance

Read the official What's New (`https://docs.python.org/{version}/whatsnew/{version}.html`) for every release after the previous tested ceiling through the target, focusing on porting, deprecations, and removals. If it is unavailable, say so rather than inventing details.

### 4. Add and Test the Target Version

1. Add the target to CI and test matrices using project conventions; quote versions in YAML.
2. If the target skips intermediate releases, follow the project's test policy: validate them or report them as supported-but-untested or unsupported. Do not invent classifiers for unvalidated versions.
3. Run the existing suite on the target. Surface `DeprecationWarning` per the project's warning policy, or with a targeted run if none exists.
4. Fix deprecations, removals, and failures with changes that remain valid on the existing minimum; if none exists, report and ask before adding a compatibility layer.
5. Re-run tests on the existing minimum after any change, then run configured type checking, linting, and package-build validation.

Do not guess dependency versions. When a dependency blocks the target, cite the evidence and make the narrowest change allowed by dependency policy, or report the blocker.

### 5. Update Support Metadata

1. Keep the lower bound of `Requires-Python` unchanged.
2. If an existing upper bound excludes the target, remove or widen it only after validation, without changing unrelated exclusions.
3. Add the Trove classifier only after validation shows support and the classifier exists.
4. Update docs to distinguish declared from tested versions. Regenerate tool-owned lockfiles; do not hand-edit them.

### 6. Final Check

Confirm that the target is in repeatable test configuration, no target-only syntax or API entered code that must run on the minimum, and metadata, classifiers, matrices, and docs agree. Report prerelease results as provisional.

## Completion Report

Report:

-   the existing support range and added version;
-   compatibility guidance reviewed;
-   deprecations, removals, dependency issues, and test failures addressed;
-   test and validation results for the target and existing minimum;
-   metadata, classifiers, matrices, and documentation updated;
-   unavailable interpreters, provisional results, or unresolved blockers.

Do not claim support when the target-version test suite did not run or failed.
