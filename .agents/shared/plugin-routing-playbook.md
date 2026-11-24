---
title: Plugin Routing Playbook
doc_type: reference
status: active
last_updated: 2026-11-23
summary: Selects one lead Public Equity Investing skill, its artifact hierarchy, and the supporting skills to sequence.
tags:
  - trading
  - routing
  - workflows
  - playbook
---
# Plugin Routing Playbook

Used after the gate in `invocation-policy.md` passes. Select one lead skill, preserve its artifact hierarchy, and load supporting skills only for the workstreams the lead assigns. The router skill map holds the full skill descriptions.

## Selection Rules

1. Pick the narrowest lead skill that owns the user's decision and hero artifact.
2. The lead owns the final artifact. Other skills provide inputs and do not compete for first read.
3. Ask only when the answer changes the lead owner, hero artifact, evidence path, or reliance standard. Use the choice sets in `deliverable-intake-policy.md`.
4. If the user names a skill, use it unless it clearly cannot do the job.
5. Do not answer from the router alone when a focused owner exists.

## Intent To Lead Skill

| Intent | Lead skill |
| --- | --- |
| Cited issuer profile or fact pack | `trading-company-tearsheet` |
| Full initiation, target-price framework | `trading-initiating-coverage` |
| Pre-print setup | `trading-earnings-preview` |
| Post-print analysis and action | `trading-earnings-deep-dive` |
| Update an existing model | `trading-equity-model-update` |
| Peer valuation | `trading-comps-valuation` |
| DCF and price-target support | `trading-dcf-model-builder` |
| Forecast model build | `trading-three-statement-model-builder` |
| Long, short, or pair pitch | `trading-long-short-pitch` |
| Screens and watchlist triage | `trading-idea-generation` |
| Thesis monitoring | `trading-thesis-tracker` |
| Dated catalysts | `trading-catalyst-calendar` |
| Event and special-situation underwriting | `trading-event-driven-analyzer` |
| Sizing, hedging, risk budget | `trading-portfolio-risk-management` |
| Scenarios and sensitivities | `trading-scenario-sensitivity-generator` |
| Macro or policy read-through | `trading-economic-impact-report` |
| PM or IC memo, thesis update | `trading-memo-builder` |
| Meeting or call prep | `trading-meeting-prep` |
| Normalize financials | `trading-financials-normalizer` |
| Model audit or tie-out | `trading-model-audit-tieout` |
| Deck or report QC | `trading-deck-report-qc` |

Saved preferences and source setup go to `user-context`. Plugin workflow tests go to `test-public-equity-investing-workflows`, only on explicit request.

## Sequencing

- **Before analysis:** source resolution (`workflow-source-resolution.md`), then evidence and data support if inputs are messy.
- **Build:** the lead produces the hero artifact. Models and calculations come from model owners, such as comps, DCF, or three-statement skills.
- **Synthesis:** memos and decks import analysis from owning skills and do not recompute it.
- **Review:** model audit before relying on a model, and deck or report QC before circulation.
- **After:** end with one next step, such as QC, a refresh, or a model or memo to add.

Typical chains:

- Earnings: preview, then deep dive, then model update, then thesis tracker.
- Valuation: financials normalizer, then comps or DCF, then scenarios, then memo.
- Pitch: idea generation, then pitch, then risk management, then thesis tracker.
- Event: catalyst calendar, then event-driven analysis, then scenarios.

## Artifact Hierarchy

- Final artifact surface follows `final-deliverable-framework.md`.
- Support artifacts follow `support-layer-routing-contract.md`.
- Workbooks follow `workbook-artifact-standard.md`, and HTML follows `html-artifact-standard.md`.
- Substantial judgment applies `pm-judgment-heuristics.md`, and valuation work applies `equity-valuation-pm-standard.md`.

## Redirects

- Credit-first work goes to Credit Markets per `credit-markets-handoff.md`.
- Private-company diligence, personal financial advice, and generic drafting are outside the plugin.
