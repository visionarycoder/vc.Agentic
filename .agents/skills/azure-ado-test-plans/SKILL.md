---
name: "azure-ado-test-plans"
description: "Create Azure DevOps Test Plans, requirement suites, Test Cases, test points, and test runs for a Feature and its User Stories."
metadata:
  metadata-version: "1.0.0"
  title: "ADO Test Plans"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "azure"
---

# ADO Test Plans

## When to use

Use this skill to test a Feature and its User Stories in Azure Test Plans.
Read [API map](references/api-map.md) before the first test call.
Do not edit application code.

## Objects

| Object | Rule |
| --- | --- |
| Test Plan | One per Feature. Name: `<Feature ID> <Feature title>`. Copy area and iteration from the Feature. |
| Suite | One requirement suite per User Story under the plan root. `suiteType` is `requirementTestSuite`. `requirementId` is the User Story ID. |
| Test Case | One case per `AC-*`. Title: `<Story ID> <AC-id>`. |
| Link | The case tests the User Story. Confirm the `Tests` relation name before the write. |
| Test point | Use the point ID returned when the case is added to the suite. |
| Test run | One run for the points in this pass. Record each point as `Passed` or `Failed`. |

Do not create a query suite or a static suite for this workflow.
Do not create a second plan for the same Feature ID.

## Procedure

1. Read the Feature, its User Stories, and each story's acceptance criteria.
2. List plans. Reuse the plan whose name starts with the Feature ID.
3. Create the plan when no match exists. Read `rootSuite.id` from the saved plan.
4. List suites. Reuse the requirement suite whose `requirementId` is the User Story ID.
5. Create the missing requirement suite under the root suite.
6. Search for a Test Case with the story ID and `AC-*` in the title. Reuse it on a match.
7. Create the missing Test Case. Write steps in `Microsoft.VSTS.TCM.Steps` with the XML shape in the API map.
8. Link the case to the User Story with the `Tests` relation.
9. Add the case to the requirement suite. Record each returned point ID.
10. Create a run with the plan ID and the point IDs for this pass.
11. Execute each point. Add a result with that point ID and outcome `Passed` or `Failed`.
12. On `Failed`, create one Bug under the User Story, then link that Bug on the result.
13. Set the run state to `Completed`. Read the saved run.
14. Return plan ID, suite IDs, case IDs, run ID, point outcomes, and Bug IDs.

## Bug from a failed point

The Bug parent is the User Story that owns the `AC-*`.
Store the run ID, point ID, `AC-*`, expected result, and actual result in the Bug description.
Do not open a second Bug for the same open point and `AC-*`.

## Stop

Stop and return `Publication: Blocked (Integration unavailable)` when no authenticated test integration exists.
Do not invent a plan, suite, case, point, or run ID.
A story with no acceptance criteria has no Test Case. Return that gap and do not create an empty case.
