---
name: "bio-cellxgene-skill"
description: "Submit compact CELLxGENE Discover API requests for public collection and dataset metadata. Use when a user wants concise single-cell collection summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Cellxgene Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Cellxgene Skill

## Operating rules
- Use `scripts/rest_request.py` for all CELLxGENE Discover calls.
- Use `base_url=https://api.cellxgene.cziscience.com/curation/v1`.
- Start with `collections/<collection_id>`; use the large `collections` list only for broad discovery, with `timeout_sec=60` and `max_items=5`.

## Execution behavior
- Return concise markdown summaries from the script JSON by default.
- Return raw JSON only if the user explicitly asks for machine-readable output.
- For full payloads, set `save_raw=true` with `raw_output_path` and report the saved file path.

## Input
- Read one JSON object from stdin.
- Required fields: `base_url`, `path`
- Optional fields: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`
- Common CELLxGENE patterns:
  - `{"base_url":"https://api.cellxgene.cziscience.com/curation/v1","path":"collections/db468083-041c-41ca-8f6f-bf991a070adf","max_items":5}`
  - `{"base_url":"https://api.cellxgene.cziscience.com/curation/v1","path":"collections","timeout_sec":60,"max_items":5}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.

## Execution
Pipe the JSON object to `python scripts/rest_request.py`.

## References
- No additional runtime references are required; keep the import package limited to this file and `scripts/rest_request.py`.
