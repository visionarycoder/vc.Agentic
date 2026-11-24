---
title: Credit Markets Handoff
doc_type: reference
status: active
last_updated: 2026-11-23
summary: When a Public Equity Investing workflow keeps credit work as an equity read-through and when it hands off to a Credit Markets plugin.
tags:
  - trading
  - credit
  - handoff
  - risk
---
# Credit Markets Handoff

Public Equity Investing owns listed-equity decisions. Credit-first work belongs to a Credit Markets plugin. This document draws the line and defines the handoff note.

## Stay In Public Equity

Handle these here as equity read-throughs:

- Refinancing stress, leverage, liquidity runway, or solvency pressure as a driver of equity value, risk, or catalysts.
- Net debt, interest burden, maturity walls, and capital-allocation effects in valuation or scenarios.
- Equity-risk signals from credit markets, such as spread moves or rating actions, used as inputs to thesis, sizing, or hedging.
- Listed-equity expression of a distressed or special situation, including event path and catalyst timing.

## Hand Off To Credit Markets

Route to a Credit Markets plugin when the primary job is:

- Credit memos, credit-first pitches, or credit committee styles.
- Covenant analysis, add-back review, or documentation terms.
- Debt-security selection, relative value, bond price, or yield and spread work.
- Capital-structure waterfall and recovery value.
- Default, restructuring, or liability-management analysis where the security is debt.

## Mixed Requests

1. Complete the equity read-through the user needs.
2. State the credit questions that remain and mark them for handoff.
3. Do not attempt covenant, recovery, or debt-security conclusions with equity tools.

If a request is credit-first with equity as a side question, hand off the lead and keep only the equity read-through here.

## Availability

- Use a Credit Markets plugin only if it is actually available in the current runtime. Do not assume or claim access.
- If it is unavailable, say so plainly, provide the equity-side analysis, and list the exact inputs a credit specialist would need.
- Do not substitute equity heuristics for credit analysis.

## Handoff Note

Include these items, in investor language:

- **Issuer and securities:** the ticker, issuer, and debt instruments in question.
- **Question for credit:** the specific decision or analysis requested.
- **Equity context:** thesis, position or watchlist status, and what a credit answer would change.
- **Evidence in hand:** sourced facts, as-of dates, and source posture.
- **Missing inputs:** covenant definitions, indenture or credit-agreement terms, debt schedules, prices, or recovery assumptions that are absent.
- **Blocked items:** conclusions that depend on unsupported add-backs or missing terms.

## Artifacts

- Workbooks with credit-instrument data mark `route_to_credit_markets` on the cover and checks tab, per `workbook-artifact-standard.md`.
- Portfolio and risk recommendations that depend on credit evidence list a missing Credit Markets handoff input under missing evidence.
- Credit memo style stays in Credit Markets unless the artifact is only a public-equity read-through.
