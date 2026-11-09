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

## When Not to Use

| Prompt Pattern | Agent Route |
|---|---|
| Only debits, credits, or chart of accounts | `accounting-double-entry` |
| Only journal workflow design | `accounting-journal-entry-patterns` |
| Only GAAP statements or CAFR reporting | `accounting-financial-reporting-gaap` |

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
| Debits, credits, posting rules, chart design | Yes | `accounting-double-entry` |
| Chart of accounts structure, segments, numbering | Yes | `accounting-chart-of-accounts-design` |
| Journal intake, approval, posting, reversal, correction | Yes | `accounting-journal-entry-patterns` |
| Adjustment entries: correcting, accrual, reclassification | Yes | `adjustment-entry-patterns` |
| Bank, subledger, or intercompany tie-out | Yes | `accounting-reconciliation-patterns` |
| Subledger-to-GL reconciliation, break detection | Yes | `accounting-subledger-reconciliation-patterns` |
| Interfund transactions, due to/from, eliminations | Yes | `accounting-interfund-patterns` |
| Multi-currency, FX translation, remeasurement | Yes | `accounting-multi-currency` |
| Sales tax, use tax, tax jurisdiction, 1099 reporting | Yes | `accounting-tax-patterns` |
| Month-end, year-end, or close checklist | Yes | `accounting-closing-cycle-patterns` |
| Controls, approvals, evidence, audit trail, segregation | Yes | `audit-trail-compliance` |
| Governmental, GASB, budgetary, or grant accounting | Yes | `accounting-public-sector` |
| Fund setup, restriction tracking, or fund balance logic | Yes | `accounting-fund-patterns` |
| Appropriation, allotment, encumbrance, budget variance | Yes | `accounting-budget-to-actual-tracking` |
| Financial statements, note support, CAFR outputs | Yes | `accounting-financial-reporting-gaap` |

## Coverage Matrix

| Need | Specialist Skill | Primary Outcome |
|---|---|---|
| Ledger foundation | `accounting-double-entry` | Balanced posting model and chart of accounts |
| Chart structure | `accounting-chart-of-accounts-design` | Account numbering, segments, hierarchy, roll-up rules |
| Entry workflow | `accounting-journal-entry-patterns` | Draft-to-post lifecycle with reversals and corrections |
| Adjustment entries | `adjustment-entry-patterns` | Correcting, accrual, reclassification, prior period adjustments |
| Matching and tie-out | `accounting-reconciliation-patterns` | Deterministic reconciliation flow and exception handling |
| Subledger control | `accounting-subledger-reconciliation-patterns` | AR, AP, Payroll, Fixed Assets to GL reconciliation |
| Interfund transactions | `accounting-interfund-patterns` | Due to/from, transfers, eliminations for consolidated reporting |
| Multi-currency | `accounting-multi-currency` | FX translation, remeasurement, gain/loss recognition |
| Tax accounting | `accounting-tax-patterns` | Sales tax, use tax, jurisdiction-based calculation |
| Period governance | `accounting-closing-cycle-patterns` | Controlled close calendar and cutoff rules |
| Controls and evidence | `audit-trail-compliance` | Traceability, approvals, and segregation boundaries |
| Government model | `accounting-public-sector` | GASB-aligned accounting structure |
| Fund model | `accounting-fund-patterns` | Fund classification and restriction tracking |
| Budget control | `accounting-budget-to-actual-tracking` | Encumbrance and variance tracking against authority |
| External reporting | `accounting-financial-reporting-gaap` | Statements, schedules, and CAFR-ready outputs |

## Decision Matrix: Commercial vs Public Sector Accounting

| Signal | Commercial Path | Public Sector Path |
|---|---|---|
| Primary basis | Investor, lender, or management reporting | Accountability, legal compliance, and public stewardship |
| Core standards | GAAP | GASB plus agency policy |
| Budgetary control | Optional management control | Core accounting dimension |
| Fund separation | Rare | Frequent or required |

## Decision Matrix: When to Use Fund Accounting

| Condition | Use Fund Accounting | Route |
|---|---|---|
| Resources carry legal, grant, donor, or statutory restrictions | Yes | `accounting-fund-patterns` |
| Entity tracks independent self-balancing pools | Yes | `accounting-fund-patterns` |
| Governmental reporting requires fund statements | Yes | `accounting-public-sector` + `accounting-fund-patterns` |
| One unrestricted commercial ledger fits the model | No | `accounting-double-entry` |

## Decision Order

| Decision | Agent Action |
|---|---|
| Commercial entity with one unrestricted ledger | Agent starts with `accounting-double-entry`, then `accounting-journal-entry-patterns`, `accounting-reconciliation-patterns`, `accounting-closing-cycle-patterns`, and `accounting-financial-reporting-gaap`. |
| Public sector entity with GASB reporting | Agent starts with `accounting-public-sector`, then `accounting-fund-patterns`, `accounting-budget-to-actual-tracking`, `accounting-journal-entry-patterns`, `accounting-closing-cycle-patterns`, and `accounting-financial-reporting-gaap`. |
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
| Treating governmental accounting as commercial accounting with extra fields | Agent routes first to `accounting-public-sector` and `accounting-fund-patterns`. |
| Deferring budgetary control until reporting | Agent routes early to `accounting-budget-to-actual-tracking`. |
| Using reports as the source of reconciliation truth | Agent anchors reconciliation in operational accounting records. |
| Publishing Fabric models straight from unstable journal drafts | Agent publishes from posted and controlled accounting facts only. |
