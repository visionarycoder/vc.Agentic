---
title: Support Layer Routing Contract
doc_type: reference
status: active
last_updated: 2026-11-23
summary: Which support skill an owning workflow calls for source, data, QC, and style work, and how results return to the owner.
tags:
  - trading
  - routing
  - support
  - contract
---
# Support Layer Routing Contract

Defines how an owning Public Equity Investing workflow calls support services. Shared obligations are in `equity-research-support-standard.md`. Support is called only when the workflow needs it, and the owner keeps the decision.

## Support Map

| Need | Support skill | Call before |
| --- | --- | --- |
| Source ranking, freshness, conflicts, citations, evidence labels | `financial-source-of-truth` | Final claims, metrics, citations, management assertions, or changing thesis status on new evidence |
| Messy public-company financials, KPIs, consensus or guidance, segments, share count, net debt, capital allocation | `trading-financials-normalizer` | Building a model, plan, or comps from raw inputs |
| Malformed tables, CSV or XLSX cleanup, ownership, short-interest, or market-data exports | `excel-data-cleaner` | Relying on a table in a workbook or analysis |
| Model audit, formula checks, source tie-out | `trading-model-audit-tieout` | Relying on or circulating a model |
| Deck or report quality control and circulation readiness | `trading-deck-report-qc` | External or senior circulation |
| Standardized dashboard rendering | `dashboard-builder` | Only when a standardized dashboard is requested |
| Style application, sector lens, provider call shaping | Internal playbooks listed in `internal-support/policy.md` | Only after the owner and route are set |

## Calling Rules

1. The owner decides what support is needed. Do not call everything by default.
2. Order: source and evidence first, then data preparation, then build or analysis, then audit, then QC, then style or rendering.
3. Pass the support skill the ticker, period, units, as-of date, source posture, and the downstream use of its output.
4. Support does not re-prompt the user for choices already resolved by `deliverable-intake-policy.md`.
5. Provider guides load only after a category is attempted, the provider is selected, and the route is confirmed callable. See `workflow-source-resolution.md`.

## Standalone Support Requests

- When the user asks only for support, such as cleaning an equity workbook, checking sources, or applying a style guide, the root router coordinates it and loads the matching playbook.
- Use `standalone_support_request` as the owning workflow where a playbook requires one.
- Preserve the support artifact's readiness rules. Do not turn a support request into a full research deliverable.

## Return Contract

Support returns to the owner:

- The support artifact or corrected inputs.
- Evidence labels, source IDs, and as-of dates.
- Conflicts, gaps, and flags that remain open.
- Readiness: ready, ready with caveats, or not ready, with reasons.
- A list of changes made, for cleaning and restyling.

The owner incorporates the result, keeps the open flags visible, and does not upgrade confidence beyond what support reported.

## Limits

- Support does not change investment conclusions, formulas, or citations as a side effect.
- Credit-first conclusions route to Credit Markets per `credit-markets-handoff.md`.
- Visible skills such as `trading-financials-normalizer` and `trading-model-audit-tieout` also serve direct user requests. Keep standalone requests with them.
