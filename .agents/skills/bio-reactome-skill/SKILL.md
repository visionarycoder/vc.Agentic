---
name: "bio-reactome-skill"
description: "Submit compact Reactome ContentService requests for pathway, event, participant, search, and diagram-related data. Use when a user wants concise Reactome summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Reactome Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Reactome Skill

Use `scripts/rest_request.py` for all Reactome calls with `base_url=https://reactome.org/ContentService` and header `Accept: application/json`.
- Paths: `data/query/<eventId>`, `data/pathways/low/entity/<identifier>` (with `species`), `data/participants/<eventId>`, search endpoints.
- For the full payload, set `save_raw=true` and report the saved file path.

## Input
- Read one JSON object from stdin.
- Required fields: `base_url`, `path`
- Optional fields: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`
- Common Reactome patterns:
  - `{"base_url":"https://reactome.org/ContentService","path":"data/query/R-HSA-199420","headers":{"Accept":"application/json"}}`
  - `{"base_url":"https://reactome.org/ContentService","path":"data/pathways/low/entity/P38398","params":{"species":"Homo sapiens"},"headers":{"Accept":"application/json"},"max_items":10}`
  - `{"base_url":"https://reactome.org/ContentService","path":"data/participants/R-HSA-199420","headers":{"Accept":"application/json"},"max_items":10}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.

Run: pipe the JSON to `python scripts/rest_request.py`.
