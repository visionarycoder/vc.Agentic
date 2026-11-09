---
name: "sfp-cluster-controller"
description: "Agent uses this controller to route a CWE-888 Software Fault Pattern (SFP) Primary Cluster or a raw CWE ID to the owning specialist skill, and to confirm full coverage of the MITRE CWE-888 taxonomy (23 Primary Clusters, 57 Secondary Clusters, 619 member CWEs, CWE version 4.20)."
metadata:
  metadata-version: "1.0.0"
  title: "SFP Cluster Controller"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# SFP Cluster Controller

Agent uses this controller to route a CWE-888 Software Fault Pattern (SFP) Primary Cluster or a raw CWE ID to the owning specialist skill, and to confirm full coverage of the MITRE CWE-888 taxonomy (23 Primary Clusters, 57 Secondary Clusters, 619 member CWEs, CWE version 4.20).

## When to Use

| Condition | Agent Action |
|---|---|
| User names an SFP Primary or Secondary Cluster | Route by Primary Cluster Lookup Matrix |
| User names a raw CWE ID with unknown owning skill | Search `references/sfp-888-full-catalog.md`, then route by matching Primary Cluster |
| User asks whether CWE-888 taxonomy is fully covered | Confirm against Coverage Summary |
| User asks for cross-family remediation across CWE families | Route to `security-controller` for mode selection, then this controller for cluster-level routing |

## When Not to Use

| Condition | Route |
|---|---|
| One CWE specialist skill is already named and the fix is narrow | Use the named specialist directly |
| Request needs scan, remediate, verify, or report mode selection | Use `security-controller` |
| Request needs OWASP Top 10 or MITRE CWE Top 25 mapping | Use `security-controller` report mode |

## Primary Cluster Lookup Matrix

| # | SFP Primary Cluster (CWE ID) | Secondary Clusters | Owning Skill |
|---|---|---|---|
| 1 | Risky Values (885) | Glitch in Computation (998) | `cwe-logic-correctness-fixes` |
| 2 | Unused entities (886) | — | `cwe-logic-correctness-fixes` |
| 3 | API (887) | Use of an Improper API (1001) | `cwe-api-contract-fixes` |
| 4 | Entry Points (897) | — | No dedicated skill. Route case-by-case to `dotnet-code-quality-standards` or `refactor`. Cluster is mostly Java/J2EE-specific entry-point patterns with limited direct applicability to managed C#. |
| 5 | Exception Management (889) | Ambiguous Exception Type (960), Incorrect Exception Behavior (961), Unchecked Status Condition (962) | `cwe-exception-management-fixes` |
| 6 | Memory Access (890) | Faulty Buffer Access (970), Faulty Pointer Use (971), Faulty String Expansion (972), Improper NULL Termination (973), Incorrect Buffer Length Computation (974) | `cwe-memory-safety-fixes` |
| 7 | Memory Management (891) | Faulty Memory Release (969) | `cwe-memory-safety-fixes` |
| 8 | Faulty Resource Release (1237) | — | `cwe-memory-safety-fixes` |
| 9 | Failure to Release Memory (1238) | — | `cwe-memory-safety-fixes` |
| 10 | Resource Management (892) | Unrestricted Consumption (985), Faulty Resource Use (983) | `cwe-resource-management-fixes` |
| 11 | Path Resolution (893) | Path Traversal (981) | `cwe-miscellaneous-security-fixes` |
| 12 | Synchronization (894) | Missing Lock (986), Multiple Locks/Unlocks (987), Race Condition Window (988), Unrestricted Lock (989) | `cwe-concurrency-fixes` |
| 13 | Information Leak (895) | Exposed Data (963) | `cwe-resource-management-fixes`, `cwe-data-protection-fixes` |
| 14 | Tainted Input (896) | Tainted Input to Variable (994), Tainted Input to Command (990), Tainted Input to Environment (991) | `cwe-input-validation-fixes`, `cwe-injection-attack-fixes`, `cwe-data-protection-fixes`, `cwe-format-external-fixes` |
| 15 | Authentication (898) | Digital Certificate (948) | `cwe-authentication-authz-fixes`, `cwe-data-protection-fixes` |
| 16 | Access Control (899) | Insecure Resource Access (945), Access Management (944) | `cwe-authentication-authz-fixes`, `cwe-resource-management-fixes` |
| 17 | Privilege (901) | — | `cwe-resource-management-fixes`, `cwe-miscellaneous-security-fixes` |
| 18 | Channel (902) | Channel Attack (956), Protocol Error (957) | `cwe-channel-fixes` |
| 19 | Cryptography (903) | Broken Cryptography (958), Weak Cryptography (959) | `cwe-cryptography-fixes` |
| 20 | Malware (904) | includes Covert Channel (968) | `cwe-malware-indicators-fixes` |
| 21 | Predictability (905) | — | `cwe-cryptography-fixes` |
| 22 | UI (906) | Feature (995), Security (996), Information Loss (997) | `cwe-ui-security-fixes` |
| 23 | Other (907) | — | No dedicated skill. Broad code-quality catch-all. Route case-by-case to `dotnet-code-quality-standards` or `refactor`. |

## CWE-to-Cluster Lookup

| Need | Agent Action |
|---|---|
| Find the Primary and Secondary Cluster for one CWE ID | Search `references/sfp-888-full-catalog.md` for the CWE ID |
| Confirm a CWE belongs to more than one cluster | Check the catalog. CWE-415 and CWE-763 are confirmed multi-cluster members in the MITRE graph. |
| Confirm CWE-900 absence | CWE-900 is a legitimate numbering gap in the official MITRE taxonomy, not missing catalog data |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Identify cluster or CWE | Agent reads the user request for an SFP Cluster name or CWE ID. | Review request text. | Cluster or CWE ID is identified, or the full catalog search runs. |
| 2. Route | Agent matches row 1-23 in the Primary Cluster Lookup Matrix. | Compare cluster name against the matrix. | One or more owning skills are selected. |
| 3. Delegate | Agent invokes the owning skill's workflow for the actual fix. | Owning skill workflow runs. | Fix follows the owning skill's rules, not this controller's. |
| 4. Verify coverage | Agent confirms the finding maps to a named skill or an explicit no-dedicated-skill note. | Compare against Coverage Summary. | Every in-scope CWE has a routing decision. |

## Coverage Summary

| Metric | Value |
|---|---|
| Primary Clusters | 23 of 23 mapped (21 to a dedicated or shared skill, 2 to explicit catch-all routing) |
| Secondary Clusters | 57 of 57 present in the full catalog |
| Member CWEs | 619 of 619 present in the full catalog |
| CWE version | 4.20 |
| New specialist skills added for this task | `cwe-logic-correctness-fixes`, `cwe-api-contract-fixes`, `cwe-exception-management-fixes`, `cwe-memory-safety-fixes`, `cwe-concurrency-fixes`, `cwe-cryptography-fixes`, `cwe-channel-fixes`, `cwe-ui-security-fixes`, `cwe-malware-indicators-fixes` |
| Existing skills extended with SFP cross-references | `cwe-resource-management-fixes`, `cwe-miscellaneous-security-fixes`, `cwe-data-protection-fixes`, `cwe-injection-attack-fixes`, `cwe-input-validation-fixes`, `cwe-authentication-authz-fixes`, `cwe-format-external-fixes`, `security-controller` |

## Special Handling Notes

| Note | Detail |
|---|---|
| AI/ML, composite/chain, and taxonomy skills | `cwe-ai-ml-security-fixes`, `cwe-composite-chain-analysis`, and `cwe-taxonomy-navigator` cover weaknesses and organizer concepts outside the CWE-888 SFP Primary Cluster taxonomy (CWE-1448, CWE-678, CWE-709, and the MITRE view/category set are not SFP clusters). Agent routes to them directly by name or behavior, not through this controller's Primary Cluster matrix. |

| Note | Detail |
|---|---|
| Malware Indicators skill scope | `cwe-malware-indicators-fixes` covers code-review and insider-threat detection guidance for a trusted internal codebase. It does not cover antivirus signature scanning. Agent escalates before removal or alteration of a suspected finding to preserve forensic evidence. |
| Memory safety applicability | `cwe-memory-safety-fixes` applies mainly to `unsafe` blocks, P/Invoke, and native interop code. Agent states when a memory-access CWE has no direct managed-C# equivalent. |
| CWE-352, CWE-918 | Not present in the CWE-888 SFP taxonomy. Agent still routes CWE-352 to `cwe-authentication-authz-fixes` and CWE-918 to `cwe-miscellaneous-security-fixes` using the existing CWE family routing, independent of SFP cluster membership. |

## References

| File | Use |
|---|---|
| `references/sfp-888-full-catalog.md` | Full 619-CWE nested catalog: 23 Primary Clusters, 57 Secondary Clusters, member CWE lists, source attribution |

## Verification Checklist

- [ ] All 23 Primary Clusters resolve to an owning skill or an explicit catch-all note.
- [ ] All 9 new specialist skills exist under `.github/skills/`.
- [ ] All 8 extended skills carry an SFP Cluster cross-reference column.
- [ ] `references/sfp-888-full-catalog.md` exists and lists 619 CWEs.
- [ ] STE modal scan returns zero prohibited matches.

## Common Pitfalls

| Pitfall | Agent Fix |
|---|---|
| Treating "Entry Points" or "Other" as unmapped gaps | Agent states the explicit catch-all routing instead of leaving them silent. |
| Fixing a CWE directly in this controller | Agent delegates the fix to the owning specialist skill. |
| Assuming one CWE has exactly one cluster | Agent checks the full catalog for confirmed multi-cluster CWEs before reporting a single owner. |
