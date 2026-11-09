---
name: "azure-deploy"
description: "Execute Azure deployments for ALREADY-PREPARED applications that have existing .azure/deployment-plan.md and infrastructure files. DO NOT use this skill when the user asks to CREATE a new application — use azure-prepare instead. This skill runs azd up, azd deploy, terraform apply, and az deployment commands with built-in error recovery. Requires .azure/deployment-plan.md from azure-prepare and validated status from azure-validate. WHEN: \"run azd up\", \"run azd deploy\", \"execute deployment\", \"push to production\", \"push to cloud\", \"go live\", \"ship it\", \"bicep deploy\", \"terraform apply\", \"publish to Azure\", \"launch on Azure\". DO NOT USE WHEN: \"create and deploy\", \"build and deploy\", \"create a new app\", \"set up infrastructure\", \"create and deploy to Azure using Terraform\" — use azure-prepare for these."
metadata:
  metadata-version: "1.0.0"
  title: "Azure Deploy"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "azure"
---

# Azure Deploy

This reusable procedure follows the user request, repository instructions, and accepted deployment plan. It grants no operational approval.

---

## Steps

| # | Action | Reference |
|---|--------|-----------|
| 1 | **Check Plan** — Read `.azure/deployment-plan.md`, verify status = `Validated` AND **Validation Proof** section is populated | `.azure/deployment-plan.md` |
| 2 | **Pre-Deploy Checklist** — MUST complete ALL steps | [Pre-Deploy Checklist](references/pre-deploy-checklist.md) |
| 3 | **Load Recipe** — Based on `recipe.type` in `.azure/deployment-plan.md` | [recipes/README.md](references/recipes/README.md) |
| 4 | **RBAC Health Check** — For Container Apps + ACR with managed identity: run `azd provision --no-prompt`, then verify `AcrPull` role has propagated before proceeding (see checklist) | [Pre-Deploy Checklist — Container Apps RBAC](references/pre-deploy-checklist.md#container-apps--acr--pre-deploy-rbac-health-check) |
| 5 | **Execute Deploy** — Follow recipe steps | Recipe README |
| 6 | **Post-Deploy** — Configure SQL managed identity and apply EF migrations if applicable | [Post-Deployment](references/recipes/azd/post-deployment.md) |
| 7 | **Handle Errors** — See recipe's `errors.md` | — |
| 8 | **Verify Success** — Confirm deployment completed and endpoints are accessible | [Verification](references/recipes/azd/verify.md) |
| 9 | **Live Role Verification** — Query Azure to confirm provisioned RBAC roles are correct and sufficient | [live-role-verification.md](references/live-role-verification.md) |
| 10 | **Report Results** — Present deployed endpoint URLs to the user as fully-qualified `https://` links | [Verification](references/recipes/azd/verify.md) |

> **⛔ URL FORMAT RULE**
>
> When presenting endpoint URLs to the user, you **MUST** always use fully-qualified URLs with the `https://` scheme (e.g. `https://myapp.azurewebsites.net`, not `myapp.azurewebsites.net`). Many Azure CLI commands return bare hostnames without a scheme — always prepend `https://` before presenting them.

> **⛔ VALIDATION PROOF CHECK**
>
> When checking the plan, verify the **Validation Proof** section (Section 7) contains actual validation results with commands run and timestamps. If this section is empty, validation was bypassed — invoke **azure-validate** skill first.

## SDK Quick References

- **Azure Developer CLI**: [azd](references/sdk/azd-deployment.md)
- **Azure Identity**: [Python](references/sdk/azure-identity-py.md) | [.NET](references/sdk/azure-identity-dotnet.md) | [TypeScript](references/sdk/azure-identity-ts.md) | [Java](references/sdk/azure-identity-java.md)

## MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp_azure_mcp_subscription_list` | List available subscriptions |
| `mcp_azure_mcp_group_list` | List resource groups in subscription |
| `mcp_azure_mcp_azd` | Execute AZD commands |
| `azure__role` | List role assignments for live RBAC verification (step 9) |

## References

- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions
- [Post-Deployment Steps](references/recipes/azd/post-deployment.md) - SQL + EF Core setup
