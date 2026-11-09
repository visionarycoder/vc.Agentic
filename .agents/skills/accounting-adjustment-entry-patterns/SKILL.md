---
name: "accounting-adjustment-entry-patterns"
description: "Design or review accounting adjustments, accruals, reversals, reclassifications, and prior-period error treatment using the applicable reporting framework and entity controls."
metadata:
  metadata-version: "1.0.0"
  title: "Accounting adjustment entry patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "accounting"
---

# Accounting adjustment entry patterns

Use for accounting treatment and control design of adjusting journal entries. This skill is technology-neutral; it does not select .NET, EF Core, MediatR, a schema, or an approval hierarchy. Drafting an entry does not authorize a live ledger posting.

## Establish the accounting basis

Identify the reporting framework and effective version, entity, ledger, reporting period, currencies, source evidence, and whether statements have been authorized or issued. Read approved accounting policies, materiality assessments, approval limits, and period controls. Missing facts may permit a labeled draft, not a definitive posting or restatement conclusion.

Distinguish errors, new estimates, policy changes, and events after the reporting date. Do not combine frameworks or assume the latest published amendment is effective for this entity. The [accounting basis reference](references/accounting-basis.md) identifies primary guidance and applicability.

## Select the treatment

| Category | Decision and evidence |
| --- | --- |
| Correction | Explain the original error, affected accounts/dimensions, recognition period, source linkage, and correcting lines. Preserve posted history. |
| Accrual/deferral | Apply recognition, measurement, and cutoff guidance. An accrual can originate from an unposted economic event. Record calculations, assumptions, settlement, and reconciliation. |
| Reversal | Use when entity policy requires a temporary accrual or estimate to be offset. Link the source, schedule the approved date, and prevent duplicate reversal or duplicate expense on settlement. Not every accrual requires automatic reversal. |
| Reclassification | Assess presentation, profit, cash-flow, tax, fund, and covenant effects where relevant. Balanced lines do not prove every reported subtotal is unchanged. |
| Prior-period error/policy change | Obtain framework-specific assessment of materiality, retrospective treatment, comparatives, opening balances, disclosure, and applicable impracticability exceptions. A locked ledger does not justify placing a material prior-period error in current profit. |
| Estimate change | Distinguish new information from misuse of information previously available. Applicable IFRS guidance generally treats estimate changes prospectively rather than as error restatements. |
| Subsequent event | Determine whether evidence concerns conditions at the reporting date and apply the relevant adjustment/disclosure rules. |

Do not use a percentage as the sole materiality rule. Assess qualitative factors, aggregation, affected periods, and applicable regulatory guidance. Route unresolved accounting judgments to the responsible finance professional.

## Preparation, approval, and posting controls

1. Prepare entity/ledger, business date, proposed period, currency/precision policy, account/dimension lines, source references, calculations, rationale, treatment basis, and expected reporting impact.
2. Validate debit/credit balance at required ledger/currency granularity, valid dimensions, intercompany/fund balancing, and approved rounding/FX treatment. Do not hard-code two decimal places for every currency or ledger.
3. Apply entity authorization and segregation of duties, with approved compensating controls where applicable. Bind reviews to the actual journal revision and support. One approval does not satisfy a multi-step policy; a role label does not authenticate its holder.
4. Respect open, soft-close, hard-close, and issued-statement controls. Determine accounting treatment before selecting a posting path. Do not replace required reopening, comparative restatement, or disclosure with automatic current-period routing. A reversal date in a closed period requires authorized resolution rather than a silent date shift.
5. Before authorized posting, recheck approvals, journal revision, period state, and idempotency. Design atomic ledger/state updates and reliable audit evidence under failure and concurrency. Describe undelivered controls as requirements, not implemented protection.
6. Preserve posted records and links among corrections, replacements, reversals, and settlements. Retain who prepared, reviewed, approved, and posted, when, why, and under which basis. Include consolidation and presentation adjustments outside the formal ledger.
7. Reconcile results to ledger/subledger totals, trial balance, support schedules, and financial statements. Track pending reversals and settlement differences through close.

## Example and verification

For a supported expense of 1,000 incurred before period end but not yet invoiced, a draft accrual might debit expense and credit an accrued liability for 1,000. This assumes the entity's recognition, currency, and cutoff policies support that treatment. Reconcile settlement against the accrual using approved reversal or direct liability-clearing treatment so expense is not counted twice.

Verify relevant cases: unsupported/unbalanced drafts; disallowed self-approval; journal changes after approval; period closure before posting; retry after partial failure; duplicate reversal; settlement after accrual; reclassification affecting statement lines; material prior-period error; and new estimate information. Report actual results and missing evidence.

Return classification/basis, draft journal and evidence, judgments requiring finance review, control requirements, posting/reversal/reconciliation plan, and verification results. A draft or example does not establish compliance, audit assurance, approval, or live posting.
