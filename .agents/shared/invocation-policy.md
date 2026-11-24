---
title: Invocation Policy
doc_type: reference
status: active
last_updated: 2026-11-23
summary: Gate that decides whether a request belongs to the Public Equity Investing plugin before any specialist is chosen.
tags:
  - trading
  - routing
  - gate
  - invocation
---
# Invocation Policy

The router reads this policy before choosing any specialist. It decides whether a request belongs in Public Equity Investing at all. It does not select the lead skill; that is the job of `plugin-routing-playbook.md`.

## Pass Conditions

The gate passes when either holds:

1. **Explicit invocation:** the user names `@trading-public-equity-investing`, `@Public Equity Investing`, or invokes the plugin directly. Treat this as strong intent, then still check the exclusions below.
2. **Investor context:** the prompt has listed-company, public-security, ticker, sector, portfolio-position, event, earnings, thesis, catalyst, valuation, model-update, or investor-lens context.

If neither holds, do not route into this plugin.

## Fail Or Redirect Conditions

Do not route into this plugin for:

- Private-company diligence.
- Credit-first analysis, such as covenant, debt-security, recovery, or spread work. See `credit-markets-handoff.md`.
- Personal financial advice.
- Generic company summaries or market commentary with no investment decision.
- Generic document, deck, or spreadsheet drafting with no public-equity investment context.

For an explicit invocation with an excluded job, say briefly why the plugin does not fit and offer the closest appropriate route or a plain answer. Do not refuse a listed-equity read-through of a credit or private-market event.

## Ambiguous Prompts

- A bare company or ticker with an investor cue passes the gate.
- A bare company with no investor cue does not. Ask only if the answer would change the routing.
- Prefer a relevant Public Equity Investing sibling when generic research, valuation, modeling, memo, deck, or risk work is really a listed-equity decision.

## After The Gate

1. Read `plugin-routing-playbook.md` and choose one lead skill.
2. Apply `deliverable-intake-policy.md` for a new substantive hero deliverable.
3. Resolve sources per `workflow-source-resolution.md`.
4. Load support through `support-layer-routing-contract.md` as the lead skill directs.

## Boundaries

- Explicit-only constituent skills are used only through this plugin or by direct naming.
- The gate does not authenticate users, grant permissions, or approve actions.
- Do not run user-context preflight as part of the gate.
- Do not expose gate mechanics to the user. Answer in investor language, and when declining, state the practical reason only.
