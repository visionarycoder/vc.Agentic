---
title: Skill Suite Ownership Matrix
doc_type: reference
status: active
last_updated: 2026-08-15
---

# Skill Suite Ownership Matrix

This matrix defines the routed-suite model for repository skills.

## Rules

1. One global intake router chooses a domain router.
2. One domain router chooses one primary execution skill.
3. Secondary specialists load only for explicit missing concerns.
4. Domain-specific skills override generic technology skills inside domain scope.
5. Bundle or alias skills exist only when they reduce ambiguity or token cost.

## Suites

| Suite | Router | Primary execution skills | Secondary specialists |
|---|---|---|---|
| VBD | `vbd-intake-router` | `vbd-system-design`, `vbd-component-construction`, `vbd-access-components`, `vbd-engine-components`, `vbd-manager-components` | `vbd-dto-authoring`, `vbd-boundary-contract-mapping`, `vbd-architecture-conformance`, `vbd-advanced-design`, `vbd-change-simulation` |
| WebAPI | — | `webapi-fixes-bundle` | `webapi-input-validation`, `webapi-error-contract-hardening`, `webapi-compatibility-migration` |
| Documentation | `documentation-intake-router` | `documentation-fixes`, `documentation-fixes-bundle` | `documentation-link-repair`, `documentation-file-placement`, `documentation-governance` |
| Testing | `testing-intake-router` | — | `assertion-quality`, `test-smell-detection` |
| Security | `security-intake-router` | `cwe-fixes` | `cwe-input-validation-fixes`, `cwe-authentication-authz-fixes`, `cwe-injection-attack-fixes`, `cwe-resource-management-fixes`, `cwe-miscellaneous-security-fixes` |
| MSBuild | `msbuild-intake-router` | — | `check-bin-obj-clash` |
| Azure | `azure-intake-router` | `azure-storage` | — |
| Frontend | `frontend-intake-router` | `webapp-consolidation-strategy` | `angular-anti-patterns`, `angular-to-vue3-migration` |
| Roslyn/Ifx | `roslyn-intake-router` | `roslyn-codefix-authoring`, `roslyn-source-generator-authoring` | — |
| Data/Fabric | `data-intake-router` | — | `data-contract-frontmatter`, `data-lineage`, `data-quality-reporting` |
| Generic .NET | `dotnet-intake-router` | — | `dotnet-channels-patterns` |

## Ownership Notes

- `vbd-dto-authoring` owns DTO rules inside VBD scope.
- `webapi-fixes-bundle` and `documentation-fixes-bundle` remain valid alias or mixed-entry surfaces.
- Generic `.NET` skills apply after domain routing resolves scope.
