---
name: "vbd-method"
description: "Apply source-backed Volatility-Based Decomposition method guidance with explicit evidence labels and limits."
metadata:
  metadata-version: "1.0.0"
  title: "VBD method"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "vbd"
---

# VBD method

## When to use

Use this skill for architecture work that needs Volatility-Based Decomposition (VBD) method guidance.
Use `vbd-coding` when the task is a code change, refactor, or code review.
Use `vbd-boundary-design` when the task needs contracts, call rules, and authority assignment.
Use `vbd-design-validation` when the task needs review, Quality Assurance (QA), or change simulation checks.

## Required source position

Treat *Righting Software* by Juval Löwy as the verified primary book source.
Do not call the source book *Designing Software Architecture*.
Do not claim that the complete IDesign standard is verified.
The current detailed IDesign standard stayed behind an email gate during research.

## Method rules

| Rule | Classification | Scope | Source |
| --- | --- | --- | --- |
| Design around plausible change in behavior and interactions. | Primary guidance | Business and software architecture | InformIT author excerpt, sequence 2 |
| Use volatility, not feature lists, as the decomposition driver. | Primary guidance | Component discovery | InformIT author excerpt, sequence 2 |
| Separate business invariant discovery from proposed solution design. | Primary guidance | Requirements and design | InformIT author excerpt, sequence 3 |
| Use time and customer axes to discover change. | Primary guidance | Volatility discovery | InformIT author excerpt, sequence 3 |
| Prefer bounded variability over unlimited variation points. | Primary guidance | Component design | InformIT author excerpt, sequence 2 |
| Reject speculative changes that lack credible evidence. | Primary guidance | Scope control | InformIT author excerpt, sequence 3 |
| Treat a rough ten-service observation as an observation, not a target count. | Secondary interpretation | Size review | InfoQ book review and author Q&A |
| Keep logical architecture separate from physical deployment. | Primary guidance | Packaging | *Righting Software* table of contents and author material |
| Preserve repository-local stricter contract rules. | Repository rule | Financial IDL and similar repositories | `.agents/skills/vbd-system-design/SKILL.md` |

## Discovery procedure

1. Name each activity with one trigger and one observable result.
2. Record a credible change event for each proposed component.
3. Classify each conclusion as `Primary guidance`, `Secondary interpretation`, `Team policy`, `Repository rule`, or `Heuristic/Unknown`.
4. Record source, section, scope, and known exceptions for each conclusion.
5. Stop the split when a new component has no independent reason to change.
6. Record why merged responsibilities change together when the design keeps them together.

## Anti-patterns

- Do not split components by database entity, folder, or noun list.
- Do not use a fixed service count as a pass condition.
- Do not add a Manager, Engine, Access, or Data Transfer Object (DTO) because a template says so.
- Do not treat Open/Closed Principle text as a substitute for VBD change evidence.
- Do not duplicate DTOs unless independent evolution has evidence.

## References

- [Source register and rule matrix](references/source-register.md)
- [Component roles](references/component-roles.md)
