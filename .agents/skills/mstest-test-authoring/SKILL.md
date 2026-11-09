---
name: "mstest-test-authoring"
description: "Create, extend, and modernize MSTest unit tests with repository-aligned isolation, assertions, data-driven cases, and lifecycle handling."
metadata:
  metadata-version: "1.0.0"
  title: "MSTest test authoring"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# MSTest test authoring

Use for new tests, regression coverage after code changes, and improving existing MSTest assertions or lifecycle usage. Use suite-audit skills for an audit without implementation; use the test runner for execution alone.

1. Inspect the target behavior, existing test layout, MSTest package versions, test discovery, and repository naming/DI conventions. Preserve intentionally selected frameworks and versions.
2. Choose cases for expected outcomes, boundaries, errors, cancellation, and relevant dependency failures. Test application behavior rather than merely asserting that mocks were configured.
3. Keep each test deterministic and independently runnable. Use scoped setup/cleanup and test doubles only at appropriate dependency boundaries. Match repository naming and avoid unapproved global state or ordering.
4. Use specific assertions and data-driven patterns supported by the selected MSTest version. Modernize obsolete APIs only within the assigned scope; a test edit does not authorize a framework upgrade.
5. Run the targeted tests through the existing build, confirm discovery and counts, and exercise the intended failure cases. Report skipped tests and environment limits explicitly.
6. Report changed scenarios, relevant gaps, and actual verification results. Do not change acceptance criteria or weaken assertions merely to obtain a pass.

## Detailed guidance

- [Repository unit-test patterns](references/contexts/dotnet-unit-testing/guide.md)
- [MSTest assertions and lifecycle patterns](references/contexts/writing-mstest-tests/guide.md)
- [Examples](references/examples.md)

These references are modes of this single authoring skill. The consuming repository's accepted conventions and selected framework version resolve historical differences.
