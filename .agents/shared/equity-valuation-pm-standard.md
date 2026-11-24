---
title: Equity Valuation PM Standard
doc_type: reference
status: active
last_updated: 2026-11-23
summary: Required decision content and discipline for public-equity model, valuation, scenario, model-update, and audit outputs.
tags:
  - trading
  - valuation
  - modeling
  - standard
---
# Equity Valuation PM Standard

Applies to substantial model, valuation, scenario, model-update, or audit work, together with `pm-judgment-heuristics.md`. Models are decision tools; the output must say what the numbers mean for the stock.

## Required Decision Content

Every substantial output states:

1. **What the current price implies:** market-implied growth, margin, return, or multiple expectations.
2. **Variant estimate path:** where the estimates or assumptions differ from consensus or the street, and why.
3. **Source of upside:** whether it comes from fundamentals, multiple expansion, mix, capital return, sentiment, or event probability.
4. **What breaks first in downside:** the weakest assumption and its leading indicator.
5. **Valuation posture and next underwriting step.**
6. **What changes target, rating, sizing, hedge, trim, exit, or watchlist status.** State this only when the user requests portfolio action or supplies the holding, benchmark, mandate, and liquidity context.
7. **What evidence is missing.**

## Valuation Discipline

- Show the bridge from enterprise value to equity value per share, including net debt, leases, minorities, and diluted share count, each sourced.
- Keep period, currency, units, fiscal-year basis, and calendarization explicit.
- Label each input as reported, provider, consensus, management guidance, estimate, or judgment.
- Cross-check the answer against an alternative method, such as comps against DCF, and explain gaps.
- Show sensitivity to the two or three drivers that matter most, and not a grid of everything.
- Treat terminal value and WACC as assumptions to defend. Report terminal share of value.
- Use scenarios with distinct causal drivers and stated probabilities where used. Do not set scenarios by scaling one number.
- Peer sets state selection logic, metric definitions, outlier treatment, and the as-of date of market data.

## Model Integrity

- Prefer formula-first workbooks that follow `workbook-artifact-standard.md`.
- Include balance, cash, and sign checks. Report failures on the cover.
- When updating an existing model, preserve structure and formulas, map each change to a source, and log before and after values.
- Separate reported actuals from forecasts and flag restatements and non-GAAP adjustments.
- Do not tune assumptions to reach a target. Backsolves are labeled as such.

## Evidence And Freshness

- Use `financial-source-of-truth` for source ranking and conflict resolution.
- Use `trading-financials-normalizer` and `excel-data-cleaner` when inputs are messy, following `support-layer-routing-contract.md`.
- State the as-of date for prices, consensus, and share counts. Stale load-bearing data is flagged, not used silently.

## Audit And Review

- For audit or tie-out work, report findings by severity with cell or source references and a recommended fix.
- Do not claim a model is audited or circulation-ready from a heuristic check alone.
- Credit-instrument valuation or recovery math follows `credit-markets-handoff.md`.
