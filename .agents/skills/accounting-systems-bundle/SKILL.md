---
name: "accounting-systems-bundle"
description: "Routes accounting system implementation work to the correct accounting skill set for commercial, public sector, fund, close, control, and reporting scenarios."
metadata:
  metadata-version: "1.0.0"
  title: "Accounting Systems Bundle"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "accounting"
---

# Accounting Systems Bundle

Agent uses this bundle for accounting system work that spans posting rules, period workflows, controls, governmental accounting, budget enforcement, or external financial reporting.

## When to Use

| Prompt Pattern | Use This Bundle |
|---|---|
| New accounting platform or accounting module | Yes |
| Commercial and governmental accounting choice | Yes |
| Journal, reconciliation, close, controls, and reporting in one request | Yes |
| Single accounting topic with no routing need | No |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Entity type | Yes | Commercial, nonprofit, or public sector |
| Reporting basis | Yes | Applicable accounting framework and reporting obligations |
| Ledger scope | Yes | General ledger only, subledgers, budget ledger, or fund ledger |
| Integration surface | No | EF Core, CQRS, domain events, Fabric, external banking, ERP |

## Activation

| Request Signal | Use Bundle | Route Detail |
|---|---|---|
| Subledger-to-GL reconciliation, break detection | Yes | `accounting-subledger-reconciliation-patterns` |
| Month-end, year-end, or close checklist | Yes | `accounting-closing-cycle-patterns` |
| Controls, approvals, evidence, audit trail, segregation | Yes | `audit-trail-compliance` |

## Coverage Matrix

| Need | Specialist Skill | Primary Outcome |
|---|---|---|
| Subledger control | `accounting-subledger-reconciliation-patterns` | AR, AP, Payroll, Fixed Assets to GL reconciliation |
| Period governance | `accounting-closing-cycle-patterns` | Controlled close calendar and cutoff rules |
| Controls and evidence | `audit-trail-compliance` | Traceability, approvals, and segregation boundaries |

## Decision Matrix: Commercial vs Public Sector Accounting

| Signal | Commercial Path | Public Sector Path |
|---|---|---|
| Primary basis | Investor, lender, or management reporting | Accountability, legal compliance, and public stewardship |
| Core standards | GAAP | GASB plus agency policy |
| Budgetary control | Optional management control | Core accounting dimension |
| Fund separation | Rare | Frequent or required |

## Decision Order

| Decision | Agent Action |
|---|---|
| Commercial or public sector entity with period-close needs | Agent starts with `accounting-closing-cycle-patterns`. |
| Control-heavy implementation | Agent adds `audit-trail-compliance` before workflow finalization. |
| Analytics and reporting platform in scope | Agent maps operational ledger events to Fabric semantic, warehouse, or lakehouse outputs after accounting model selection. |

## Integration Patterns

| Concern | Pattern |
|---|---|
| EF Core | Use immutable journal headers and lines, posting batches, reconciliation snapshots, and close status aggregates with explicit concurrency tokens. |
| CQRS | Use commands for draft, approve, post, reverse, close, reopen, reconcile, and budget reserve actions; use read models for trial balance, fund balance, budget variance, and close dashboards. |
| Domain events | Emit `JournalPosted`, `ReconciliationCompleted`, `PeriodClosed`, `BudgetExceeded`, and `FundBalanceChanged` events for downstream controls and reporting. |
| Fabric | Land posted journal, budget, and reconciliation facts in Fabric lakehouse or warehouse; publish semantic models for statements, CAFR schedules, variance analysis, and audit evidence. |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 2. Select ledger model | Agent chooses unrestricted ledger, budget ledger, fund ledger, or mixed model. | Agent maps restrictions and reporting drivers. | Ledger model fits constraints. |
| 3. Add workflow skills | Agent attaches journal, reconciliation, close, and control skills in dependency order. | Agent lists routed skills. | Each operational need maps to one skill. |
| 4. Add reporting path | Agent maps GAAP, GASB, CAFR, and Fabric outputs. | Agent records statement and analytics consumers. | Reporting path covers all consumers. |

## Verification Matrix

| Area | Agent Verifies | Test | Pass |
|---|---|---|---|
| Posting model | Debits equal credits and chart segments align to reporting needs. | Inspect entry rules and sample postings. | All sample postings balance. |
| Workflow | Draft, approval, posting, reversal, and close states are explicit. | Inspect command and state flow. | No hidden state transition exists. |
| Reconciliation | Exceptions, timing items, and adjustments are traceable. | Inspect matching and exception outputs. | Every break has an owner and status. |
| Public sector and funds | Funds, budgetary controls, and GASB outputs align. | Inspect fund model and statement mapping. | Government reporting dimensions reconcile. |

## Common Pitfalls

| Pitfall | Agent Fix |
|---|---|
| Using reports as the source of reconciliation truth | Agent anchors reconciliation in operational accounting records. |
| Publishing Fabric models straight from unstable journal drafts | Agent publishes from posted and controlled accounting facts only. |
