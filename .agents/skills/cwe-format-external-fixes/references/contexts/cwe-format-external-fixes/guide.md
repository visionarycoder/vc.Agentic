---
metadata-version: "1.0.0"
title: "CWE - Untrusted External Code Loading: Consolidated Fixes"
description: "Preserve scoped source guidance for cwe-format-external-fixes."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# CWE - Untrusted External Code Loading: Consolidated Fixes

This skill hardens external code loading by removing ambient search-path dependence.
This skill keeps trusted paths explicit, validated, and least-privilege.

## Remediation Table

| Scenario | Avoid | Preferred |
|---|---|---|
| Native library load | `NativeLibrary.Load("helper")` | `NativeLibrary.Load(trustedAbsolutePath)` |
| Shell execution | `Process.Start("tool.exe")` | `Process.Start(new ProcessStartInfo(trustedAbsolutePath))` |
| PATH mutation | Prepending writable folders to `PATH` | Loading from application-owned, non-writable directories |
| Plugin discovery | Scanning untrusted directories | Allow-listing trusted directories and signed or hashed artifacts |

## Workflow

| Step | Agent action | Output |
|---|---|---|
| 1. Inventory | Agent finds each DLL, executable, script, or plugin load site. | Load-site list |
| 2. Normalize | Agent converts relative or ambient paths into validated absolute trusted paths. | Hardened path strategy |
| 3. Restrict | Agent removes writable search roots, PATH dependence, and silent fallback rules. | Safer loader behavior |
| 4. Validate | Agent runs targeted build and execution checks. | Verified hardening |

## Quality Gate

| Check | Test | Pass criteria |
|---|---|---|
| Explicit paths | Review changed load sites. | Every changed load site uses a trusted explicit path or allow list. |
| Writable roots | Search for changed `PATH` or equivalent edits. | No writable or user-controlled directory is introduced ahead of trusted paths. |
| Failure behavior | Review missing-file handling. | The application fails closed with clear diagnostics. |
| Validation | Run the smallest targeted build or execution test. | Hardened paths resolve correctly in the expected environment. |
