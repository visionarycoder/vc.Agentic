---
name: "bio-rhea-skill"
description: "Submit compact Rhea reaction search requests for biochemical reactions and reaction IDs. Use when a user wants concise Rhea summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Rhea Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Rhea Skill

Use `scripts/rest_request.py` for all Rhea calls with `base_url=https://www.rhea-db.org`, path `rhea`, `format=json`, `record_path=results`.
- Search by `query` (compound, EC number, text) or `query=RHEA:<id>`; keep `max_items` at 5-10.

## Input
- Read one JSON object from stdin.
- Required fields: `base_url`, `path`
- Optional fields: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`
- Common Rhea patterns:
  - `{"base_url":"https://www.rhea-db.org","path":"rhea","params":{"query":"caffeine","format":"json"},"record_path":"results","max_items":10}`
  - `{"base_url":"https://www.rhea-db.org","path":"rhea","params":{"query":"RHEA:47148","format":"json"},"record_path":"results","max_items":5}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.

Run: pipe the JSON to `python scripts/rest_request.py`.
