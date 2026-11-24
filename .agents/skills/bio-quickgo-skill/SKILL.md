---
name: "bio-quickgo-skill"
description: "Submit compact QuickGO requests for GO terms, annotations, and ontology traversal. Use when a user wants concise QuickGO summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Quickgo Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Quickgo Skill

Use `scripts/rest_request.py` for all QuickGO calls with `base_url=https://www.ebi.ac.uk/QuickGO/services` and header `Accept: application/json`.
- Paths: `ontology/go/terms/<id>`, `annotation/search` (use `limit=10`), ontology child or ancestor endpoints.
- `annotation/search` is upstream-fragile when the Solr backend is unavailable; fall back to ontology term lookup or UniProt GO annotations.
- For the full payload, set `save_raw=true` and report the saved file path.

## Input
- Read one JSON object from stdin.
- Required fields: `base_url`, `path`
- Optional fields: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`
- Common QuickGO patterns:
  - `{"base_url":"https://www.ebi.ac.uk/QuickGO/services","path":"ontology/go/terms/GO:0008150,GO:0003674","headers":{"Accept":"application/json"},"record_path":"results","max_items":10}`
  - `{"base_url":"https://www.ebi.ac.uk/QuickGO/services","path":"annotation/search","params":{"geneProductId":"P04637","limit":10},"headers":{"Accept":"application/json"},"record_path":"results","max_items":10}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.

Run: pipe the JSON to `python scripts/rest_request.py`.
