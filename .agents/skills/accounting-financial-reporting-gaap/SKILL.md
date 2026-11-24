---
name: "accounting-financial-reporting-gaap"
description: "Build GAAP-aligned financial statement, note, and annual report outputs when work needs statement assembly, disclosures, RSI, or statistical reporting patterns."
metadata:
  metadata-version: "1.0.0"
  title: "Financial Reporting GAAP"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "accounting"
---

# Financial Reporting GAAP

Agent assembles GAAP-aligned financial statements, notes, MD&A support, RSI, and comprehensive annual reporting datasets with public sector awareness.

## When Not to Use

| Condition | Route |
|---|---|
| Work item focuses on foundational governmental accounting treatment | Use `accounting-public-sector` |
| Work item focuses on fund structures and interfund logic | Use `accounting-fund-patterns` |
| Work item focuses on budget execution and encumbrance control | Use `accounting-budget-to-actual-tracking` |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Reporting basis | Yes | Record governmental GAAP, proprietary accrual, or mixed package scope. |
| Statement package | Yes | Record statements, notes, MD&A, RSI, and statistical sections in scope. |
| Close status | Yes | Record preliminary, adjusted, final, or issued close stage. |
| Comparative periods | Yes | Record current year, prior year, and trend-year requirements. |
| Disclosure topics | No | Record debt, capital assets, leases, pensions, commitments, and contingencies in scope. |

## Workflow

| Step | Action | Pass |
|---|---|---|
| 1 | Map statements, notes, MD&A support, RSI, and statistical schedules. | Every requested section has named datasets and owners. |
| 2 | Align each section to the selected GAAP and public-sector view. | Basis, presentation, and disclosures match the reporting objective. |
| 3 | Trace statement lines and note support to closed-ledger and subledger sources. | Published amounts remain lineage-safe and reproducible. |
| 4 | Build narrative, comparative, and trend measures from governed datasets. | MD&A, RSI, and statistical sections avoid ad hoc spreadsheet-only values. |
| 5 | Validate cross-statement ties, disclosure completeness, and issue-state controls. | Statements, notes, and trend schedules reconcile across the package. |

## Package Structure

A comprehensive annual report package contains statements, notes (structured note-support schedules with line references and disclosure checklists for debt, capital assets, leases, pensions, commitments, contingencies), MD&A, RSI, and a statistical section (long-horizon trends with consistent dimensions), all versioned together.

## Public Sector Specific Patterns

| Pattern | Implementation |
|---|---|
| Package versioning | Store issuance state, period, and package version on report artifacts. |
| Note-support datasets | Persist disclosure schedules with line references. |
| Fund and government-wide ties | Maintain reconciliation tables between presentation layers. |
| RSI and statistical persistence | Snapshot issued-year trends by schedule definition. |
| Narrative support | Publish approved measures and definitions for authors. |

## Integration Hooks

| Surface | Output |
|---|---|
| EF Core | Close packages, statement mappings, note schedules, disclosure topics, and issuance states |
| Microsoft Fabric | Statement lines, note schedules, MD&A metrics, RSI schedules, and trend datasets |
| Report generation services | Deterministic close, assembly, narrative binding, and publication pipeline |

## Verification Checklist

| Check | Test | Pass |
|---|---|---|
| Publication control | Review package version and issue state. | Issued packages stay immutable and reproducible; track release state per section. |

## Outputs

| Output | Description |
|---|---|
| Package map | Statements, notes, MD&A, RSI, and statistical layout |
| Lineage model | Source-to-statement and source-to-note traceability |
| Integration plan | EF Core, Fabric, and report-build design |
| Verification plan | Reconciliation, completeness, and publication-control checks |
