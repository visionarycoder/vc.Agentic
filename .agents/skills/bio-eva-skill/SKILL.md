---
name: "bio-eva-skill"
description: "Submit compact EVA REST requests for species metadata and archived variant lookups. Use when a user wants concise European Variation Archive summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Eva Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Eva Skill

## Operating rules
- Use `scripts/rest_request.py` for all EVA calls.
- Use `base_url=https://www.ebi.ac.uk/eva/webservices/rest/v1`.
- Prefer metadata and targeted variant lookups; keep region queries narrow.

## Execution behavior
- Return concise markdown summaries from the script JSON by default.

## Input
- Read one JSON object from stdin.
- Required fields: `base_url`, `path`
- Optional fields: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`
- Common EVA patterns:
  - `{"base_url":"https://www.ebi.ac.uk/eva/webservices/rest/v1","path":"meta/species/list","record_path":"response.0.result","max_items":10}`
  - `{"base_url":"https://www.ebi.ac.uk/eva/webservices/rest/v1","path":"variants/rs699","max_items":10}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.

## Execution
```bash
echo '{"base_url":"https://www.ebi.ac.uk/eva/webservices/rest/v1","path":"meta/species/list","record_path":"response.0.result","max_items":10}' | python scripts/rest_request.py
```

## References
- No additional runtime references are required; keep the import package limited to this file and `scripts/rest_request.py`.
