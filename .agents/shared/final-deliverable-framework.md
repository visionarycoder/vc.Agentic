---
title: Final Deliverable Framework
doc_type: reference
status: active
last_updated: 2026-11-23
summary: How an owning workflow selects, structures, and finalizes the investor-facing hero artifact and its supporting artifacts.
tags:
  - trading
  - deliverables
  - artifacts
  - judgment
---
# Final Deliverable Framework

Applied by the lead skill after routing, for substantive investment judgment. It decides what the user reads first, what supports it, and what must be true before it is final. Intake choices come from `deliverable-intake-policy.md`.

## Principles

- One lead skill owns one hero artifact. Other skills supply inputs and do not compete to be the first read.
- The artifact answers a decision question: what is priced in, what the view is, what proves or kills it, and what to do or watch next.
- Judgment comes before volume. Cut material that does not change the decision.
- Evidence supports the conclusion and is visible, not buried.

## Surface Selection

| Need | Surface | Standard |
| --- | --- | --- |
| Reusable, source-heavy, or web-style report | Standalone HTML | `html-artifact-standard.md` |
| Formal IC, committee, client, or research memo | Word `.docx` | Workflow template |
| Model, comps, tracker, or valuation | Excel `.xlsx` | `workbook-artifact-standard.md` |
| Quick or conversational answer | Chat | Concise, sourced |
| Presentation to an audience | Deck | Workflow template, then QC |

- An explicit user request overrides the default. A resolved intake choice overrides inference.
- Create a workbook only when the user selects or clearly implies a model, tracker, valuation, or workbook surface.
- Offer additional surfaces as next steps rather than producing all of them.

## Structure Of A Hero Artifact

1. **Answer:** stance, posture, or conclusion in a few lines.
2. **Why now:** the setup, catalyst, or change that makes the view timely.
3. **Evidence:** sourced facts, with assumptions and judgment labeled separately.
4. **Valuation or payoff:** what is priced in and what the view implies.
5. **Risks and disconfirming evidence:** what breaks first and the triggers that prove or kill the thesis.
6. **Action or watch list:** next steps, and portfolio action only when the user supplies the holding and mandate context.
7. **Limits:** source posture, missing evidence, and readiness.

Adapt order and depth to the workflow. Do not pad sections that have no content.

## Supporting Artifacts

- Models and workbooks feed the hero artifact and carry their own `Cover`.
- Evidence ledgers, normalized tables, and QC logs are appendices or companion files unless requested as the main output.
- A memo or deck imports analysis from the owning skills and does not recompute it.

## Finalization

- Apply `pm-judgment-heuristics.md` before finalizing substantial work.
- Resolve open conflicts, or show them. Do not leave placeholder text.
- Check consistency of numbers, dates, tickers, and units across the artifact and companions.
- Route through `trading-deck-report-qc` before any external circulation.
- State readiness honestly. Do not label output circulation-ready without review.
- End with one short next step tied to the artifact.
