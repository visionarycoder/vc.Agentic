---
metadata-version: "1.0.0"
title: "Test Smell Detection"
description: "Preserve scoped source guidance for test-smell-detection."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Test Smell Detection

Agent runs a formal smell audit and reports citable, location-backed findings.

## When to Use

| User prompt | Use |
|---|---|
| User asks for a formal smell audit | Use this skill |
| User cites testsmells.org or named smells | Use this skill |
| User wants severity-ranked smell remediation | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User asks for a quick pragmatic review | Use `test-anti-patterns` |
| User asks for assertion diversity only | Use `assertion-quality` |
| User asks where tests are missing | Use `test-gap-analysis` or `find-untested-sources` |
| User asks to write tests | Use a test-writing skill |

## Required Inputs

| Input | Required | Description |
|---|---|---|
| Test files | Yes | Agent needs test code or a test project scope. |
| Framework | No | Agent infers it, then reads `test-analysis-extensions`. |
| Production context | No | Agent reads it when a smell depends on collaboration boundaries. |

## Smell Catalog

| Smell | Signal | Severity | Agent fix |
|---|---|---|---|
| Conditional Test Logic | Branching or loops inside the test body | High | Agent splits cases or parameterizes inputs. |
| Mystery Guest | Test reaches files, DB, HTTP, env, or hidden fixtures | High | Agent replaces the hidden dependency with a hermetic fixture or test double. |
| Sleepy Test | Fixed waits or delays control timing | High | Agent replaces waits with event or state synchronization. |
| Assertion-Free Test | No assertion, verification, or snapshot exists | High | Agent adds meaningful verification. |
| Eager Test | One test drives several distinct production calls | Medium | Agent splits behaviors or labels the test integration-focused. |
| Magic Number Test | Opaque expected literals dominate intent | Medium | Agent introduces named inputs or derived expectations. |
| Sensitive Equality | Test compares serialized strings or `ToString()` output only | Medium | Agent asserts structured fields or trusted formatting helpers. |
| Exception Handling in Test | Manual exception handling manages expected failures | Medium | Agent uses framework exception helpers. |
| General Fixture | Setup initializes unused data or collaborators | Low | Agent narrows fixture scope. |
| Ignored or Skipped Test | Skip markers remain without current rationale | Low | Agent requests re-enable, triage, or removal. |

## Workflow

| Step | Agent action | Test | Pass |
|---|---|---|---|
| 1 | Agent reads the matching extension file. | Review chosen extension. | Language-specific markers and assertion forms match the test framework. |
| 2 | Agent scans only the requested test scope. | Review selected files. | Audit stays bounded. |
| 3 | Agent maps each finding to one smell entry. Agent reads `references/test-smell-catalog.md` when the audit needs the extended taxonomy, research background, or prevalence context. | Review finding table. | Every finding uses a published smell label. |
| 4 | Agent calibrates false positives for integration and parameterized tests. | Review calibrated findings. | Legitimate framework idioms are not misreported. |
| 5 | Agent writes a prioritized report. | Review final report. | Each finding includes path, test identifier, snippet, severity, and one-line fix. |

## Report Contract

| Field | Requirement |
|---|---|
| Summary | Agent reports counts by severity and smell type. |
| Finding | Agent reports smell, path, test name, snippet, severity, and fix. |
| Remediation plan | Agent orders work by severity and spread. |
| Calibration note | Agent names the false-positive filters it applied for the smells it reported. |

## Reference Files

| File | Coverage | Agent Reads It When |
|---|---|---|
| `references/test-smell-catalog.md` | Extended 19-smell taxonomy, research background, prevalence notes, and extra examples beyond the core top-10 catalog. | Agent reads it during deep smell audits when the report needs academic taxonomy alignment, extended smell coverage, or citation-ready context. |

## Verification Checklist

- [ ] Agent loaded the framework extension first.
- [ ] Agent kept every finding location-backed.
- [ ] Agent used one smell label per finding.
- [ ] Agent filtered integration and parameterized idioms conservatively.
- [ ] Agent produced one-line fixes that stay test-focused.

## Common Pitfalls

| Pitfall | Agent fix |
|---|---|
| Agent treats any helper usage as Mystery Guest | Agent flags only hidden external dependency coupling. |
| Agent misses mock verifications as assertions | Agent counts framework-native verifications and snapshots. |
| Agent reports every skip as severe | Agent uses Low severity unless risk context raises it. |
| Agent mixes pragmatic opinions with formal labels | Agent keeps smell labels aligned to the catalog. |
