---
title: ADO Test Plan API Map
doc_type: reference
status: active
last_updated: 2026-10-09
---

# Test API map

Sources checked 2026-10-09:

- Test Suites, REST 7.1: `https://learn.microsoft.com/en-us/rest/api/azure/devops/testplan/test-suites?view=azure-devops-rest-7.1`
- Suite Test Case - Add, REST 7.1: `https://learn.microsoft.com/en-us/rest/api/azure/devops/testplan/suite-test-case/add?view=azure-devops-rest-7.1`
- Runs - Create, REST 7.1: `https://learn.microsoft.com/en-us/rest/api/azure/devops/test/runs/create?view=azure-devops-rest-7.1`
- Results - Add, REST 7.1: `https://learn.microsoft.com/en-us/rest/api/azure/devops/test/results/add?view=azure-devops-rest-7.1`
- Link types: `https://learn.microsoft.com/en-us/azure/devops/boards/queries/link-type-reference?view=azure-devops`

Write scope: `vso.test_write`.

## Calls

List plans:

`GET https://dev.azure.com/{organization}/{project}/_apis/testplan/plans?api-version=7.1`

Create plan:

`POST https://dev.azure.com/{organization}/{project}/_apis/testplan/plans?api-version=7.1`

Create suite:

`POST https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{planId}/suites?api-version=7.1`

Suite body:

```json
{
  "suiteType": "requirementTestSuite",
  "requirementId": 0,
  "parentSuite": { "id": 0 }
}
```

Add a case to a suite:

`POST https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{planId}/Suites/{suiteId}/TestCase?api-version=7.1`

Body: `[{ "workItem": { "id": 0 } }]`

Create a run:

`POST https://dev.azure.com/{organization}/{project}/_apis/test/runs?api-version=7.1`

```json
{
  "name": "<Feature ID> <run date>",
  "plan": { "id": "0" },
  "pointIds": [0]
}
```

Add results:

`POST https://dev.azure.com/{organization}/{project}/_apis/test/Runs/{runId}/results?api-version=7.1`

```json
[
  {
    "testPoint": { "id": "0" },
    "outcome": "Passed",
    "state": "Completed"
  }
]
```

Use outcome `Failed` for a failed point. After the Bug exists, include `associatedBugs: [{ "id": 0 }]`.
Set the run state to `Completed` through the Runs update operation. Read the saved run.

## Test Case steps

`Microsoft.VSTS.TCM.Steps` stores XML. Use lowercase `steps`. Start step `id` at 1. Set `last` to the final step id.

```xml
<steps id="0" last="1">
  <step id="1" type="ValidateStep">
    <parameterizedString isformatted="true">Action</parameterizedString>
    <parameterizedString isformatted="true">Pass mark</parameterizedString>
    <description/>
  </step>
</steps>
```

## Tests link

List relation types. Add the relation named `Tests` from the Test Case to the User Story.
The expected reference name is `Microsoft.VSTS.Common.TestedBy-Reverse`.
Use the listed reference name when it differs. Do not write the link until the list confirms the name.
