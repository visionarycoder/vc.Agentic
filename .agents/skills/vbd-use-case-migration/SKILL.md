---
name: "vbd-use-case-migration"
description: "Build and run a migration harness with routing, shadow execution, tolerance comparison, replay, rollback, and drift monitoring for `UC-*` outcomes."
metadata:
  metadata-version: "1.0.0"
  title: "VBD Use-Case Migration Harness"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "vbd"
---

# VBD Use-Case Migration Harness

Agent builds the harness that proves a migration wave is safe before and after cutover.

## When to Use

Use when a migration wave needs old and new implementations behind one routing decision.
Use when the user needs outcome comparison before live traffic trusts the new path.
Use when captured traffic replay against the new path.
Use when cutover finished and drift still needs observation.

## When Not to Use

Do not use when the prompt asks for wave planning only. Use `vbd-cutover-migration`.
Do not use when no use-case catalog exists. Use `vbd-use-case-reconstruction`.
Do not use when the prompt is only hypothetical impact analysis. Use `vbd-change-simulation`.

## Workflow

| Step | Agent action | Output | Test | Pass |
|---|---|---|---|---|
| 1. Configure routing | Agent writes logical routing states for old, canary, and full cutover. | Routing table | Agent reads the routing table. | Every `UC-*` route has explicit old, canary, and full states. |
| 2. Run shadow mode | Agent routes sampled or full traffic through both paths while old stays authoritative. | Shadow run log | Agent reads shadow results. | Caller-visible results come from old path only. |
| 3. Compare outcomes | Agent applies field rules from the tolerance policy. | Diff log | Agent reads diff log. | Every diff record names `UC-*`, field, expected, actual, and severity. |
| 4. Rehearse replay | Agent replays recorded traffic against the new path after each changed build. | Replay report | Agent reads replay report. | Replayed cases meet tolerance thresholds. |
| 5. Rehearse rollback | Agent routes traffic back to the old path and verifies data authority. | Rollback report | Agent reads rollback report. | Old path resumes service and reconciliation rules pass. |
| 6. Monitor drift | Agent keeps comparison and operational telemetry active through the observation window. | Drift report | Agent reads trend report. | Diff rate, latency, and error thresholds stay inside policy for the full window. |

Test: Run the harness verification suite for the selected wave.
Pass: Diff rate stays at or below policy threshold. Rollback drill passes. Observation window closes with zero unresolved drift.

## Inputs

| Input | Required | Description |
|---|---|---|
| Use-case catalog | Yes | `UC-*` outcomes and acceptance criteria |
| Old and new implementations | Yes | One logical entry point can reach both |
| Tolerance policy | Yes | Exact, normalized, ignore, and numeric-band rules |
| Observation window | Yes | Time and threshold rules for post-cutover drift |

Tolerance rules: business-critical values match exactly; generated identifiers and timestamps are normalized or ignored; numeric results use the stated band; ordering-insensitive collections compare as sets; undocumented new fields are flagged as diffs. Discard new-path side effects before cutover so shadow mode never becomes dual-write.

## Output Contract

| Output | Minimum content |
|---|---|
| Routing packet | Current route per `UC-*` |
| Diff log | Severity, count, trend, and tolerance rule |
| Replay report | Recorded batch, result, and drift summary |
| Rollback report | Route reversal and reconciliation evidence |
| Observation record | `MIG-*` rehearsal record and closeout notes |

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [vbd-use-case-migration-alternative-1](references/contexts/vbd-use-case-migration-alternative-1/guide.md)
