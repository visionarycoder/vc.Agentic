---
name: "performance-load-testing"
description: "Write load, stress, and soak tests that verify non-functional thresholds, and benchmark hot paths with evidence."
metadata:
  metadata-version: "1.0.0"
  title: "Performance and Load Testing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Performance and Load Testing

Load this skill when `chaos-tester` writes tests in `tests/performance/**`. Load `microbenchmarking` for hot-path benchmarks and `dotnet-performance-standards` for code-level guidance.

## When to use

Use a performance test only for a non-functional requirement that states a measurable threshold (latency percentile, throughput, batch window, memory ceiling). Never optimize without evidence that a threshold fails.

## Procedure

1. Copy the threshold, workload, and data volume from the test specification. A missing number returns the requirement to `product-owner`.
2. Choose the test type.

   | Type | Question | Shape |
   |---|---|---|
   | Load | Does the system meet the threshold at expected volume? | Steady expected volume |
   | Stress | Where does it break, and how? | Ramp past expected volume |
   | Soak | Does it degrade over time (leaks, pool exhaustion)? | Expected volume for hours |

3. Build the workload from `tests/data/` with production-shaped volume and distribution, using synthetic or anonymized data.
4. Run in the isolated performance environment on fixed hardware sizing. Record the build, configuration, data set, and environment with every result.
5. Warm up first. Discard warm-up samples.
6. Collect percentiles (p50, p95, p99), throughput, error rate, and resource use (CPU, memory, connections, database waits). Use OpenTelemetry metrics from the system under test.
7. Assert against the threshold. Report the measured value next to the threshold.
8. For a hot path, add a BenchmarkDotNet benchmark under `tests/performance/benchmarks/` and compare against a stored baseline.

## Rules

- Never run load tests against shared or production environments.
- Compare results only across identical environment and data set.
- Report a failed threshold with the root cause evidence (trace, query plan, or profile) and two alternatives with cost and effort. Do not apply a fix.
- Keep results as artifacts in the pipeline run for trend comparison.
