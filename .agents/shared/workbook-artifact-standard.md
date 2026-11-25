---
title: Workbook Artifact Standard
doc_type: reference
status: active
last_updated: 2026-11-23
summary: Quality bar for generated XLSX workbooks, including the required first-tab Cover dashboard, traceability, and formula integrity.
tags:
  - trading
  - excel
  - workbook
  - quality
---
# Workbook Artifact Standard

Shared requirements for generated `.xlsx` artifacts such as models, comps, trackers, and cleaned data workbooks. Skill-specific specs add tabs and fields; they do not remove anything required here.

## Cover Tab

- Every polished workbook has a `Cover` tab as the first visible tab.
- The cover is a PM or analyst dashboard, not a raw data table.
- Include company or subject, workbook type, as-of or valuation date, currency and units, workbook mode, and status.
- Include source posture, hard failures, warnings, and QA posture.
- Include the key outputs the reader needs first, such as valuation range, scenario outputs, or cleaned-table counts.
- Include a workbook map that lists each tab and its purpose.
- Keep it readable on one screen at normal zoom. Use short labels and no merged-cell tricks that break filtering.

## Structure

- Separate inputs, calculations, and outputs. Mark input cells distinctly and consistently.
- Keep one definition per assumption and reference it rather than repeating the value.
- Use a `Sources` or equivalent tab with stable source IDs, provider, document or field, as-of date, and retrieval status.
- Include an `Assumptions` area that labels each assumption as reported, provider, estimate, or judgment.
- Include a `quality_checks` or equivalent tab with named checks and pass, warn, or fail results.
- Hide nothing load-bearing. Hidden helper sheets are labeled on the map.

## Formulas And Values

- Prefer live formulas for calculations so the reader can audit them. Hard-coded outputs need a reason on the cover or checks tab.
- Preserve existing formulas, named ranges, and structure when updating a user's workbook. Log every changed cell with before and after values and the source.
- Avoid volatile functions, external links, and macros unless the user supplied them and they are needed.
- Do not leave error values (`#REF!`, `#DIV/0!`, `#N/A`) in delivered cells without an explicit handling note.
- Keep units, scale, periods, and signs consistent and stated in headers.

## Traceability

- Each load-bearing input traces to a source ID, period, unit, and timestamp. Keep tickers, periods, and identifiers intact.
- Keep conflicts and unresolved items in a visible log instead of silently choosing a value.
- Cleaning and normalization steps are recorded so the transformation can be replayed.

## Formatting

- Freeze header rows, set sensible column widths, and apply number formats for units, percentages, multiples, and dates.
- Use a restrained palette. Do not rely on color alone for status.
- Set print areas and orientation for the cover and key output tabs.

## Credit-Instrument Data

If a workbook carries credit-instrument data, mark `route_to_credit_markets` on the cover and checks tab unless the data is only an equity-risk signal, such as refinancing stress or solvency pressure. See `credit-markets-handoff.md`.

## Delivery Checks

1. The workbook opens without repair prompts and recalculates without errors.
2. Totals, tie-outs, and balance checks pass or are flagged on the cover.
3. The cover matches the underlying tabs.
4. Source IDs resolve and no unsourced load-bearing input remains.
