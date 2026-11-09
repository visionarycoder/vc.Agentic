---
name: "azure-intake-router"
description: "Route Azure requests to the minimum correct Azure skill by separating identity, configuration, functions, secrets, and storage concerns before deeper implementation guidance loads."
metadata:
  metadata-version: "1.0.0"
  title: "Azure Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "azure"
---

# Azure Intake Router

Agent routes Azure work to one primary Azure skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Azure platform work and the exact Azure concern is not yet narrowed | Use this skill |
| Request involves identity, configuration, secrets, functions, or storage | Use this skill |
| User asks which Azure skill owns the work | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Azure request is already narrowed to one known Azure execution skill | Use that Azure skill |
| Request is domain-first and Azure is only an implementation detail | Use the domain router first |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad Azure routing belongs here |
| Domain precedence | Domain suites win when Azure is only an implementation detail inside a broader domain workflow |
| Specialist loading | Choose one Azure primary first, then only concrete follow-on Azure specialists |
| Security split | Secret access routes to Key Vault before broader configuration guidance when secrets dominate |

## Verification

- [ ] Agent chose one primary Azure skill
- [ ] Agent added a secondary Azure skill only when the primary scenario required it
- [ ] Agent avoided broad Azure cross-loading for narrow tasks

## Routing Table

| Intent | Primary skill | Optional secondary |
|---|---|---|
| Azure Functions host or trigger work | `azure-functions` | `azure-storage` |
| Entra ID or downstream token flow | `azure-ad-authentication` | `azure-keyvault` |
| App Configuration or feature flags | `azure-app-configuration` | `azure-keyvault` |
| Secret or certificate access | `azure-keyvault` | `azure-ad-authentication` |
| Blob, Queue, or Table Storage | `azure-storage` | `azure-functions` |
