---
name: "vbd-intake-router"
description: "Route VBD requests to the minimum skill set by classifying intent, lifecycle phase, boundary type, and correction-versus-authoring scope before loading detailed guidance."
metadata:
  metadata-version: "1.0.0"
  title: "VBD Intake Router"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "vbd"
---

# VBD Intake Router

Agent uses this skill first for VBD requests. Agent loads the smallest correct follow-on skill set and avoids parallel instruction overlap.

## When to Use

| User prompt | Use |
|---|---|
| User asks about Manager, Engine, Access, DTO, decomposition, or component boundaries | Use this skill |
| VBD authoring and VBD remediation both plausibly apply | Use this skill |
| User asks for the correct VBD workflow or capability skill | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| VBD scope is already narrowed to one known execution skill | Use that VBD execution skill |
| Request is technology-specific and not VBD-scoped | Use the matching non-VBD router |

## Routing Rules

| Topic | Rule |
|---|---|
| Boundary precedence | `vbd-system-design` owns boundary authority |
| DTO precedence | `vbd-dto-authoring` owns VBD DTO rules |
| Generic .NET precedence | Generic `.NET` skills load only after VBD intent is resolved |
| Correction split | Existing-slice correction routes before new authoring when both seem plausible |
| Skill count | Load one VBD primary first, then only concrete secondaries |

## Verification

- [ ] Agent classified lifecycle phase before loading detailed skill text
- [ ] Agent loaded exactly one primary skill first
- [ ] Agent added secondary skill only for a concrete missing concern
- [ ] Agent avoided same-phase peer-skill stacking
- [ ] Agent preferred VBD-specific guidance over generic .NET guidance

## Purpose

Agent reduces token burn and activation ambiguity by classifying the request before reading deeper skills.

## Intake Questions

Agent classifies the request on four axes:

1. **Lifecycle phase**
   - `design`
   - `construction`
   - `capability-authoring`
   - `remediation`
   - `governance`

2. **Boundary focus**
   - `system`
   - `manager`
   - `engine`
   - `access`
   - `dto`
   - `cross-boundary`

3. **Work type**
   - `new`
   - `existing`
   - `mixed`

4. **Requested depth**
   - `decision`
   - `scaffold`
   - `implementation`
   - `fix`
   - `audit`

## Routing Table

| Intent | Primary skill | Optional secondary skill | Load policy |
|---|---|---|---|
| New decomposition or authority split | `vbd-system-design` | `vbd-advanced-design` | Load one primary first |
| New component scaffold | `vbd-component-construction` | `vbd-system-design` | Load construction only unless decomposition is unresolved |
| Access capability or query pattern | `vbd-access-components` | `vbd-dto-authoring` | Load DTO skill only when contract shape changes |
| Engine capability or rule pattern | `vbd-engine-components` | `vbd-dto-authoring` | Load DTO skill only when boundary contracts change |
| Manager workflow or orchestration pattern | `vbd-manager-components` | `vbd-dto-authoring` | Load DTO skill only when workflow contracts change |
| Boundary DTO ownership or immutable record design | `vbd-dto-authoring` | `dotnet-dto-standards` | Use VBD DTO skill inside VBD scope |
| Existing slice violates VBD boundaries | `vbd-boundary-contract-mapping` | `vbd-architecture-conformance` | Load corrective skill first |
| Architecture rule audit or drift check | `vbd-architecture-conformance` | `vbd-system-design` | Load audit skill first |

## Load Rules

1. Agent loads **one primary skill first**.
2. Agent loads a secondary skill only when the primary skill explicitly lacks the needed rule.
3. Agent does not load peer skills from the same phase unless the request spans multiple boundaries.
4. Agent prefers VBD-specific skills over generic `.NET` skills inside VBD work.
5. Agent uses generic `.NET` skills only for cross-cutting implementation detail after VBD intent is settled.

## Conflict Prevention

| Conflict risk | Prevention |
|---|---|
| Multiple skills define boundary ownership | `vbd-system-design` owns boundary authority |
| Multiple skills define DTO rules | `vbd-dto-authoring` owns VBD DTO rules |
| Generic .NET skill overrides VBD intent | VBD skill takes precedence inside VBD scope |
| Construction and remediation both load | Route by `new` vs `existing` work type first |
