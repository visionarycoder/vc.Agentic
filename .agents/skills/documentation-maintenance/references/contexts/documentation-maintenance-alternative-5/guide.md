---
metadata-version: "1.0.0"
title: "Documentation Maintenance"
description: "Preserve scoped source guidance for documentation-maintenance."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Documentation Maintenance

Docs in this repo are a first-class deliverable, not an afterthought. A change
is "done" only when the code **and** its documentation land together. This
skill defines what documentation is required, where it lives, and how to keep
it in sync.

> **Golden rule:** If you add, change, or delete code, assume something in
> `/docs/**`, an XML/JSDoc comment, a README, or a runbook needs to move with
> it. Treat the doc search as part of the change.

## When to Use This Skill

Use this skill **on every code change**, including:

- Adding a new feature, endpoint, component, service, job, interface, or schema
- Changing public API shape (routes, DTOs, scopes, config keys, feature flags,
  environment variables, SQL objects)
- Changing authentication, authorization, or security posture
- Adding or changing operational behavior (logging, retries, scheduled jobs,
  background workers, connection targets)
- Deleting a feature or endpoint
- Refactoring that renames, moves, or splits a type/file that is referenced by
  name in any doc
- Updating a dependency version that is called out in docs

If the PR only updates tests that don't change observable behavior, docs may be
unchanged — but still check (test patterns in skill docs count).

## Documentation Surfaces

Know where each kind of doc lives; update the correct surface(s).

| Surface | Location | Use for |
| --- | --- | --- |
| Copilot repository instructions | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` | Instructions Visual Studio Copilot discovers automatically. |
| Copilot agent skills | `.github/skills/<skill-name>/SKILL.md` | Agent skill files Visual Studio Copilot discovers automatically. |
| Copilot prompts | `.github/prompts/*.prompt.md` | Reusable prompt files Visual Studio Copilot discovers automatically. |
| Repo guidance | `docs/instructions/**` | Coding standards, per-project conventions, refactor plans, PR rules, and reports. |
| Mirrored skill guidance | `docs/instructions/skills/<skill-name>/SKILL.md` | Optional user-requested mirror of agent skills; do not maintain long-term mirrors by default, and keep any requested mirror synchronized with `.github/skills/**` while it exists. |
| Ops / runbooks | `docs/ops/**` | Release checklists, feature-flag matrices, on-call procedures, smoke tests. |
| Architecture | `docs/architecture/**`, `docs/adr/**` | System diagrams and ADRs. Add an ADR for non-trivial design decisions. |
| Migration / upgrade | `docs/migration/**`, `docs/instructions/upgrades/**` | One-time transitions (framework upgrades, schema migrations). |
| Quick reference | `docs/ref/**`, `docs/start-here/**` | Onboarding docs. |
| Package / project README | `README.md`, `<project>/README.md` | High-level purpose, how to build/run locally. |
| API code comments | `///` XML doc comments on C# public types/members; JSDoc on exported TS symbols | Generated reference + IntelliSense. |
| Swagger / OpenAPI | Driven from `///` + `[ProducesResponseType]` attributes on controllers | External API contract. |
| Changelog (if present) | `CHANGELOG.md` | User-visible changes. |

All new long-form guidance content must go under `/docs/instructions/**` or
another existing `/docs/**` subfolder. Copilot-discovered assets are the
exception: repository instructions belong in `.github/copilot-instructions.md`
or `.github/instructions/*.instructions.md`, agent skills belong in
`.github/skills/<skill-name>/SKILL.md`, and reusable prompts belong in
`.github/prompts/*.prompt.md`.

## Required Patterns

### 0. Research report and action plan workflow

When a user asks for a plan, migration, refactor, modernization, cleanup, or
other non-trivial change, produce documentation artifacts before changing or
adding code unless the user explicitly asks to implement immediately.

1. Create a findings report under `docs/instructions/reports/**` after
   researching the request.
   - Summarize the current state, relevant files, risks, assumptions,
     unanswered questions, and recommended direction.
   - Call out any decision points that need user confirmation.
   - Prefer evidence from repository files over assumptions.
2. Create an implementation plan under `docs/instructions/plans/**` that pairs
   with the report.
   - Start with a short goal statement and link to the companion report.
   - Break the work into small, PR-sized slices or phases.
   - Inside each slice, use detailed checklist items that are concrete enough
     to execute and review.
   - Include validation requirements for each slice, such as build, focused
     tests, full tests, documentation scans, or deployment checks.
   - Include a legend for status markers: `[ ]` not started, `[~]` in progress,
     `[x]` done.
3. Pause after presenting the report and plan when the user has not explicitly
   requested immediate implementation.
   - Let the user answer questions, correct misinterpretations, adjust scope,
     or approve the direction before code changes begin.
   - For small documentation-only changes, still prefer a brief findings note
     plus checklist plan when a plan is requested.
4. Update checklist statuses as work proceeds.
   - Mark items `[~]` before or while actively working them.
   - Mark items `[x]` after the change and its validation are complete.
   - Leave unfinished or deferred items as `[ ]` and explain why in the final
     response or plan notes.

preferred structure example for detailed, progress-trackable plans.

### 1. New feature or endpoint

When adding a new controller action, Angular component, service, job, etc.:

- C# public types/members: add a `///` XML comment with `<summary>`, each
  `<param>`, `<returns>`, and `<response code="...">` for controllers. Match
  the style of existing controllers (see `JobsController`, `AdminController`).
- TypeScript exported symbols: add a JSDoc block explaining purpose and any
  non-obvious side effects (HTTP calls, storage writes, polling).
- If the feature is gated by a feature flag, scope, role, or config key,
  update **every** table/matrix that lists those:
  - `docs/ops/production-feature-flags.md` (flag matrix)
  - Relevant skill doc (e.g. `webapp-frontend-security/SKILL.md` storage or
    scope tables)
  - `appsettings*.json` comments where the key first appears
- If it introduces a new agent-facing concept, decide whether it belongs in
  an existing skill or warrants a new `SKILL.md`.

### 2. Changing behavior

- Update every doc location that *asserts* the old behavior. Search the repo
  for the old value (route, flag name, scope string, enum case, class name)
  before you rename.
- For controllers whose auth posture changed, update the auth column of the
  flag matrix in `docs/ops/production-feature-flags.md` in the same commit.
- For anything that changes an ADR's "Decision" or "Consequences", append an
  amendment block to the ADR or supersede it with a new one — do not silently
  edit history.

### 3. Deletions

- Remove docs that describe the deleted code in the **same commit**. A stale
  reference is worse than no reference.
- If the deletion is security- or ops-relevant, add a brief note to the
  relevant skill's "Anti-Patterns" section so the pattern isn't reintroduced
  (example: the `AuthService` removal is preserved in
  `webapp-frontend-security/SKILL.md`).
- Grep for the deleted symbol across `docs/**`, `README*.md`, and the
  instruction skills. Every hit should be resolved.

### 4. Skills and instruction files

- Copilot-discovered skill files (`.github/skills/<name>/SKILL.md`) must start
  with the YAML frontmatter: `name`, `description`, `appliesTo` (glob).
- Do not create or keep mirrored skill files under
  `docs/instructions/skills/<name>/SKILL.md` unless the user specifically asks
  for a mirror. If a requested mirror exists, update it in the same change as
  the matching `.github/skills/<name>/SKILL.md` file.
- Copilot-discovered targeted instruction files must live in
  `.github/instructions/*.instructions.md` and use `applyTo` frontmatter.
- Keep "Required Patterns" concrete with short code examples that compile.
- Keep a "Pull Request Checklist" the author can literally tick.
- Keep an "Anti-Patterns" section so deleted/bad patterns are preserved.
- Whenever a skill's reference files are renamed or moved, update the
  "Reference Files" table in that skill.

### 5. Cross-references

When a doc references code by path or symbol:

- Use repo-relative paths from the repo root (e.g.
  `AzureAPI/src/Client.Portal.WebApi/Controllers/V1/JobsController.cs`).
- Prefer linking to a **folder** or a **stable symbol name** over a line
  number; line numbers rot.
- If you must call out a specific constant (scope string, flag key), write it
  verbatim in backticks and treat it as a contract: the next person renaming
  it is responsible for grepping and updating.

### 6. Ops / runbooks

Any change to:

- Feature flags, App Configuration keys, Key Vault secret names
- Required roles, scopes, app-role assignments
- External dependencies (SFTP hosts, downstream DBs, email service)
- Scheduled job groups, cron cadence, retention windows

…requires a matching update to `docs/ops/**` (create the doc if none exists)
so the release lead / on-call engineer has a current reference.

### 7. Build and run docs

- Every `.csproj` / `package.json` / deployable project should ultimately be
  reachable from a README that states: what it is, how to build, how to run
  locally, how to test. When adding a new project, add or extend a README.
- When build commands change (e.g. new `dotnet` TFM, new `npm` script), update
  those READMEs plus any onboarding doc under `docs/start-here/**`.

## Pull Request Checklist

Tick every box that applies to your change.

- [ ] Every new public C# type/member has `///` XML doc comments
- [ ] Every new exported TS symbol has a JSDoc block
- [ ] New controller actions have `[ProducesResponseType]` entries matching
      the documented `<response>` codes
- [ ] New feature flags / scopes / roles / config keys are added to
      `docs/ops/production-feature-flags.md` (or the equivalent matrix)
- [ ] Changed auth posture is reflected in the same flag matrix in the same
      commit
- [ ] Every relevant Copilot skill under `.github/skills/**` is updated
      (new storage keys, new scopes, new anti-patterns)
- [ ] No mirrored skill under `docs/instructions/skills/**` was added or kept
      unless the user specifically requested it
- [ ] Any user-requested mirrored skill under `docs/instructions/skills/**` is
      synchronized with the matching `.github/skills/**` skill
- [ ] Requested plans have a companion findings report under
      `docs/instructions/reports/**`
- [ ] Requested plans use small checklist-based slices with `[ ]`, `[~]`, and
      `[x]` status markers
- [ ] Renames: old name has zero remaining hits in `docs/**` and `README*.md`
      (`git grep` clean)
- [ ] Deletions: all docs describing the deleted code were removed or
      rewritten in this commit
- [ ] New design decisions of any significance have an ADR under
      `docs/adr/**` (or an amendment to an existing one)
- [ ] New projects have a README covering purpose / build / run / test
- [ ] CHANGELOG (if the repo keeps one) has a user-visible entry
- [ ] Long-form guidance stayed under `docs/**`; Copilot-discovered assets
      stayed under the supported `.github/**` locations
- [ ] Links in touched docs still resolve; code snippets in docs still compile
      or run

## Anti-Patterns (Do Not Do)

- Shipping code in one commit and "docs to follow". They follow in the same
  PR or they don't follow at all.
- Renaming a scope / flag / class without grepping `docs/**` for the old
  string.
- Moving Copilot-discovered assets out of `.github/copilot-instructions.md`,
  `.github/instructions/**`, `.github/skills/**`, or `.github/prompts/**`.
- Maintaining duplicate skill mirrors under `docs/instructions/skills/**` unless
  the user specifically requested the mirror.
- Placing long-form guidance content in a loose root file or unrelated folder;
  it belongs in `docs/instructions/**` or another existing `docs/**` area.
- Starting non-trivial implementation immediately after research when the user
  asked for a plan but did not explicitly approve code changes.
- Writing vague plans without PR-sized slices, detailed checklist items, or
  status markers that can be updated as work proceeds.
- Editing an ADR's "Decision" to reflect a new choice. ADRs are immutable;
  supersede them instead.
- Leaving dead references to deleted types, endpoints, or config keys.
- Deferring XML / JSDoc comments "until the API stabilizes". Write them with
  the code; they are cheaper now than later.
- Copy-pasting doc tables instead of linking to the canonical one, which
  guarantees they drift.

## Quick Authoring Commands

```powershell
# Find every doc reference to a name you're about to rename:
Get-ChildItem -Path docs, README*.md, **\*.csproj -Recurse -ErrorAction SilentlyContinue |
  Select-String -Pattern 'OldSymbolName'

# Find docs that reference a file you're about to move:
Select-String -Path (Get-ChildItem docs -Recurse -Include *.md).FullName `
              -Pattern 'AzureAPI/src/Client\.Portal\.WebApi/Controllers/V1/Old\.cs'

# Confirm no stale references remain after the change:
Select-String -Path (Get-ChildItem docs -Recurse -Include *.md).FullName `
              -Pattern 'OldSymbolName'
```

## Reference Files

| Concern | File |
| --- | --- |
| Guidance-location rule | `.github/copilot-instructions.md` |
| Example ops doc | `docs/ops/production-feature-flags.md` |
| Example skill (security) | `.github/skills/webapp-frontend-security/SKILL.md` |
| Example skill (testing) | `.github/skills/mstest-test-authoring/SKILL.md` |
| User-requested mirrored skill guidance | `docs/instructions/skills/**` |
| Coding standard | `docs/instructions/coding-standard.md` |
