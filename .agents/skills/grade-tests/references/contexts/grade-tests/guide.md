---
metadata-version: "1.0.0"
title: "Grade Tests"
description: "Preserve scoped source guidance for grade-tests."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Grade Tests

Agent grades named tests one by one and generates a compact score table.

## When to Use

| User prompt | Use |
|---|---|
| User asks for per-test grades | Use this skill |
| User asks for a PR comment on selected tests | Use this skill |
| User gives a file and says grade every test here | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User asks for whole-suite audit | Use `test-anti-patterns` or another suite skill |
| User asks to write or fix tests | Use a test-writing skill |
| User asks for coverage or CRAP numbers | Use `coverage-analysis` or `crap-score` |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Explicit scope | Yes | List test names, files, or diff scope |
| Test bodies | Yes | Read test source when the user does not inline it |
| Production code | No | Read production code when behavior context matters |
| Output style | No | Default to PR-comment table |

## Scoring Matrix

| Dimension | Strong signal | Weak signal |
|---|---|---|
| Assertions | Outcome assertions verify behavior | Trivial, tautological, or missing assertions |
| Focus | One behavior with readable setup | Mixed behaviors or hidden shared state |
| Hygiene | Stable structure and clear names | Flaky flow, swallowed exceptions, or over-mocking |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent verifies the grading scope is explicit. | Read the prompt. | Each target test is named or discoverable from one file scope. |
| 2 | Agent reads framework-specific guidance from `test-analysis-extensions`. | Read the matching extension file. | Guidance matches the language and framework in scope. |
| 3 | Agent reads each requested test body. | Read the source file or symbol. | Each requested test is found or marked missing. |
| 4 | Agent scores each test on assertions, focus, and hygiene. | Read the score table. | Each test has one grade and one note. |
| 5 | Agent caps the overall grade at the weakest trust-breaking dimension. | Compare subscores to final score. | Final grade never exceeds the weakest critical dimension. |
| 6 | Agent generates a compact output table. | Read the final report. | Output has one row per requested test. |

## Output Columns

| Column | Content |
|---|---|
| Test | Fully qualified name or file-local name |
| Grade | `A` through `F` |
| Score band | `90-100`, `80-89`, `70-79`, `60-69`, or `0-59` |
| Note | One concise reason |

## Verification Checklist

- [ ] Agent used an explicit grading scope.
- [ ] Agent read the matching framework guidance.
- [ ] Agent graded only observable evidence.
- [ ] Agent marked missing tests as `N/A`.
- [ ] Agent kept the output compact.
- [ ] Agent wrote one row per requested test.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Scope is vague | Agent stops and asks for explicit scope. |
| Agent grades the whole workspace | Agent limits work to the named scope. |
| Agent deducts for hypothetical gaps | Agent scores only observed defects. |
| Agent ignores framework idioms | Agent reads the extension guidance first. |
