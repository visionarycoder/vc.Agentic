---
metadata-version: "1.0.0"
title: "Test Fixes Bundle"
description: "Preserve scoped source guidance for test-fixes."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Test Fixes Bundle

Agent routes test-focused analysis, remediation to correct specialist.

Agent acts as the primary mixed-concern testing skill after `testing-intake-router` classifies the request.

## When to Use

| User prompt | Use |
|---|---|
| User asks for mixed or unclear testing remediation | Use this skill |
| User asks for the right test-analysis path across multiple concerns | Use this skill |
| Intake identified testing remediation but no single specialist is obvious yet | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User asks only for assertion analysis | Use `assertion-quality` |
| User asks only for test smells | Use `test-smell-detection` |
| User asks only for gap analysis | Use `test-gap-analysis` |
| User asks to create or execute tests | Use test authoring or run-test tooling directly |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Mixed-concern testing remediation belongs here after `testing-intake-router` |
| Specialist loading | Choose one testing specialist first based on dominant concern |
| Bundle scope | This skill exists to reduce ambiguity, not to replace focused specialist skills |
| Execution split | Test creation and test execution stay outside this bundle unless the user explicitly pivots |

## Verification

- [ ] Agent used this skill only for mixed or unclear testing remediation
- [ ] Agent selected one specialist first when the dominant concern became clear
- [ ] Agent kept test creation and test execution out of this bundle unless explicitly requested

## Bundle Coverage Matrix

| Area | Specialized skill source | Router reference |
|---|---|---|
| Pragmatic anti-pattern audit | `.github/skills/test-anti-patterns/SKILL.md` | `references/test-analysis-routing-table.md` |
| Mutation-style gap analysis | `.github/skills/test-gap-analysis/SKILL.md` | `references/test-analysis-routing-table.md` |
| Academic 19-smell catalog review | `.github/skills/test-smell-detection/SKILL.md` | `references/test-analysis-routing-table.md` |
| Assertion depth/diversity audit | `.github/skills/assertion-quality/SKILL.md` | `references/test-analysis-routing-table.md` |

## Router Rules

| User Request Contains | Route To | Reason |
|---|---|---|
| "pragmatic" / "clean code" | `test-anti-patterns` | Practical pattern audit |
| "mutation" / "escaped defect" | `test-gap-analysis` | Coverage gap detection |
| "test smell" / "academic" | `test-smell-detection` | 19-smell catalog |
| "assertion depth" / "assertion diversity" | `assertion-quality` | Assertion analysis |

## Required Workflow

### Phase 1: Intent classification

Agent performs:
1. Agent classifies request into one or more analysis tracks
2. Agent loads consolidated routing reference
3. Agent declares codebase scope, language

### Phase 2: Execute targeted analysis

Agent performs:
1. Agent runs only relevant specialized skill
2. Agent keeps findings evidence-based with file references
3. Agent avoids unrelated framework migrations or test generation suggestions unless asked

### Phase 3: Summarize and next actions

Agent performs:
1. Agent returns severity-ranked findings where applicable
2. Agent identifies highest-value follow-up fixes
3. Agent suggests when to switch to test generation or test execution tools

## Non-Goals

- This bundle does not generate new tests directly
- This bundle does not run test frameworks by itself
- For writing tests use `code-testing-agent` or `mstest-test-authoring`
- For executing tests use run-tests tooling.
