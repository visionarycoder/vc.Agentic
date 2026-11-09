---
name: "test-strategy-design"
description: "Allocate requirements to test tiers, assign stable IDs, write the test specification, and report traceability gaps."
metadata:
  metadata-version: "1.0.0"
  title: "Test Strategy Design"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Test Strategy Design

Load this skill when `test-architect` plans tests for a feature.

## Tier Model

| Tier | Scope | Speed | Environment |
|---|---|---|---|
| Unit | One component, dependencies at named boundaries only | Milliseconds | None |
| Integration | Several components with real resources | Seconds | Disposable database or emulator |
| Contract | One boundary between two parties | Seconds | None or emulator |
| Acceptance | One acceptance criterion end to end | Seconds to minutes | QA-like environment |
| Chaos | Fault injection against a running flow | Minutes | Isolated test environment |
| Performance | Load against a non-functional threshold | Minutes | Isolated, production-like |

Place a test at the lowest tier that can fail for the right reason. Use a higher tier only when the lower tier cannot observe the behavior.

## Procedure

1. List every requirement and acceptance criterion. Give each a stable ID (`FR-<feature>-<n>`, `NFR-<feature>-<n>`, `AC-<feature>-<n>`). Never reuse an ID.
2. Reject any criterion that has no observable pass condition. Return it to `product-owner` with a suggested rewrite.
3. Allocate each ID to one primary tier and record the reason. Add a second tier only for risk, such as a security or financial-control requirement.
4. Write the test specification per feature using the table below.
5. Identify infrastructure needs: databases, emulators, fakes, data sets, secrets, and environments. Send them to the `test-infrastructure-harness` work.
6. Publish the plan and suites through the `azure-ado-test-plans` skill by way of `scribe`.
7. Before Gate 4, build the traceability report.

## Specification Row

| Field | Content |
|---|---|
| ID | Requirement or criterion ID |
| Tier and author | Tier and the agent that writes it |
| Given / When / Then | Preconditions, action, observable result |
| Data | Data set name from `tests/data/**` |
| Environment | Environment and fakes needed |
| Threshold | Numeric target for performance or resilience tests, else `none` |

## Traceability Report

| Requirement ID | Test IDs | Latest result | Gap |
|---|---|---|---|

A row with no test ID is a gap and blocks Gate 4. A row whose latest result is missing is also a gap.

## Anti-Patterns

- The same behavior verified in every tier.
- Acceptance tests that re-test unit logic through the UI.
- Performance tests with no threshold.
- Tests that depend on the order of other tests.
