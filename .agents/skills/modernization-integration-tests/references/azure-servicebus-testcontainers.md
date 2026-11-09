---
metadata-version: "1.0.0"
title: "Azure Service Bus emulator tests"
description: "Configure Java application tests against a local Service Bus emulator."
document-type: "index"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Azure Service Bus emulator tests

Use for Layer 1 tests of the application's Service Bus adapter or service. Keep local connection strings and credentials out of production configuration.

1. Inspect approved Testcontainers and Azure SDK versions. The [Testcontainers Java Azure module](https://java.testcontainers.org/modules/azure/) documents `ServiceBusEmulatorContainer` and its SQL Server dependency. Use compatible APIs without silently upgrading the project.
2. Pin compatible emulator and SQL Server images under the dependency policy. Check support and existing license authorization. Use a private Docker network, test-only credentials, and dynamically mapped host ports.
3. Put a version-compatible emulator configuration under `src/test/resources`, declaring the queues/topics/subscriptions the application uses. Wire the SQL dependency and emulator using documented module APIs. Wait for initialization, not just an open port.
4. For host-run Java tests, obtain the connection string from the container API. Containerized applications use private-network aliases rather than host loopback. Inject values through an existing test configuration or DI seam.
5. Invoke application operations and assert payload mapping, identity, settlement, error handling, and downstream results where relevant. Use bounded asynchronous waits and unique entities or isolated containers.
6. Close clients and containers on success and failure. Report unsupported emulator features separately; verify them only in an explicitly assigned Layer 3 environment.

Use [Microsoft's emulator configuration and health-check guidance](https://learn.microsoft.com/en-us/azure/service-bus-messaging/test-locally-with-service-bus-emulator) for the selected image. Do not assume a timeless configuration schema.

Record image digests/tags, library versions, configuration path, application entrypoint, readiness, assertions, test count, and results. A local pass does not prove production identity, networking, or every cloud feature.
