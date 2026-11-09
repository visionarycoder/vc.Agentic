---
name: "microbenchmarking"
description: "Design, run, and review BenchmarkDotNet microbenchmarks with explicit comparison scope, controlled case count, and measured correctness checks."
metadata:
  metadata-version: "1.0.0"
  title: "Microbenchmarking"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Microbenchmarking

Use for BenchmarkDotNet comparisons of .NET implementations, runtimes, configurations, and representative input sizes. Use a profiler for production diagnosis and a load-test workflow for system throughput.

1. Record the question, baseline, correctness criteria, inputs, runtime, and run budget.
2. Read [benchmark authoring](references/writing-benchmarks.md) and [comparison design](references/comparison-strategies.md). Estimate parameter combinations times jobs before running.
3. Keep preparation in setup methods. Return or consume results so the JIT cannot remove the operation. Check candidate behavior outside measured methods.
4. Follow [project setup](references/project-setup-and-running.md). Run Release builds without an attached debugger. Dry and Short jobs check execution; they do not establish a performance conclusion.
5. Read [execution and tuning](references/bdn-internals-and-tuning.md) before changing jobs or iteration settings. Preserve approved SDK and package versions.
6. Add [diagnosers and exporters](references/diagnosers-and-exporters.md) only for the question under investigation; disclose their overhead and platform support.
7. Report baseline ratios, uncertainty, relevant allocations, environment, input scope, and artifact paths. Limit conclusions to measured environments.

The tuning reference is bundled here. See official [BenchmarkDotNet good practices](https://benchmarkdotnet.org/articles/guides/good-practices.html) for measurement mechanics; repository requirements govern project changes.
