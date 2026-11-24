---
name: "bio-ipd-skill"
description: "Submit compact IPD REST requests for HLA allele and cell-level metadata using the public IPD query API. Use when a user wants concise IPD summaries; save raw JSON or text only on request."
metadata:
  metadata-version: "1.0.0"
  title: "Bio Ipd Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Ipd Skill

## Operating rules
- Use `scripts/rest_request.py` with `base_url=https://www.ebi.ac.uk/cgi-bin/ipd/api`.
- The most stable public routes are `allele` and `cell` (also `allele/download`).
- Return concise markdown summaries by default; raw output only on explicit request.

## Input
- One JSON object on stdin; required: `base_url`, `path`; optional: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`.
- Patterns:
  - `{"base_url":"https://www.ebi.ac.uk/cgi-bin/ipd/api","path":"allele","params":{"project":"HLA","limit":10},"record_path":"data","max_items":10}`
  - `{"base_url":"https://www.ebi.ac.uk/cgi-bin/ipd/api","path":"allele","params":{"project":"HLA","query":"contains(name,\"A*01\")","limit":10},"record_path":"data","max_items":10}`
  - `{"base_url":"https://www.ebi.ac.uk/cgi-bin/ipd/api","path":"cell","params":{"limit":10},"record_path":"data","max_items":10}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records`, a compact `summary`, or `text_head`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.
