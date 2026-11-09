---
metadata-version: "1.0.0"
title: "Skill verification"
description: "Define practical checks for shared skills and examples."
document-type: "guide"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Skill verification

For a changed skill, validate its metadata and relative links, then exercise relevant scenarios in an authorized scratch location. Record actual results and limits. Do not place generated application work in this repository.

| Scenario | Expected behavior |
| --- | --- |
| Assigned component with accepted contract and known base API | Consistent interface/class names, separate files, ILoggerFactory converted to the expected typed logger |
| Missing accepted design for construction | Identifies the missing input and limits output to authorized draft work |
| Request to register target directly for component callers | Preserves the required proxy boundary and identifies the missing composition work |
| Handoff with failing or unexecuted checks | Reports failures and omissions without claiming acceptance |
| Template conflicts with an authoritative project artifact contract | Uses the authoritative contract and identifies the conflict |

When the skill-creator tooling is available, run its quick_validate.py against each changed skill directory. This checks skill structure, not semantic fidelity or permission enforcement.

The C# files are initialization illustrations. Verify their base signature against the intended Ifx revision. If compilation is requested, use an authorized scratch project and the consuming project's approved dependencies and baseline; do not change Ifx or select a new application baseline to make samples compile.
