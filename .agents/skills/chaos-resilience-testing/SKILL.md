---
name: "chaos-resilience-testing"
description: "Write system-level fault-injection tests that verify degradation and recovery against stated hypotheses."
metadata:
  metadata-version: "1.0.0"
  title: "Chaos and Resilience Testing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Chaos and Resilience Testing

Load this skill when `chaos-tester` writes tests in `tests/chaos/**`. Also load `dotnet-resilience-standards`.

## When to use

Use a chaos test for a resilience requirement the detailed design states: timeouts, retries, circuit breakers, idempotency, queued Manager calls, and restart recovery. Unit-level fault injection belongs to the developer's unit tests.

## Procedure

1. Write a hypothesis for each test: `When <fault> occurs during <flow>, the system <expected behavior> within <threshold>.`
2. Choose the failure class and the injector from `tests/common/Faults/`.

   | Class | Injection |
   |---|---|
   | Dependency outage | Stop the container or return connection errors |
   | Latency | Delay responses beyond the timeout |
   | Partial failure | Fail one call in a multi-call flow |
   | Duplicate or out-of-order delivery | Replay or reorder queued messages |
   | Resource pressure | Exhaust the connection pool or return throttling responses |
   | Restart | Stop the host mid-operation and restart it |

3. Establish the steady state first: run the flow without the fault and record the baseline.
4. Inject the fault, run the flow, and observe. Never inject outside the test's own isolated environment.
5. Remove the fault. Assert recovery: the flow succeeds again within the threshold and no state is lost or duplicated.
6. Assert degradation: the caller receives the specified error (Problem Details, retry-after, or queued acknowledgement) and not a hang or an unhandled exception.
7. Assert data integrity: no partial writes, no duplicate postings, and balances still reconcile for financial flows.
8. Record fault, observed behavior, and thresholds in the test output so the traceability report cites them.

## Rules

- Make every fault reversible and every test self-cleaning, including after a failed assertion.
- Never inject faults into shared or production environments.
- A test with no stated threshold is invalid. Return it to `test-architect`.
- Run with cancellation tokens and a hard test timeout so a hung system fails the test.
