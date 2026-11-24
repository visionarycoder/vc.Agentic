---
name: "bio-metabolights-skill"
description: "Submit compact MetaboLights requests for study discovery and study-level metabolomics metadata. Use when a user wants concise MetaboLights summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Metabolights Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Metabolights Skill

## Operating rules
- Use `scripts/rest_request.py` with `base_url=https://www.ebi.ac.uk/metabolights/ws`.
- Paths: `studies` (browse, records under `content`) and `studies/<MTBLS accession>`.
- Return concise markdown summaries by default; raw output only on explicit request.

## Input
- One JSON object on stdin; required: `base_url`, `path`; optional: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`.
- Patterns:
  - `{"base_url":"https://www.ebi.ac.uk/metabolights/ws","path":"studies","record_path":"content","max_items":10}`
  - `{"base_url":"https://www.ebi.ac.uk/metabolights/ws","path":"studies/MTBLS1"}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.
