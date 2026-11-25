---
title: HTML Artifact Standard
doc_type: reference
status: active
last_updated: 2026-11-23
summary: Quality bar for bespoke standalone HTML artifacts produced by Public Equity Investing workflows.
tags:
  - trading
  - html
  - artifacts
  - quality
---
# HTML Artifact Standard

Shared principles for polished, legible, evidence-aware standalone HTML artifacts such as tearsheets, catalyst calendars, trade pitches, scenario reports, event reports, economic-impact reports, risk plans, and memos. The owning workflow decides the content and structure; this standard sets the quality bar.

## When To Use

- Use when a workflow default, an explicit user request, or the intake preflight resolves the presentation surface to HTML.
- Do not force a fixed module inventory or the standardized dashboard shell. The decision and the primary analytical object determine the layout.

## Standalone Requirements

- Produce one self-contained `.html` file. Inline CSS and any JavaScript, and embed images or charts as inline SVG or data URIs.
- Do not depend on external CDNs, fonts, trackers, or network calls at view time. Use system font stacks.
- Open without a server, work offline, and keep the file small enough to share by email.
- Do not embed secrets, credentials, personal data, or unrelated workspace paths.

## Reading Order

- Put the decision, conclusion, or answer first: stance, valuation posture, what is priced in, and what changes the view.
- Follow with the evidence that supports it, then risks, then what to watch next.
- Keep a visible status block with as-of date, currency and units, source posture, and readiness or confidence.
- Keep the first screen useful without scrolling or interaction.

## Evidence And Citations

- Give every load-bearing number, quote, date, and management assertion a visible source label or footnote.
- Separate reported facts, provider data, estimates, assumptions, and judgment with consistent labels.
- Mark stale, conflicting, inferred, or missing evidence where it is used, not only in an appendix.
- Do not present unverified figures as sourced. Preserve provider and source provenance.
- Keep source dates and market-data timestamps visible.

## Layout And Legibility

- Use a restrained palette with one accent. Do not rely on color alone for status; add text or icons.
- Meet WCAG AA contrast for text and key chart marks.
- Use semantic headings, landmarks, table headers, captions, and `lang`. Include text alternatives for charts.
- Align numbers right with consistent units, decimals, and negative-value formatting.
- Prefer a few well-chosen tables and charts over decoration. Every chart states what it shows and the source.
- Keep line length readable and avoid dense walls of text.

## Responsive And Print

- Layout adapts from narrow mobile widths to desktop without horizontal page scroll. Wide tables scroll inside their own container.
- Include a print stylesheet so the artifact prints or exports to PDF cleanly, with page breaks that avoid splitting tables and key callouts.
- Respect `prefers-reduced-motion`. Motion is optional and never carries meaning.
- Interactive elements, such as toggles or filters, are keyboard accessible. Content stays readable if JavaScript fails.

## Honesty And Readiness

- State what the artifact is and is not fit for. Do not imply it is circulation-ready, client-ready, or investment advice unless QC has passed.
- Carry limitations from the source posture into the artifact: missing connectors, user-supplied data, and weaker categories.
- Do not expose internal workflow terms such as `source_category_plan`, `preflight`, or `next_action` in reader-facing text.

## Delivery Checks

Before handing off, confirm:

1. The file opens offline with no console errors and no external requests.
2. Numbers, dates, and labels match the underlying analysis or workbook.
3. Citations are visible for load-bearing claims.
4. Mobile width, keyboard navigation, and print output were checked.

Provide the file path and a short summary of the first-read takeaway and any open limitations.
