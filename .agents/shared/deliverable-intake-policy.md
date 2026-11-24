---
title: Deliverable Intake Policy
doc_type: reference
status: active
last_updated: 2026-11-23
summary: Adaptive preflight for resolving format, depth, audience or use, and focus before a substantive Public Equity Investing deliverable.
tags:
  - trading
  - intake
  - preflight
  - deliverables
---
# Deliverable Intake Policy

Adaptive intake for a new substantive hero deliverable. Ask only about choices that are materially unresolved and that change the lead owner, hero artifact, evidence path, reliance standard, or user action.

## Who Runs It

- The owning workflow reads this policy before source gathering or analysis for a new substantive hero deliverable.
- Support, presentation, QC, and sub-workflow skills inherit resolved choices and do not re-prompt.
- Narrow, quick, conversational, or follow-up requests skip the preflight and use the workflow default.
- Run it once per deliverable. Reuse resolved preferences downstream and in later turns unless the user changes them.

## Choice Dimensions

Resolve only the dimensions the request leaves open.

| Dimension | Typical options |
| --- | --- |
| Format | Chat answer, polished standalone HTML, Word `.docx`, Excel `.xlsx`, deck, or a combination |
| Depth | Quick take, standard, or full decision-grade |
| Audience or use | PM decision, IC or committee circulation, client-facing, sell-side style, or personal working file |
| Focus | The thesis, event, period, section, or question that gets the most weight |

## Inference Before Asking

1. Take explicit user statements first: named format, audience, depth, ticker, or period.
2. Apply the workflow's documented default surface when the request is substantive and the signal is high-confidence.
3. Infer from context such as an attached model, a memo for committee, or a "quick" cue.
4. Ask only if the remaining ambiguity changes the deliverable.

Do not ask merely because several skills or formats could work. Do not ask about facts you can find or reasonably assume.

## Asking

- Use `request_user_input` when available. Send all materially unresolved questions together in one call, with at most a few bounded questions.
- Put the recommended option first and label it `(Recommended)`. Make options short and investor-readable.
- Set `autoResolutionMs` so an unanswered picker resolves to the recommended option. Let the chosen or timeout-resolved option control the deliverable.
- If `request_user_input` is unavailable or errors, ask the same questions together in the next normal response, with defaults first, and wait for the answer.
- For open-ended gaps such as an unknown ticker or portfolio context, ask one concise plain-text message grouping every missing item.
- Do not narrate internal setup. Use portfolio-manager or analyst language.

## Material Ambiguity Choice Sets

Use these when the lead workflow, first-read artifact, source posture, or risk or event mode stays ambiguous after routing.

- **Lead workflow:** the narrowest listed-equity owner that fits, with the main alternative as a second option.
- **First-read artifact:** the recommended surface for the workflow, then the next best, then chat summary.
- **Source posture:** connected sources first, then user-supplied files or exports, then public evidence only, with the reliance limit stated for each.
- **Risk or event mode:** thesis-preserving versus action-oriented, or the event type that sets probability, payoff, and timing treatment.

Each set recommends one option, explains the practical consequence in a clause, and avoids more than four options.

## Defaults

- Substantive reusable reports, source-heavy work, and multi-item calendars or screens default to a polished standalone HTML report following `html-artifact-standard.md`.
- Formal IC, committee, client, or research memo circulation defaults to a real Word `.docx`.
- Models, trackers, and valuation work default to a workbook following `workbook-artifact-standard.md`.
- Quick or conversational requests default to chat. Markdown is formatting, not the deliverable contract.
- The workflow's own documented default overrides these when it is more specific.

## After Resolution

- Record the resolved format, depth, audience, and focus in the working notes so downstream skills inherit them.
- Route final artifact selection through `final-deliverable-framework.md`.
- Continue with source resolution per `workflow-source-resolution.md`.
- If the user later asks for a different surface, regenerate from the same analysis instead of re-running the research.
