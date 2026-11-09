---
metadata-version: "1.0.0"
title: "Test Fixes Bundle Alias"
description: "Preserve scoped source guidance for test-fixes-bundle."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Test Fixes Bundle Alias

This skill routes test-analysis requests through the canonical `test-fixes` bundle.
This skill keeps one routing surface while preserving specialized downstream skills.

## Routing Table

| Request signal | Route |
|---|---|
| General test-quality analysis | `.agents/skills/test-fixes/SKILL.md` |
| Pragmatic anti-pattern review | `.agents/skills/test-anti-patterns/SKILL.md` via `test-fixes` |
| Missing edge-case or escaped-defect analysis | `.agents/skills/test-gap-analysis/SKILL.md` via `test-fixes` |
| Assertion depth or diversity audit | `.agents/skills/assertion-quality/SKILL.md` via `test-fixes` |
| Academic smell catalog review | `.agents/skills/test-smell-detection/SKILL.md` via `test-fixes` |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Normalize | Agent maps the request to the canonical `test-fixes` entry point. | Routing decision |
| 2. Delegate | Agent follows the routing table in `test-fixes`. | Specialized analysis |
| 3. Report | Agent returns findings and follow-up actions from the specialized skill. | Consolidated result |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Canonical entry | Review the selected bundle. | The request routes through `test-fixes` instead of duplicating bundle logic here. |
| Specialized route | Compare user intent to downstream skill choice. | The downstream skill matches the requested test-analysis surface. |
| Result shape | Review final reporting. | The final output preserves actionable findings and follow-up actions. |
