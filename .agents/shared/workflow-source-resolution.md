---
title: Workflow Source Resolution
doc_type: reference
status: active
last_updated: 2026-11-23
summary: How a workflow resolves only the source categories it needs, chooses a route, and labels the resulting source posture.
tags:
  - trading
  - sources
  - connectors
  - evidence
---
# Workflow Source Resolution

Workflow-scoped source setup for Public Equity Investing. Connect or request only the source categories the selected workflow actually needs. The runtime contract in `trading-public-equity-investing/SKILL.md` defines the categories; this document defines how a workflow applies them.

## Categories

| Label | Legacy id | Covers |
| --- | --- | --- |
| Market Data & Estimates | `market_data_estimates` | Prices, estimates, ownership, benchmarks, factors, comparable-company evidence |
| Company Filings & IR | `company_filings_ir` | Filings, investor presentations, reported fundamentals, KPI disclosures |
| Earnings Transcripts & Events | `earnings_transcripts_events`, `earnings_transcripts_presentations` | Calls, management remarks, investor days, conferences, release calendars |
| Portfolio Models & Trackers | `portfolio_models_trackers` | Existing models, watchlists, trackers, exports, workpapers |
| Internal Research | `internal_research` | Analyst notes, PM discussions, meeting notes, saved theses |

Labels and legacy ids are interchangeable.

## Resolution Steps

1. List only the categories the current workflow needs. Do not resolve categories "just in case".
2. Prefer a user-named source first.
3. Otherwise choose one available app, connector, file, export, or pasted input that satisfies the category. An app satisfies a category when its declared category matches.
4. Prefer canonical finance plugins or provider-specific guidance over raw connectors when they add workflow support.
5. Attempt the smallest useful native read-only check, and only when the workflow needs that source.
6. Broaden to additional sources only when the first pass is empty, thin, conflicting, stale, or decision-relevant.

## Readiness Rules

- A successful read is run-specific evidence, not durable setup state. Do not claim a source is ready without a read in this run.
- A declared dependency does not prove a source is installed, authorized, or readable.
- Do not use browser automation, screenshots, or mirrored adjacent sources as readiness proof.
- Do not silently substitute a weaker category for a stronger required one.

## When A Source Is Unavailable

- If a route needs authentication, connection, or setup, state the practical limitation in analyst language.
- Continue from user-provided or public context when a limited answer is still useful, and label the posture.
- Request a specific export or file when that would close the gap. Use `request_plugin_install` only when an available plugin or connector would solve a material missing category.
- Stop only when the missing source owns a required input that cannot be supplied or reliably inferred.

## Source Posture Labels

State one posture in the deliverable:

- **Connected:** the needed categories were read through live connectors.
- **User-supplied:** files, exports, or pasted context were the evidence.
- **Public only:** public documents without provider data.
- **Mixed:** a combination, with each part labeled.

Keep provider and source provenance, as-of dates, and any gap beside each load-bearing claim. Use `financial-source-of-truth` for source ranking and conflict handling.

## Provider Guides

Load a provider guide only after the workflow attempts a category, selects that provider as the concrete route, and confirms the route is callable in the current run. For providers without a bundled guide, follow the live tool surface and do not invent access.

## User Context

Do not run user-context setup or inspection during ordinary workflows. Saved preferences are optional accelerators. Route explicit save, recall, reset, or source-setup requests to the `user-context` skill.
