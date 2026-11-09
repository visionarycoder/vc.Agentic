---
metadata-version: "1.0.0"
title: "Azure Compliance & Security Auditing"
description: "Preserve scoped source guidance for azure-compliance."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Azure Compliance & Security Auditing

## Quick Reference

| Property | Details |
|---|---|
| Best for | Compliance scans, security audits, Key Vault expiration checks |
| Primary capabilities | Comprehensive Resources Assessment, Key Vault Expiration Monitoring |
| MCP tools | azqr, subscription and resource group listing, Key Vault item inspection |

## When to Use This Skill

- Run azqr or Azure Quick Review for compliance assessment
- Validate Azure resource configuration against best practices
- Identify orphaned or misconfigured resources
- Audit Key Vault keys, secrets, and certificates for expiration

## Skill Activation Triggers

Activate this skill when user wants to:
- Check Azure compliance or best practices
- Assess Azure resources for configuration issues
- Run azqr or Azure Quick Review
- Identify orphaned or misconfigured resources
- Review Azure security posture
- "Show me expired certificates/keys/secrets in my Key Vault"
- "Check what's expiring in the next 30 days"
- "Audit my Key Vault for compliance"
- "Find secrets without expiration dates"
- "Check certificate expiration dates"

## Prerequisites

- Authentication: user is logged in to Azure via `az login`
- Permissions to read resource configuration and Key Vault metadata

## Assessments

| Assessment | Reference |
|------------|-----------|
| Comprehensive Compliance (azqr) | [references/azure-quick-review.md](../../azure-quick-review.md) |
| Key Vault Expiration | [references/azure-keyvault-expiration-audit.md](../../azure-keyvault-expiration-audit.md) |
| Resource Graph Queries | [references/azure-resource-graph.md](../../azure-resource-graph.md) |

## MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp_azure_mcp_extension_azqr` | Run azqr compliance scans |
| `mcp_azure_mcp_subscription_list` | List available subscriptions |
| `mcp_azure_mcp_group_list` | List resource groups |
| `keyvault_key_list` | List all keys in vault |
| `keyvault_key_get` | Get key details including expiration |
| `keyvault_secret_list` | List all secrets in vault |
| `keyvault_secret_get` | Get secret details including expiration |
| `keyvault_certificate_list` | List all certificates in vault |
| `keyvault_certificate_get` | Get certificate details including expiration |

## Assessment Workflow

1. Select scope (subscription or resource group) for Comprehensive Resources Assessment.
2. Run azqr and capture output artifacts.
3. Analyze Scan Results and summarize findings and recommendations.
4. Review Key Vault Expiration Monitoring output for keys, secrets, and certificates.
5. Classify issues and propose remediation or fix steps for each finding.

### Priority Classification

| Priority | Guidance |
|---|---|
| Critical | Immediate remediation required for high-impact exposure |
| High | Resolve within days to reduce risk |
| Medium | Plan a resolution in the next sprint |
| Low | Track and fix during regular maintenance |

## Error Handling

| Error | Message | Remediation |
|---|---|---|
| Authentication required | "Please login" | Run `az login` and retry |
| Access denied | "Forbidden" | Confirm permissions and fix role assignments |
| Missing resource | "Not found" | Verify subscription and resource group selection |

## Best Practices

- Run compliance scans on a regular schedule (weekly or monthly)
- Track findings over time and verify remediation effectiveness
- Separate compliance reporting from remediation execution
- Keep Key Vault expiration policies documented and enforced

## SDK Quick References

For programmatic Key Vault access, see the condensed SDK guides:

- **Key Vault (Python)**: [Secrets/Keys/Certs](../../sdk/azure-keyvault-py.md)
- **Secrets**: [TypeScript](../../sdk/azure-keyvault-secrets-ts.md) | [Rust](../../sdk/azure-keyvault-secrets-rust.md) | [Java](../../sdk/azure-security-keyvault-secrets-java.md)
- **Keys**: [.NET](../../sdk/azure-security-keyvault-keys-dotnet.md) | [Java](../../sdk/azure-security-keyvault-keys-java.md) | [TypeScript](../../sdk/azure-keyvault-keys-ts.md) | [Rust](../../sdk/azure-keyvault-keys-rust.md)
- **Certificates**: [Rust](../../sdk/azure-keyvault-certificates-rust.md)
