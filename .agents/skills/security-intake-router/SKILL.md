---
name: "security-intake-router"
description: "Route security requests to the minimum correct security skill by separating broad CWE sweeps from narrow vulnerability-family remediation."
metadata:
  metadata-version: "1.0.0"
  title: "Security Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Security Intake Router

Agent routes security work to one primary security skill.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Security Intake Router work | Use this skill |
| Request falls inside the security suite and needs this specific surface | Use this skill |
| The routed catalog needs a single current-state owner for this concern | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is already narrowed to one execution skill | Use that execution skill |
| Request belongs to a different suite | Use the correct suite router |
| Request is not skill-catalog routing work | Use the matching domain skill |

## Routing Rules

| Topic | Rule |
|---|---|
| Entry ownership | Broad security routing belongs here. |
| Current-state rule | Agent treats this skill catalog as the only valid current state. |
| Scope control | Agent keeps this skill focused on one clear concern. |
| Skill loading | Agent loads one primary surface first and adds only concrete secondary support. |

## Verification

- [ ] Agent chose `cwe-fixes` only for broad or mixed security requests
- [ ] Agent routed narrow security requests to one thematic skill
- [ ] Agent avoided loading multiple CWE families unless request scope required it

## Routing Table

| Intent | Primary skill |
|---|---|
| Broad security sweep or multiple vulnerability families | `cwe-fixes` |
| Input validation / bounds | `cwe-input-validation-fixes` |
| Authentication / authorization / CSRF | `cwe-authentication-authz-fixes` |
| Injection / SQL / command / XSS | `cwe-injection-attack-fixes` |
| Disclosure / deserialization / secrets | `cwe-data-protection-fixes` |
| Resource, logging injection, privilege, DoS | `cwe-resource-management-fixes` |
| Traversal, upload, redirect, SSRF, null | `cwe-miscellaneous-security-fixes` |
| Search path / format external control | `cwe-format-external-fixes` |
