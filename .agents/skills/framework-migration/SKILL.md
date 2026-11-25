---
name: "framework-migration"
description: "Replace one application or tooling framework with another while preserving behavior, contracts, build workflows, and validation evidence. Use for full framework replacement, not same-framework version upgrades."
metadata:
  metadata-version: "1.0.0"
  title: "Framework Migration"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-24"
  collection: "optional"
---

# Framework Migration

Migrate the complete project, not a representative slice. Having source and target both working is an acceptable intermediate state, but not a finished migration while the source is still required for behavior, development, CI, or deployment.

## Artifacts

Keep repository-specific evidence in three files under a migration working directory:

- `inventory.md`: source inventory, baseline evidence, source contract values.
- `migration-plan.md`: dependency-ordered items with source evidence, target design, dependencies, validation, and status.
- `completion-report.md`: final parity evidence, contract status, and remaining gaps.

## Contract changes

A contract is any observable property that other code, CI, tooling, or users depend on: minimum runtime version, production dependencies, coverage provider or artifact path, public command names, CI-consumed outputs. Record a contract-changes table in each artifact with: contract, source value, target value, why required, alternatives considered, validation evidence, approval status (`preserved`, `approved change`, `blocked`, `unapproved`).

- Prefer preserving the source contract; change it only when the target genuinely requires it.
- Raising the minimum runtime requires reconciling package metadata, CI, containers, deployment config, docs, and integration tests together, and validating on the new minimum itself. Passing on a newer host does not prove the floor.
- Stable public commands (`start`, `dev`, `build`, `test`) are behavioral contracts. Do not rewrite application startup to accommodate a tooling change. If a retained command breaks on a proposed runtime raise, that is evidence against the raise.
- Replacing a long-running development or watch process is its own contract change. Validate rebuild on edit, error surfacing, and clean exit, not only an initial healthy response.
- Substituting a production dependency needs an immutable source and equivalence evidence, kept separate from the framework swap.
- Changing a coverage provider or artifact path requires searching every CI, badge, quality-gate, and artifact consumer of the old output.
- A successful production build is necessary but not sufficient evidence of dependency equivalence.
- A repository-level consumer of the migrated package (integration test, fixture, container scenario) must be run, or marked `blocked` with the missing capability. Editing a version reference is not validation.
- Do not enter cutover while any material contract change is `unapproved`.

## Decision policy

- Derive answers from source, configuration, CI, and the request before asking the user. Ask only when evidence cannot resolve a product decision with materially different user-visible outcomes.
- Build the target in place, alongside the source, in the same package. Do not clone the repository or copy the package. Create a sibling package only in a monorepo when the two frameworks cannot coexist in one package.
- A full-migration request authorizes continuous execution through the cutover approval gate, not material contract changes discovered mid-migration.
- Use the target framework's official migration guidance for mechanics. If a curated guide for the pair exists, read it first; otherwise say so in the completion report.

## Phase 1: Inventory and baseline

1. Inventory topology, source configuration, the units the framework governs (routes, layouts, components, data pipelines, or specs, mocks, matchers, reporters, coverage), plugins and the behavior each supplies, and development, CI, build, test, and deployment commands.
2. Use exact counts from the repository or generated output, never rough quantities. Reconcile declarations against discovered output and explain differences.
3. Capture a source baseline before the first migration edit, and do not migrate on an unexplained red baseline.

Make the baseline trustworthy:

- Resolve the current supported runtime. The target runtime is the higher of the current floor and what the target requires; a raise is a contract change.
- Repairs needed to run the source (dependency, lockfile, plugin fixes) must not be folded silently into the baseline. Label the state `pristine-baseline`, `source-baseline-blocked`, or `repaired-source-diagnostic`, record the exact tree used, and keep source failures visible.
- Run a read-only dependency preflight before installing: manifest versus lockfile drift, reachability of non-registry sources, and native or lifecycle-script packages. Record a non-reproducible graph as a baseline limitation; never mask it with force or ignore-compatibility flags or an uncommitted lockfile rewrite.
- Classify each failure as a plan or harness defect, an environment blocker, or a genuine project failure. A malformed command or missing executable is a plan defect, not a failing suite.

## Phase 2: Set up the target

1. Record source and target paths in the plan.
2. Add the target's source, configuration, dependencies, and scripts; make only changes the target requires.
3. Preserve framework-independent content, generators, assets, tests, and utilities.
4. Connect shared data pipelines before migrating units that need them.
5. Keep stable command names where practical so baseline validation can be replayed.
6. Keep the source available until equivalent target behavior is proven.
7. Run the target's primary command before proceeding.

## Phase 3: Migrate feature families

A family is a group produced by the same template, data source, configuration, or behavior. Order the plan: shared foundation and configuration, then families, then cross-cutting behavior, then infrastructure cutover and source removal.

For each family: migrate every unit, reuse framework-independent code, re-run validation whose prerequisites are met, open plan items for every regression, and do not proceed while failures are unexplained.

## Phase 4: Restore cross-cutting parity

Check what unit-level migration commonly misses: redirects, aliases, error handling, metadata, localization, generated content, shared setup and teardown, global mocks, coverage thresholds, reporters, environment variables, CI wiring, and build and deploy configuration.

- Treat every difference as a pending plan item and fix it. A difference may remain only with concrete evidence of an external blocker or explicit user approval.
- Rerun validation on the target until every check that passed on the baseline passes.
- Never weaken or delete assertions to make a run pass. Fix the assertion only for a genuine plan defect.

## Phase 5: Approval gate

Enter only when target validation matches the baseline (or differences are approved), no plan item is partial without approved scope change, and no material contract is `unapproved`. The target must run on its own, without source-framework imports or compatibility shims.

Exercise the migrated project locally, give the user exact commands, summarize known differences, and request explicit cutover approval. Keep the source intact during review. A passing target build alone is not approval.

## Phase 6: Cut over

Switch development, CI, and deployment to the target, keeping familiar command names. Remove the source only after:

1. Every family is migrated with no unexplained gaps.
2. Target validation passes.
3. Development and CI use the target.
4. Each plugin behavior has a target implementation or approved removal.
5. Shared code no longer uses source APIs.
6. Shims, aliases, and old commands are unnecessary.

## Phase 7: Final validation

1. Produce a fresh passing validation result recorded after the last migration edit. Stale or partial results do not count.
2. From a clean environment, verify the exact install, build, test, and run commands.
3. Derive the completion report from gates: runtime contract reconciled, baseline state classified, target validation passed, repository-level consumers run or blocked, retained commands validated on the minimum runtime, contract changes approved, source tooling removed. If any gate fails, title the report **Migration incomplete** and list blockers.

Keep changes local. Do not commit, push, publish, or open a pull request unless the user asks.
