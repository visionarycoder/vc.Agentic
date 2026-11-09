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
| WebAPI | `webapi-intake-router` | `dotnet-webapi`, `webapi-fixes-bundle` | `webapi-rest-route-standardization`, `webapi-input-validation`, `webapi-authz-hardening`, `webapi-error-contract-hardening`, `webapi-compatibility-migration` |
| Documentation | `documentation-intake-router` | `documentation-fixes`, `documentation-fixes-bundle` | `documentation-link-repair`, `documentation-frontmatter`, `documentation-file-placement`, `documentation-governance`, `agent-instruction-governance` |
| Testing | `testing-intake-router` | `test-fixes`, `test-fixes-bundle` | `test-anti-patterns`, `test-gap-analysis`, `assertion-quality`, `test-smell-detection`, `grade-tests` |
| Security | `security-intake-router` | `cwe-fixes` | `cwe-input-validation-fixes`, `cwe-authentication-authz-fixes`, `cwe-injection-attack-fixes`, `cwe-data-protection-fixes`, `cwe-resource-management-fixes`, `cwe-miscellaneous-security-fixes`, `cwe-format-external-fixes` |
| MSBuild | `msbuild-intake-router` | `msbuild-modernization`, `msbuild-antipatterns` | `msbuild-directory-build-organization`, `msbuild-parallelism`, `msbuild-performance-diagnostics`, `msbuild-binlog-failure-analysis`, `check-bin-obj-clash` |
| Azure | `azure-intake-router` | `azure-functions`, `azure-ad-authentication`, `azure-app-configuration`, `azure-keyvault`, `azure-storage` | `aspnetcore-identity-setup`, `dotnet-webapi`, `configuration-options-pattern` |
| EF Core | `efcore-intake-router` | `efcore-dbcontext-design`, `efcore-migrations`, `efcore-testing-patterns` | `optimizing-ef-core-queries`, `vbd-access-components`, `dotnet-mapping-standards` |
| Frontend | `frontend-intake-router` | `angular-modernization`, `vue3-webapp-setup`, `webapp-consolidation-strategy`, `wpf-project-setup` | `angular-anti-patterns`, `angular-to-vue3-migration`, `vue3-pinia-state-management`, `vue3-e2e-testing-playwright`, `wpf-mvvm-implementation` |
| Roslyn/Ifx | `roslyn-intake-router` | `roslyn-analyzer-authoring`, `roslyn-codefix-authoring`, `roslyn-source-generator-authoring` | `roslyn-ca-code-quality-fixes`, `roslyn-ca-design-quality-fixes`, `roslyn-ca-perf-reliability-fixes`, `mcp-csharp-test` |
| Data/Fabric | `data-intake-router` | `fabric-kql-diagnostics`, `fabric-lakehouse-ingestion`, `fabric-pipeline-diagnostics`, `fabric-semantic-model-builder` | `data-contract-frontmatter`, `data-lineage`, `data-quality-reporting`, `data-window-validation` |
| Generic .NET | `dotnet-intake-router` | `dotnet-code-review`, `dotnet-dependency-injection-standards`, `dotnet-validation-standards`, `dotnet-logging-standards`, `dotnet-performance-standards` | `dotnet-dto-standards`, `dotnet-mapping-standards`, `dotnet-namespace-standards`, `dotnet-value-object-standards`, `dotnet-resilience-standards`, `dotnet-caching-patterns`, `dotnet-channels-patterns` |

## Ownership Notes

- `vbd-dto-authoring` owns DTO rules inside VBD scope.
- `dotnet-dto-standards` stays the generic DTO skill outside VBD scope.
- `webapi-fixes-bundle`, `documentation-fixes-bundle`, and `test-fixes-bundle` remain valid alias or mixed-entry surfaces.
- Generic `.NET` skills apply after domain routing resolves scope.
