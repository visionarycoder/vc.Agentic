# P0 Integrations

## Source and normalization

Use `financial-source-of-truth` before or alongside this skill when the user provides filings, public data, connected-app data, or multiple source versions. Carry its evidence labels into `source_basis`.

Use `trading-financials-normalizer` when inputs are PDFs, filings, messy statements, VDR exports, accounting reports, or multiple tabs that need mapping into normalized IS/BS/CF.

Use `excel-data-cleaner` before modeling when a workbook has broken headers, inconsistent units, date problems, hidden rows, or raw exports.

## Audit and scenario expansion

Use `trading-model-audit-tieout` when the user asks to review or fix an existing model, or when formulas/hardcodes/signs/source tie-outs require a dedicated audit.

Use `trading-scenario-sensitivity-generator` when the base model is complete and the user wants deeper stress testing, breakeven analysis, severe downside, or tornado-style sensitivity outputs.

## Public Equity Investing

Use `trading-equity-model-update` when updating a public-company model from earnings, guidance, filings, transcripts, consensus, or market data.

Use Credit Markets when credit instruments, creditworthiness, debt stack, maturity wall, liquidity, covenant disclosure, refinancing, distressed, recovery, spreads, yields, or capital-structure analysis is the primary deliverable. Keep this model builder focused on public-company equity models.

Use `trading-dcf-model-builder`, `trading-comps-valuation` when the primary output is intrinsic value, trading comps, SOTP, or valuation range.

Use `trading-thesis-tracker`, `trading-earnings-preview`, or `trading-earnings-deep-dive` when actuals, KPI monitoring, consensus changes, or thesis signals are the primary deliverable.

## Memo and presentation

Use `trading-memo-builder` after the model when the user needs an IC memo, board note, lender memo, client memo, or portfolio update.

Use `trading-deck-report-qc` and `style-guide-adapter` before external circulation.
