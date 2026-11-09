---
metadata-version: "1.0.0"
title: "vc.Agentic"
description: "Define the reusable agent working kit and its repository boundaries."
document-type: "index"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# vc.Agentic

Agentic work pursues an assigned goal by selecting actions, using tools, checking results, and adjusting within authorized boundaries. An agent's ability to act does not grant decision or approval authority.

vc.Agentic provides reusable skills, supporting templates, component initialization samples, and skill verification guidance. It supports planning, design, construction, testing, and review. These resources assist work in consuming repositories; they do not define a competing governance framework.

## Repository boundaries

| Repository | Owns |
| --- | --- |
| vc.Governance | Method rules, role authority, lifecycle gates, required constraints, and authoritative artifact contracts and templates |
| vc.Agentic | Shared task skills, supporting work templates, illustrative component skeletons, examples, and skill behavior checks |
| vc.Ifx | Production libraries, generators, analyzers, code fixes, proxies, interception infrastructure, and their executable tests |
| Consuming application | Application requirements, accepted designs, contracts, business code, project-specific instructions, and execution evidence |

The established Governance/Ifx boundary is documented in [repository ownership](../vc.Governance/docs/implementation/repository-ownership.md). This setup records the user's assignment for Agentic resources; it does not reassign existing Governance or Ifx responsibilities.

Keep repository-specific skills beside their repository. Governance's documentation skills remain there. Put reusable skills here when they can serve multiple consuming repositories. Link governing rules instead of copying them. Production code generation belongs in Ifx; an illustrative code template used by an agent belongs here.

## Starting catalog

| Resource | Purpose |
| --- | --- |
| [Shared skills](.agents/README.md) | Select a focused task skill |
| [Prepare component initialization](.agents/skills/prepare-component-initialization/SKILL.md) | Adapt the component skeleton to an assigned design |
| [Prepare task handoff](.agents/skills/prepare-task-handoff/SKILL.md) | Summarize inputs, outputs, evidence, and unresolved work |
| [Supporting templates](templates/README.md) | Task brief, handoff, and component initialization starting points |
| [Component samples](samples/components/README.md) | Manager, Engine, and Access interface/class examples |
| [Skill verification](verification/README.md) | Check behavior and boundaries using realistic scenarios |

## Use and contribution

Read the consuming repository's instructions and current assignment before applying a resource. Skill discovery depends on the client; these files are not globally installed by their presence here. If discovery is unavailable, read the linked SKILL.md directly.

Keep each skill focused on one task. Store substantial references or assets beside the skill only when needed. Reuse catalog templates rather than maintaining copies. New skills should identify their inputs, output, applicable authority, and what to do when required information is missing.

Update document metadata when editing. Skill entrypoints use name and description metadata; other Markdown uses the document header illustrated here. Verify relative links and skill metadata after changes. Skill behavior checks do not authenticate approvals or establish independent review.

Component samples are source illustrations, not a runnable application, generated proxy, approved detailed design, or delivered Ifx capability. No SDK, application technology baseline, or deployment is selected by this repository.
