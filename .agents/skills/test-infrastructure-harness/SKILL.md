---
name: "test-infrastructure-harness"
description: "Build the shared test harness, fixtures, fakes, builders, disposable resources, and synthetic data that every test tier consumes."
metadata:
  metadata-version: "1.0.0"
  title: "Test Infrastructure Harness"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Test Infrastructure Harness

Load this skill when `test-architect` builds or changes anything under `tests/common/**` or `tests/data/**`.

## Layout

| Path | Content |
|---|---|
| `tests/common/Harness/` | Base classes, host and service-provider builders, configuration loaders |
| `tests/common/Fixtures/` | Assembly- and class-scoped fixtures for databases, storage emulators, and message brokers |
| `tests/common/Builders/` | Test data builders that create valid domain objects with overrides |
| `tests/common/Faults/` | Fault-injection helpers used by chaos tests (latency, error, drop, duplicate) |
| `tests/data/` | Synthetic and anonymized data sets, seed scripts, expected-output files |

Name projects `*.TestCommon` and `*.TestData`. Test projects reference them. Production projects never do.

## Rules

1. **Disposable.** Every fixture creates its own resources and removes them on dispose. Use a unique name per run (run ID or GUID suffix) so parallel runs never collide.
2. **Real resource first.** Prefer a container or emulator (SQL Server container, Azurite, Service Bus emulator) over a mock for Access-layer tests. Use a fake only for systems with no local emulator.
3. **Configuration, not files.** Read connection details from configuration or environment variables. Never write secrets, tokens, or connection strings into the repository.
4. **Deterministic.** Inject a clock (`TimeProvider`), a random seed, and a GUID source. Tests never read the wall clock or generate unseeded randomness.
5. **Synthetic data.** Build data with builders or generate it. Anonymize any sample taken from a real source and remove Category 3 and 4 data before it enters `tests/data/`.
6. **Seed once, isolate per test.** Seed reference data at fixture scope. Wrap test-specific changes in a transaction or a per-test schema and roll back.
7. **One way to do each thing.** Tier authors never copy harness code. A missing capability returns to `test-architect` as a request.
8. **Pipeline-ready.** Every fixture runs on the build agent without manual setup. Document any prerequisite in `tests/common/README.md` and in the pipeline template through the `devops` layer.

## Verification

1. Write one smoke test per fixture that creates the resource, uses it, and disposes it.
2. Run the smoke tests twice in parallel. Pass criteria: no collisions and no leftover resources.
3. Run them in the pipeline. Pass criteria: green with no manual step.

## Change Control

A change to a harness API is a contract change for every tier author. Announce it through `scribe` and update dependent tests in the same work item.
