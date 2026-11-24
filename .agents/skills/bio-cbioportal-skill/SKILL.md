---
name: "bio-cbioportal-skill"
description: "Submit compact cBioPortal API requests for studies, molecular profiles, mutations, clinical data, and samples. Use when a user wants concise cBioPortal summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Cbioportal Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Cbioportal Skill

## Operating rules
- Use `scripts/rest_request.py` for all cBioPortal API calls.
- Use `base_url=https://www.cbioportal.org/api` and `Accept: application/json`; use `method=POST` plus `json_body` for fetch-style endpoints.
- Collection endpoints: `pageSize=10` and `max_items=10`; single study or profile lookups need no cap.
- Treat displayed `...` in tool previews as UI truncation, not literal request content.
- Re-run requests rather than rely on older output.

## Execution behavior
- Return concise markdown summaries from the script JSON by default.
- If the user needs the full payload, set `save_raw=true` and report the saved file path.

## Input
- Read one JSON object from stdin.
- Required fields: `base_url`, `path`
- Optional fields: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`
- Common cBioPortal patterns:
  - `{"base_url":"https://www.cbioportal.org/api","path":"studies","params":{"keyword":"breast","projection":"SUMMARY","pageSize":10},"headers":{"Accept":"application/json"},"max_items":10}`
  - `{"base_url":"https://www.cbioportal.org/api","path":"molecular-profiles/brca_tcga_mutations/mutations/fetch","method":"POST","json_body":{"sampleListId":"brca_tcga_all","entrezGeneIds":[7157]},"headers":{"Accept":"application/json"},"max_items":10}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.

## Execution
Pipe the JSON object to `python scripts/rest_request.py`.

## References
- No additional runtime references are required; keep the import package limited to this file and `scripts/rest_request.py`.
