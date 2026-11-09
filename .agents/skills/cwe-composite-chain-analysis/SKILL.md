---
name: "cwe-composite-chain-analysis"
description: "Decompose composite and named-chain CWE findings into component weaknesses and route each component to the owning specialist skill."
metadata:
  metadata-version: "1.0.0"
  title: "CWE Composite & Chain Analysis"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE Composite & Chain Analysis

Agent uses this skill to decompose composites, where all component weaknesses exist together, and named chains, where one weakness enables the next, into verified component weaknesses, then route each component to the owning specialist skill.

## Activation

**USE FOR:** Findings that match MITRE View-678 Composites or View-709 Named Chains; one exploit path that spans multiple CWE components; one finding that crosses multiple existing CWE specialist skills.
**DO NOT USE FOR:** Single-CWE findings with one owning skill; direct vulnerability mapping to View-678 or View-709; unrelated architecture redesign.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent treats View-678 and View-709 as navigation views, not fix targets. | Review the mapped CWE ID. | Fix plan targets member CWEs, not View-678 or View-709. |
| Agent verifies every cited composite or chain against the MITRE member page title and component table before routing work. | Review the evidence rows in the analysis note. | Every cited example lists a verified title and verified component CWE IDs. |
| Agent routes each component weakness to its owning specialist skill. | Review the routing matrix for the finding. | Every component has one owning skill or an explicit `security-controller` escalation. |
| Agent breaks the exploit path by removing at least one required composite component or one primary/resultant chain link. | Run targeted tests or existing scanners for touched scope. | The exploit path no longer reproduces after the component fixes land. |

## Taxonomy Coverage

| Scope | CWE | MITRE Title | Verified Components | Route Skills |
|---|---:|---|---|---|
| Composite | 689 | Permission Race Condition During Resource Copy | 362 Concurrent Execution using Shared Resource with Improper Synchronization; 732 Incorrect Permission Assignment for Critical Resource | `cwe-concurrency-fixes` + `cwe-resource-management-fixes` |
| Composite | 352 | Cross-Site Request Forgery (CSRF) | 346 Origin Validation Error; 441 Unintended Proxy or Intermediary; 613 Insufficient Session Expiration; 642 External Control of Critical State Data | `cwe-channel-fixes` + `cwe-authentication-authz-fixes` + `cwe-input-validation-fixes` |
| Composite | 384 | Session Fixation | 346 Origin Validation Error; 441 Unintended Proxy or Intermediary; 472 External Control of Assumed-Immutable Web Parameter | `cwe-channel-fixes` + `cwe-authentication-authz-fixes` + `cwe-input-validation-fixes` |
| Chain | 680 | Integer Overflow to Buffer Overflow | 190 Integer Overflow or Wraparound → 119 Improper Restriction of Operations within the Bounds of a Memory Buffer | `cwe-resource-management-fixes` + `cwe-memory-safety-fixes` |
| Chain | 690 | Unchecked Return Value to NULL Pointer Dereference | 252 Unchecked Return Value → 476 NULL Pointer Dereference | `cwe-logic-correctness-fixes` + `cwe-memory-safety-fixes` |
| Chain | 692 | Incomplete Denylist to Cross-Site Scripting | 184 Incomplete List of Disallowed Inputs → 79 Improper Neutralization of Input During Web Page Generation | `cwe-input-validation-fixes` + `cwe-injection-attack-fixes` |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Detect | Agent identifies a candidate composite or named chain from scanner output, review notes, or exploit narrative. | Review the candidate finding. | Finding references one composite or named-chain CWE or one multi-step exploit path. |
| 2. Verify | Agent checks the MITRE view page for membership, then checks the member page for the title and component table. | Review saved evidence rows. | Membership, title, and components match MITRE. |
| 3. Decompose | Agent rewrites the finding as component CWE rows with primary/resultant or all-required semantics. | Review the decomposition table. | Every component row has one CWE ID, one title, and one role. |
| 4. Route | Agent maps each component row to one specialist skill and one concrete fix stream. | Review the routing plan. | Every component routes to one owning skill or one explicit escalation. |
| 5. Fix | Agent runs the owning skills or applies their fix patterns in the touched code. | Run the smallest existing build and test scope that covers the change. | Component fixes pass targeted validation. |
| 6. Recompose | Agent verifies that the full exploit path is broken after the component fixes land together. | Re-run the exploit, security test, or scanner flow. | Composite or chain no longer reproduces. |

## Decision Matrix

| Condition | Use |
|---|---|
| One finding cites View-678 or View-709 only | Open the named member CWE and decompose it before any edit |
| All components route to one specialist skill | Use this skill for classification, then hand off to that specialist skill |
| Components route to multiple specialist skills | Keep this skill active as the coordinator and split work by component |
| One chain has a clear primary and resultant link | Fix the primary link first, then verify the resultant link no longer activates |
| One composite requires all listed components at the same time | Remove at least one required component and verify exploit failure |
| Component ownership is unclear | Escalate through `security-controller`, then label the cluster with `sfp-cluster-controller` when the pattern spans multiple SFP areas |

## Verification Checklist

Agent verifies:
- [ ] View-678 or View-709 stayed out of the final fix target list
- [ ] Every cited example lists verified component CWE IDs from the member page
- [ ] Every component routes to one owning specialist skill
- [ ] Targeted build and test commands passed for the touched scope
- [ ] The recomposed exploit path failed after the component fixes landed

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| Candidate composite or chain CWE ID | No | Derived from the finding |
| Existing scanner or review evidence | No | Current session evidence |

## Outputs

Agent generates:
- Decomposition table with verified component CWE IDs
- Routing plan that maps components to specialist skills
- Validation note that shows the broken exploit path

## References

| Source | Purpose |
|---|---|
| https://cwe.mitre.org/data/definitions/678.html | View-678 membership |
| https://cwe.mitre.org/data/definitions/709.html | View-709 membership |
| https://cwe.mitre.org/data/definitions/689.html | Composite member verification |
| https://cwe.mitre.org/data/definitions/352.html | Composite member verification |
| https://cwe.mitre.org/data/definitions/384.html | Composite member verification |
| https://cwe.mitre.org/data/definitions/680.html | Chain member verification |
| https://cwe.mitre.org/data/definitions/690.html | Chain member verification |
| https://cwe.mitre.org/data/definitions/692.html | Chain member verification |
