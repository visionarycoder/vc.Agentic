---
name: "cwe-ui-security-fixes"
description: "Consolidated guidance for UI misrepresentation, password masking, unsafe-action warning, security-feature discrepancy, and security-information loss CWEs with measurable fixes and verification."
metadata:
  metadata-version: "1.0.0"
  title: "CWE UI Security Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "security"
---

# CWE UI Security Fixes

Agent uses this bundle for UI misrepresentation, unsafe-action warning, password masking, security-control discrepancy, and security-information loss defects.

## Activation

**USE FOR:** CWE-221, CWE-222, CWE-223, CWE-224, CWE-356, CWE-357, CWE-446, CWE-451, CWE-549.
**DO NOT USE FOR:** Backend authorization defects, transport-channel defects, or unrelated visual design refinement without security impact.

## Critical Rules

| Rule | Test | Pass |
|---|---|---|
| Agent presents security-relevant state, origin, and file type with accurate labels and trusted cues. | Run UI tests with spoofed names, icons, origins, or extensions. | UI shows the real security-relevant value. |
| Agent masks password and secret-entry fields in every interactive view. | Inspect rendered password-entry controls in existing UI tests or view checks. | Secret-entry fields render with masked input controls. |
| Agent requires explicit user acknowledgment before destructive or irreversible actions. | Run delete, revoke, or disable flows without confirmation. | Unsafe action does not execute without confirmation. |
| Agent distinguishes dangerous actions from safe actions with consistent labels and prominence. | Review action styling and text in existing UI snapshots or component tests. | Dangerous actions remain distinct. |
| Agent preserves security-relevant details in UI grids, dialogs, and exports. | Run UI or export tests with long status, audit, or identity values. | Security-relevant content stays visible, expandable, or exportable. |

## CWE Coverage

| CWE | Concern | Trigger Pattern | Fix Pattern | Verification |
|---|---|---|---|---|
| 451 | UI misrepresentation of critical information | UI shows trusted file icon, origin, or extension from untrusted display name rather than verified metadata | Render verified origin, media type, extension, and security indicators from trusted data | Run spoofed-name UI test. Pass: UI shows verified origin or file type. |
| 549 | Missing password field masking | Password or secret entry uses text input, plain bind, or visible echo control | Use password input control and masked secret-entry component in every view | Run rendered-control check. Pass: Secret input is masked. |
| 356 | Product UI does not warn user of unsafe actions | Delete, revoke, approve, or publish action executes immediately without confirmation | Add confirmation dialog, second-step acknowledgment, or undo flow per repo pattern | Run destructive-flow test. Pass: Unsafe action requires confirmation. |
| 357 | Insufficient UI warning of dangerous operations | Dangerous action uses the same label, color, placement, or emphasis as safe action | Use distinct danger label, styling, iconography, and explanatory text | Run UI snapshot or component test. Pass: Dangerous action is distinct and labeled. |
| 446 | UI discrepancy for security feature | UI checkbox, badge, toggle, or banner claims a security control is active while backend state differs or one view omits the control | Bind UI to authoritative state, remove fake affordances, and keep views consistent | Run multi-view state test. Pass: Every view reflects the same security state. |
| 221 | Information loss or omission | Audit, identity, or warning field is omitted from a grid, dialog, or export | Include the required security-relevant field or provide drill-down access | Run grid or export test. Pass: Required field is present. |
| 222 | Truncation of security-relevant information | Long status, actor, certificate, host, or reason text truncates without expansion or full export | Add wrap, tooltip, expand, detail pane, or full-fidelity export | Run long-value UI test. Pass: Full value remains accessible. |
| 223 | Omission of security-relevant information | Summary card, row, or notification drops failure reason, target, actor, or timestamp needed for security judgment | Show essential security context in summary and details | Run alert-display test. Pass: User can see the security context. |
| 224 | Obscured security-relevant information by alternate name | UI renames blocked, revoked, unsigned, external, or unverified state to vague wording | Use precise security terminology and preserve the authoritative status meaning | Run terminology review or snapshot test. Pass: UI uses unambiguous labels. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1. Inventory | Agent scans UI components, forms, dialogs, grids, exports, and status labels for security-relevant rendering. | Run `rg -n "password|delete|revoke|confirm|warning|danger|audit|status|origin|filename|extension|tooltip|truncate" -g "**/*.{razor,cshtml,ts,tsx,vue,cs}"`. | Hotspot list exists for each touched file. |
| 2. Classify | Agent maps each hotspot to one CWE row. | Review hotspot list. | Every hotspot has one CWE label or explicit out-of-scope note. |
| 3. Fix | Agent adds accurate labels, masked fields, confirmations, danger styling, consistent bindings, and full-detail affordances. | Run targeted build for the touched project. | Build passes with zero new errors. |
| 4. Run tests | Agent runs existing UI, component, snapshot, accessibility, or export tests for touched scope. | Run existing tests for touched scope. | All targeted tests pass. |
| 5. Re-scan | Agent runs grep and UI checks again. | Re-run inventory commands. | Zero unexplained targeted hits remain in touched files. |

## Decision Matrix

| Condition | Use |
|---|---|
| UI renders file, origin, or trust state | Use verified metadata and explicit security indicators |
| UI accepts password or secret text | Use masked control with secure bind pattern |
| UI triggers destructive action | Use confirmation, acknowledgment, or undo pattern |
| UI shows warning or danger action | Use distinct text and visual treatment |
| UI displays audit or security status detail | Use full-fidelity display, expansion, or export |

## Repo Notes

| Area | Agent Uses | Agent Avoids |
|---|---|---|
| Razor or MVC forms | Built-in password inputs and server-validated confirmation flows | Plain text secret entry controls |
| Component state | Authoritative backend or store-backed security status | Hard-coded security badges or toggles |
| Grid and export detail | Expanders, tooltips, detail dialogs, and full export fields | Silent truncation of security-relevant values |

## Verification Checklist

Agent verifies:
- [ ] Critical UI data is accurate and non-misleading
- [ ] Secret-entry fields are masked
- [ ] Unsafe actions require explicit confirmation
- [ ] Dangerous actions remain visually distinct
- [ ] Security-relevant details remain visible or fully accessible

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| CWE subset | No | All 9 |
| UI flow scope | No | All matching files |

## Outputs

Agent generates:
- Hotspot list with CWE labels
- Patch set for UI warning, masking, labeling, and information-preservation fixes
- Verification notes with UI, snapshot, accessibility, and export results

## References

- CWE-888 SFP Primary Cluster: UI
- OWASP User Interface Security guidance
- ASP.NET Core forms and validation guidance
- Repository UI component patterns
