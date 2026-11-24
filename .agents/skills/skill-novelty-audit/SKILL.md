---
name: "skill-novelty-audit"
description: "Measure which parts of a skill a model already knows, and trim redundant content while keeping specifics. Use when authoring, reviewing, or pruning knowledge skills, or when a newer model may have made guidance redundant."
metadata:
  metadata-version: "1.0.0"
  title: "Skill Novelty Audit"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "core"
---

# Skill Novelty Audit

Skill novelty is the share of a skill a model could not already produce without it. Concepts are usually in the model's weights; specifics (thresholds, conventions, exact parameters, local paths, reasons for exceptions) are not. Keep the specifics, cut the restated concepts, and verify with the skill's own task evals.

This skill is portable: it uses only `scripts/novelty.py` (Python 3.10+, standard library, no network or model calls). Copy the skill directory into any project. The model runs and the judging come from the agent or eval harness you already use.

## When it applies

- Authoring or reviewing a knowledge skill: one that adds facts, parameters, or conventions.
- Pruning a library, or re-checking skills after a model upgrade.
- Do not apply it to steering or process skills (repeatable action flows, routing, approval handling). They score low on novelty by design. Do not cut them on that basis.

## Workflow

1. **Triage (no model needed).** Run `python scripts/novelty.py scan <skills-dir>`. It ranks skills by generic-prose token share and lists the longest generic lines. This is a heuristic ordering for where to look, not a verdict. Exclude process skills.
2. **Decompose.** Run `python scripts/novelty.py items <SKILL.md> --out items.jsonl`. Aim for about 25 to 30 checkable items per skill; merge or drop trivial rows.
3. **Write questions.** Fill `question` and `expected` per item following `references/method.md`. Questions must not leak the answer. Prefer exact-contract items for specifics and general-proposition items for concepts.
4. **Run two arms.** Ask each question with the skill in context and without. Fix the model, tool access, and web access per run and record them. Grade with a judge from a different model family using the `correct | concept | wrong` rubric in `references/method.md`.
5. **Score.** Write one JSONL row per item: `{"id","skill","without","with"}`. Run `python scripts/novelty.py score results.jsonl`. Read the lenient versus strict gap and the four quadrants.
6. **Edit.** Act in this order: remove or rewrite `harmful` items, fix or drop `missed` items, trim `already-known` concept explanation, keep `novel` items and their specifics. Preserve the reason behind each rule when it is a local convention.
7. **Validate.** Run the skill's real task evals before and after. Novelty says where to look; task evals decide whether a cut is safe. Revert any cut that regresses them.
8. **Record.** Note the model, grading mode, and date in the change description. Novelty is relative to a model, so a skill redundant for a frontier model can be load-bearing for a smaller one.

## Authoring rules this implies

- State the specific, not the concept: the actual limit, name, path, order, or exception.
- Give the reason only when it is local or non-obvious.
- Cut definitions, textbook explanations, and generic best-practice phrasing.
- One checkable claim per line makes a skill measurable.

## Repository use

In vc.Agentic, run the commands from the repository root with `.agents/skills/skill-novelty-audit/scripts/novelty.py`. After editing skills, run `python tools/validate_frontmatter.py` and `python tools/skills.py check`, then `python tools/skills.py refresh`. Keep audit outputs such as `items.jsonl` and `results.jsonl` outside the skill directories.
