---
name: "cwe-ui-security-fixes"
description: "Consolidated guidance for UI misrepresentation, password masking, unsafe-action warning, security-feature discrepancy, and security-information loss CWEs with measurable fixes and verification."
metadata:
  metadata-version: "1.0.0"
  title: "CWE UI Security Fixes"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "security"
---

# CWE UI Security Fixes

Agent uses this bundle for UI misrepresentation, unsafe-action warning, password masking, security-control discrepancy, and security-information loss defects.

## Activation

**USE FOR:** CWE-221, CWE-222, CWE-223, CWE-224, CWE-356, CWE-357, CWE-446, CWE-451, CWE-549.
**DO NOT USE FOR:** Backend authorization defects, transport-channel defects, or unrelated visual design refinement without security impact.

## Rules

- Show verified origin, media type, and extension, never values derived from untrusted display names; test with spoofed names.
- Mask password and secret entry in every view.
- Require confirmation or undo for destructive actions; style dangerous actions distinctly from safe ones.
- Bind security indicators to authoritative backend or store state; no fake badges or toggles, and keep views consistent.
- Keep security-relevant values (audit, identity, status, reason) visible, expandable, or exportable in full.

## CWE Coverage

| CWE | Trigger Pattern | Fix Pattern |
|---|---|---|
| 451 | Trusted icon, origin, or extension drawn from an untrusted display name | Render verified origin, media type, extension from trusted metadata |
| 549 | Password or secret entry uses plain text input | Password input control in every view |
| 356 | Delete, revoke, approve, or publish runs with no confirmation | Confirmation dialog, second-step acknowledgment, or undo |
| 357 | Dangerous action looks like a safe one in label, color, placement, or emphasis | Distinct danger label, styling, iconography, and explanatory text |
| 446 | UI claims a security control is active while backend state differs, or a view omits it | Bind to authoritative state; remove fake affordances |
| 221 | Audit, identity, or warning field omitted from a grid, dialog, or export | Include the field or provide drill-down |
| 222 | Long status, actor, certificate, host, or reason text truncated | Wrap, tooltip, expand, detail pane, or full export |
| 223 | Summary or notification drops failure reason, target, actor, or timestamp | Show essential security context in summary and details |
| 224 | Blocked, revoked, unsigned, external, or unverified state renamed vaguely (e.g. "inactive") | Use precise security terminology |

## Inventory

`rg -n "password|delete|revoke|confirm|warning|danger|audit|status|origin|filename|extension|tooltip|truncate" -g "**/*.{razor,cshtml,ts,tsx,vue,cs}"`

## Inputs

| Input | Required | Default |
|---|---|---|
| Repo or component path | Yes | - |
| CWE subset | No | All listed |
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
