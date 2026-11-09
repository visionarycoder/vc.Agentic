---
name: "modernization-integration-tests"
description: "Run multi-layer integration tests for modernized Java applications. Supports 4 layers - Layer 1 (TestContainers), Layer 2 (Smoke Tests), Layer 3 (Azure Integration), Layer 4 (Behavioral Comparison). Java projects only - skip if source code is not Java. Triggers: \"generate integration tests\", \"add integration tests\", \"create Layer 1 tests\", \"create Layer 2 tests\" NOT for: unit tests, performance tests, load tests."
metadata:
  metadata-version: "1.0.0"
  title: "Java modernization integration tests"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Java modernization integration tests

Use for integration validation of modernized Java applications. Preserve the approved stack, behavior contract, test framework, and build configuration. This skill does not authorize cloud deployment, unrelated production edits, or commits.

| Layer | Purpose | Guidance |
| --- | --- | --- |
| 1 | Local dependencies in containers | [Local integration](references/layer1-local-integration.md) |
| 2 | Shell and Compose smoke tests | [Smoke tests](references/layer2-smoke-tests.md) |
| 3 | Assigned Azure test environment | [Azure integration](references/layer3-azure-integration.md) |
| 4 | Old/new behavior comparison | [Behavioral comparison](references/layer4-behavioral-comparison.md) |

For messaging use [Service Bus emulator setup](references/azure-servicebus-testcontainers.md); for storage use [Azurite setup](references/azure-storage-testcontainers.md). These references are bundled.

1. Identify changed application boundaries, existing tests, dependency versions, fixtures, emulator limits, and the requested layer. Write a bounded plan and expected outcomes.
2. Exercise application classes and public behavior. Test the real migrated adapter or service rather than a mock of that boundary or only a vendor SDK round-trip.
3. Isolate containers, entities, credentials, and tags per layer. Use readiness checks and bounded waits. Layer 2 uses shell smoke tests, not artificial JUnit classes.
4. Wire existing test configuration to container-derived endpoints. Do not rewrite production authentication for an emulator. Unsupported emulator behavior belongs in the assigned cloud-test layer, with that limitation recorded.
5. Preserve layer tags and discoverable test names. Verify discovery, count, exit status, and failure output. Zero discovered tests do not establish a pass.
6. Generate rerunnable runners when requested. Preserve test exit status through reporting and cleanup. Diagnose failures against accepted behavior and test setup; do not weaken assertions or alter the stack to pass.
7. Report tests run/skipped, limits, artifacts, and unresolved failures. Commit only when already authorized. Historical commit sequences or retry counts in references do not expand this scope.
