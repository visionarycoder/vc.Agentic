---
name: "devops-pipeline-harness"
description: "Verify the CI/CD harnesses and pipeline rules when the developer layer is devops."
metadata:
  metadata-version: "1.0.0"
  title: "DevOps Pipeline Harness"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# DevOps Pipeline Harness

Load this skill when the `developer` agent works in layer `devops` (write scope `.devops/**` and `azure-pipelines.yml`).

## Harnesses To Verify

| Harness | Pass criteria |
|---|---|
| Restore and build | Solution builds with zero analyzer warnings |
| Tests | Unit, integration, and chaos suites run and publish results |
| Coverage | Coverage report published |
| PR scope check | Script from the `tooling` layer runs on every pull request |
| Security | Dependency and secret scanning run and fail the build on findings |
| Database | `database` layer project builds and publishes a dacpac |
| Artifacts | Versioned artifacts publish on tags |
| Compile stage | Build checks for security vulnerabilities, runs unit tests, then creates artifacts stored in Azure DevOps (release standard) |
| QA stage | Release deploys to QA automatically; integration tests run there |
| Production approval | Pre-deployment approver exists and has no write permission to the code repository |
| Merge to main | Final branch merges into `main` only after production deployment completes |
| Hot fix | Expedited path uses the same stages and approvals |
| Environments | Deployment stages use environments with approvals |
| Branch policy | `development` requires PR build and review approval; `main` updates only through the release pipeline |

## Process

1. Submit a proposal to `application-architect`: stages, triggers, environments, and service connections. Wait for approval before writing (Gate 2).
2. Implement the pipelines using templates in `.devops/pipelines/` to avoid duplication.
3. Validate with the Azure DevOps YAML validation API or a dry-run, and confirm a run succeeds.

## Rules

- Use the `az devops` CLI for pipeline, variable group, environment, and service connection setup.
- Create secrets and service connections through `az devops`. Secrets never appear in files, logs, commits, or work items. Prefer workload identity federation and managed identity over stored secrets.
- Pin task and template versions.
- Keep production deployment behind an approval gate.
