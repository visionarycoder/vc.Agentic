---
name: "cwe-taxonomy-navigator"
description: "Routes MITRE CWE taxonomy views and categories to the owning repository security skill when a request cites meta-level CWE organizers instead of a fixable weakness."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Taxonomy Navigator"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE Taxonomy Navigator

Agent uses this controller to decode MITRE CWE organizer entries, then route to the repository skill that owns the concrete weakness family.

## When to Use

| Condition | Agent Action |
|---|---|
| User names one of these organizer IDs: 677, 701, 702, 884, 1003, 1008, 1040, 1400, 1450, 2000 | Use the Taxonomy Lookup Matrix. |
| User asks about design-phase weakness, implementation-phase weakness, architectural security tactic, OWASP Top Ten 2025, or mappable CWE for a CVE | Use this navigator first. |
| User cites a CWE view or category instead of a concrete weakness | Translate the organizer into the next routing step. |
| User needs a broad taxonomy explanation before remediation starts | Explain the organizer row, then delegate the fix to the owning skill. |

## When Not to Use

| Condition | Route |
|---|---|
| One concrete weakness family is already named, such as injection, auth, crypto, or path traversal | Use the owning `cwe-*-fixes` skill directly. |
| Request needs scan, remediate, verify, or report flow across many weakness families | Use `security-controller`. |
| Request names an SFP cluster, SFP secondary cluster, or CWE-888 taxonomy concept | Use `sfp-cluster-controller`. |
| Request needs a concrete final CWE for a vulnerability record | Route through this navigator, then end on a member weakness, often from CWE-1003. |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Organizer ID or phrase | Yes | Example: `design-phase weakness`, `OWASP Top Ten 2025`, `mappable CWE`. |
| Current finding summary | Yes | Use the behavior or trust boundary to choose the family. |
| Desired outcome | No | Explanation, routing, remediation, verification, or reporting. |
| Reporting target | No | CVE, OWASP, MITRE trend, or internal triage. |

## Taxonomy Lookup Matrix

| CWE ID | Exact MITRE Title | Type | Use When | Route |
|---|---|---|---|---|
| 701 | Weaknesses Introduced During Design | Category | Request names a design-phase weakness or CWE-701. | `security-controller`, then the owning family. |
| 702 | Weaknesses Introduced During Implementation | Category | Request names an implementation-phase weakness or CWE-702. | `security-controller`, then the owning family. |
| 1008 | Architectural Concepts | View | Request names a security architecture tactic, such as auth, access control, encryption, or communications. | `security-controller`, then `cwe-authentication-authz-fixes`, `cwe-cryptography-fixes`, `cwe-data-protection-fixes`, or `cwe-channel-fixes`. |
| 1040 | Quality Weaknesses with Indirect Security Impacts | Category | Request names indirect security impact, quality weakness, or CWE-1040. | `security-controller`, then `cwe-resource-management-fixes`, `cwe-exception-management-fixes`, `cwe-api-contract-fixes`, or `cwe-logic-correctness-fixes`. |
| 1400 | Comprehensive Categorization for Software Assurance Trends | View | Request needs software assurance trend slicing or CWE-1400. | `security-controller` for reporting, then the member family. |
| 1450 | Weaknesses in OWASP Top Ten RC1 (2025) | View | Request names OWASP Top Ten 2025 or CWE-1450. | `security-controller`, then the OWASP 2025 routing matrix. |
| 884 | CWE Cross-section | View | Request needs a representative sample, survey, or CWE-884. | `security-controller`, then the member family. |
| 1003 | Weaknesses for Simplified Mapping of Published Vulnerabilities | View | Request needs mappable CWE selection for CVE-style classification. | `security-controller`, then a concrete member weakness from this view when the finding fits. |
| 2000 | Comprehensive CWE Dictionary | View | Request starts at the top of the CWE tree with no narrower organizer. | `security-controller`, then 1003, 1008, 1400, 1450, or a direct family. |
| 677 | Weakness Base Elements | Category | Request names a base or atomic weakness class. | `security-controller`, then the owning family. |

## OWASP Top Ten 2025 Routing Matrix

| OWASP 2025 RC1 Category from CWE-1450 | Mapped CWE Family | Route |
|---|---|---|
| A01:2025 - Broken Access Control | Authentication and authorization | `cwe-authentication-authz-fixes` |
| A02:2025 - Security Misconfiguration | Deployment and control-surface hardening | `cwe-miscellaneous-security-fixes` |
| A03:2025 - Software Supply Chain Failures | External control and hostile artifact indicators | `cwe-format-external-fixes`, `cwe-malware-indicators-fixes` |
| A04:2025 - Cryptographic Failures | Cryptography and secret protection | `cwe-cryptography-fixes`, `cwe-data-protection-fixes` |
| A05:2025 - Injection | Injection and untrusted command or query construction | `cwe-injection-attack-fixes`, `cwe-input-validation-fixes` |
| A06:2025 - Insecure Design | Trust-boundary and security-design flaws | `security-controller`, then the owning family |
| A07:2025 - Authentication Failures | Identity, session, and authorization control failures | `cwe-authentication-authz-fixes` |
| A08:2025 - Software or Data Integrity Failures | Integrity and unsafe trust of code or data | `cwe-data-protection-fixes`, `cwe-format-external-fixes` |
| A09:2025 - Logging &amp; Alerting Failures | Logging, alert coverage, and detection gaps | `cwe-resource-management-fixes`, `cwe-exception-management-fixes` |
| A10:2025 - Mishandling of Exceptional Conditions | Error handling and exception control flow | `cwe-exception-management-fixes`, `cwe-logic-correctness-fixes` |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Identify organizer | Agent matches the user phrase or CWE ID to one row in the Taxonomy Lookup Matrix. | Compare the request text to the matrix. | One organizer row is selected. |
| 2. Decode intent | Agent reads whether the request needs explanation, routing, remediation, verification, or reporting. | Review the request verbs and output target. | One next action is selected. |
| 3. Choose family | Agent maps the concrete weakness behavior to the owning family or OWASP row. | Compare the finding behavior to the matrix notes. | One primary route is selected, with one secondary route only when the family overlaps. |
| 4. Hand off | Agent delegates the actual fix or scan flow to the owning skill. | Review the selected skill. | The next skill owns the implementation work. |
| 5. Close the taxonomy gap | Agent replaces the organizer-only label with a member weakness before a vulnerability record closes. | Review the final finding label. | The record ends on a concrete weakness, often one from CWE-1003. |

## Verification Checklist

| Checkpoint | Pass Condition |
|---|---|
| Frontmatter complete | Required skill frontmatter fields exist. |
| Ten organizer rows present | The lookup matrix covers 677, 701, 702, 884, 1003, 1008, 1040, 1400, 1450, and 2000. |
| OWASP 2025 rows present | The routing matrix covers A01 through A10 from CWE-1450. |
| Repository routes preserved | Every row points to an existing repository skill or controller. |
| CVE mapping note preserved | The workflow ends on a concrete weakness, often from CWE-1003. |
| STE wording clean | Modal-verb scan returns zero matches for the prohibited set. |

## Common Pitfalls

| Pitfall | Agent Fix |
|---|---|
| Treating a view or category as the final vulnerability label | Agent routes through the organizer, then records a concrete weakness. |
| Treating `design` or `implementation` as the weakness family | Agent uses 701 and 702 as phase tags, then routes from the actual behavior. |
| Treating OWASP Top Ten 2025 as one family | Agent uses the A01-A10 matrix, then hands off to the owning family skill. |
| Starting a code fix inside this navigator | Agent delegates implementation work to the owning skill. |

## References

| Reference | Use |
|---|---|
| `references/cwe-mitigation-attribute.md` | Agent reads this file to apply the `[CweMitigation]` attribute and query `CweCoverageManifest.Entries` for compile-time CWE coverage discovery. |
