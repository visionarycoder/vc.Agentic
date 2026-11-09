---
name: "testing-intake-router"
description: "Route test-analysis and test-remediation requests to the minimum correct testing skill by separating bundle analysis, anti-pattern review, gap analysis, assertion quality, and smell detection."
metadata:
  metadata-version: "1.0.0"
  title: "Testing Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Testing Intake Router

Agent routes testing requests to one primary testing skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for test analysis or test remediation and the exact concern is unclear | Use this skill |
| The request maps to bundle, anti-pattern, gap, assertion, or smell analysis | Use this skill |
| User asks which testing skill handles the work | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| User already asked for one specific testing specialist | Use that specialist |
| User is creating tests or running tests rather than analyzing them | Use authoring or execution tooling directly |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad testing analysis routing belongs here |
| Bundle use | Bundle stays mixed-concern or alias-only |
| Specialist loading | One specialist first unless the request explicitly spans multiple analysis modes |
| Execution split | Test execution and test authoring remain outside analysis routing |

## Verification

- [ ] Agent chose one primary testing skill
- [ ] Agent used bundle only as an alias or mixed-entry surface
- [ ] Agent avoided loading multiple test-analysis peers for one narrow concern

## Routing Table

| Intent | Primary skill | Optional secondary |
|---|---|---|
| Mixed test quality or remediation request | `test-fixes` | none |
| Unsure / alias entry for test analysis | `test-fixes-bundle` | none |
| Anti-pattern audit | `test-anti-patterns` | none |
| Missing cases or escaped defects | `test-gap-analysis` | none |
| Assertion quality or depth | `assertion-quality` | none |
| Academic smell review | `test-smell-detection` | none |
