---
name: "bio-pharmgkb-skill"
description: "Submit compact PharmGKB API requests for genes, variants, clinical annotations, dosing guidelines, and search. Use when a user wants concise PharmGKB summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Pharmgkb Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Pharmgkb Skill

## Operating rules
- Use `scripts/rest_request.py` with `base_url=https://api.pharmgkb.org/v1/data`.
- Preferred paths: `gene/<id>`, `variant/<id>`, `clinicalAnnotation`, `dosingGuideline`, and search endpoints.
- Return concise markdown summaries by default; for the full payload set `save_raw=true` and report the saved file path.

## Input
- One JSON object on stdin; required: `base_url`, `path`; optional: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`.
- Patterns:
  - `{"base_url":"https://api.pharmgkb.org/v1/data","path":"gene/PA36679"}`
  - `{"base_url":"https://api.pharmgkb.org/v1/data","path":"clinicalAnnotation","params":{"relatedChemicals.accessionId":"PA449726","limit":10},"max_items":10}`
  - `{"base_url":"https://api.pharmgkb.org/v1/data","path":"variant/PA166158545"}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.
