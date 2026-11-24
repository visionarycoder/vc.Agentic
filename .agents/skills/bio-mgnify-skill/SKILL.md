---
name: "bio-mgnify-skill"
description: "Submit compact MGnify API requests for microbiome studies, samples, and biome metadata. Use when a user wants concise MGnify summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Mgnify Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Mgnify Skill

## Operating rules
- Use `scripts/rest_request.py` with `base_url=https://www.ebi.ac.uk/metagenomics/api/v1`.
- Paths: `studies`, `samples`, `biomes`; use `record_path=data`.
- Return concise markdown summaries by default; raw output only on explicit request.

## Input
- One JSON object on stdin; required: `base_url`, `path`; optional: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`.
- Patterns:
  - `{"base_url":"https://www.ebi.ac.uk/metagenomics/api/v1","path":"studies","params":{"page_size":10},"record_path":"data","max_items":10}`
  - `{"base_url":"https://www.ebi.ac.uk/metagenomics/api/v1","path":"biomes","params":{"page_size":10},"record_path":"data","max_items":10}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.
