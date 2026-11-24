---
title: Equity Research Support Standard
doc_type: reference
status: active
last_updated: 2026-11-23
summary: Common obligations for support-layer source, data, QA, and style work that feeds Public Equity Investing deliverables.
tags:
  - trading
  - support
  - evidence
  - quality
---
# Equity Research Support Standard

Applies to the support layer: `financial-source-of-truth`, `excel-data-cleaner`, `trading-financials-normalizer`, `trading-deck-report-qc`, and style and rendering helpers. It sets the obligations they share. Routing between them is in `support-layer-routing-contract.md`.

## Role Of Support

- Support serves an owning listed-equity workflow. It does not make the investment decision or change the conclusion.
- Support output is a support artifact with its own readiness posture, such as an evidence ledger, cleaned table, normalized schedule, QC pack, or restyled file.
- Support does not expand scope. Do only the source, data, QA, or style work that was assigned.

## Evidence Labels

Label every load-bearing item as one of:

- `reported`: from a filing, release, or company disclosure.
- `provider`: from a market-data or estimates provider.
- `consensus` or `guidance`: street estimates or management outlook.
- `estimate` or `assumption`: analyst-derived and flagged as such.
- `inferred`: derived from other evidence, with the logic shown.
- `missing` or `conflicted`: not available, or sources disagree.

## Source Hierarchy And Freshness

- Prefer primary company documents for reported facts, then provider data, then secondary sources.
- Record source, document or field, period, as-of timestamp, and retrieval status.
- State the as-of time for market data, consensus, and share counts. Mark stale items.
- Resolve conflicts by hierarchy and recency, and show the rejected value and reason. Do not silently average or overwrite.
- Source-selection rules follow `workflow-source-resolution.md`.

## Identifier And Unit Preservation

- Preserve ticker, exchange, issuer, period, fiscal-year basis, currency, scale, units, signs, and timestamps through every transformation.
- Do not drop decision-critical detail such as footnotes, adjustments, segment definitions, or restatement flags.
- Record each transformation so it can be traced and replayed.

## Change Control

- Restyling must not change facts, formulas, citations, or investment conclusions.
- Data cleaning must not change meaning. Flag ambiguous values instead of guessing.
- Report what changed, what was left alone, and what needs a human decision.

## QA Posture

- QA is first-pass issue finding: prioritize issues, cite locations, and suggest fixes. Rewrite or rebuild only when the user asks for remediation.
- A heuristic or script check alone does not make a deliverable externally circulable.
- State readiness plainly: ready, ready with caveats, or not ready, with the blocking reasons.

## Reader Language

- Write for a portfolio manager or analyst. Avoid internal terms such as `source_category_plan` or `next_action` in reader-facing text.
- Report limitations, missing sources, and confidence directly.

## Credit Boundary

Credit-first conclusions and credit-instrument data follow `credit-markets-handoff.md`.
