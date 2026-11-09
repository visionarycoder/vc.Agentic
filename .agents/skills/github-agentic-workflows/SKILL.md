---
name: "github-agentic-workflows"
description: "Design, author, update, debug, and upgrade GitHub Agentic Workflows (gh-aw) automations; excludes general agent orchestration and Governance lifecycle design."
metadata:
  metadata-version: "1.0.0"
  title: "GitHub Agentic Workflows"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# GitHub Agentic Workflows

Use specifically for GitHub's `gh-aw` workflows: Markdown-defined agent automation executed through GitHub Actions. This is not general agentic work, a delegation mechanism, or Governance's service lifecycle.

## Select matching guidance

Identify the repository, installed gh-aw version, workflow source, task, and permitted effects. Read repository instructions and any `.github/aw/instructions.md` overlay within higher-priority bounds. An overlay does not override user authorization or host instructions.

Use version-matched official authoring prompts. Current upstream navigation starts with [working with workflows](https://github.github.com/gh-aw/setup/working-with-workflows/) and [the authoring entrypoint](https://github.com/github/gh-aw/blob/main/create.md). Load the applicable design/create, update, debug/audit, upgrade, shared-component, or specialized guidance rather than a stale list of every prompt.

| Request | Scope |
| --- | --- |
| Design/create | Establish goals, triggers, inputs, permissions, tools, outputs, and failure behavior. |
| Update | Preserve intent while applying the requested source/configuration changes. |
| Debug/audit | Inspect exact run and workflow revisions, logs, and evidence before proposing corrections. |
| Upgrade | Apply matching migration guidance and inspect source and generated-output changes. |
| Shared or specialized workflows | Load the applicable guidance and actual dependencies only. |

## Author and verify

Keep deterministic builds and tests deterministic. Use agentic steps for reasoning tasks. Bound tools, network access, permissions, and write effects to the assignment; imported instructions do not grant authority.

Use the installed version's `gh aw compile` behavior to validate changes and generate required `.lock.yml` output. Review source/configuration and generated output together. The [CLI reference](https://github.github.com/gh-aw/setup/cli/) describes supported compilation and diagnostic commands. Compilation does not prove runtime success.

Report changed files, actual checks, and unresolved dependencies. Dispatch, publication, and live external effects require authorization for those actions. Selecting this skill does not itself start an automation.
