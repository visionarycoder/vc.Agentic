---
name: "ui-acceptance-testing"
description: "Verify approved user-visible acceptance criteria through browser or desktop UI scenarios with traceable evidence; excludes general service/API acceptance testing."
metadata:
  metadata-version: "1.0.0"
  title: "UI acceptance testing"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# UI acceptance testing

Use for criteria whose behavior must be observed through a web or desktop user interface. Use service/API test guidance for criteria observable entirely at that boundary. A browser smoke check is preliminary evidence, not completion of a UI acceptance plan.

## Inputs

Read the assigned criterion IDs, approved scenarios, target revision and environment, test plan, client technology, and permitted test identities. Preserve the target repository's test layout and reporting conventions. Use its approved UI harness rather than selecting a new stack.

## Procedure

1. Map each criterion outcome to an independent UI scenario covering success, stated rejection rules, and boundaries. Keep criterion IDs in names and reports.
2. Prepare deterministic data using supported builders or seed utilities. Do not depend on another scenario's residue. Use configured test identities and keep credentials out of source and evidence.
3. Drive the visible journey through the approved browser or desktop harness. Use accessible roles, labels, or stable test IDs. Refresh targets when the UI changes; avoid positional or generated selectors.
4. Assert the displayed outcome and business state exposed through approved observations. An internal record or successful HTTP response alone does not prove a UI requirement.
5. For accessibility criteria, run configured automated checks and identify the manual observations still required. Automated checks do not establish complete accessibility conformance.
6. Capture failures, useful screenshots or traces, and cleanup results. Do not weaken assertions or modify application behavior to make a test pass. Keep scenarios independent and self-cleaning.
7. Link results to the project's criterion/test-case records. Use Azure DevOps Test Plans only when configured and available. File or send external defects only when authorized.

Report criterion coverage, scenario outcomes, revision/environment, evidence, and unexecuted or blocked checks. Product Owner acceptance and the project's approval routes remain separate decisions.

## Related skills and provenance

Use agent-browser automation (`../agent-browser-automation/SKILL.md`, external skill not bundled) for an assigned CLI task, or Copilot Browser session for that plugin. Neither replaces the approved test plan.

## Project and host prerequisites

References labeled as consuming-project or host files are not bundled assets. Resolve them in the assigned project or connected host and verify them before a dependent step. If required context is absent, report it and limit the work to a supported draft. Optional external skills are not installed by this library; use an available authorized capability or identify the unmet prerequisite. Do not recreate owner-deleted skills.
