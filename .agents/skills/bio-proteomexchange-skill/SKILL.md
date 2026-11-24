---
name: "bio-proteomexchange-skill"
description: "Submit compact ProteomeXchange PROXI requests for datasets, libraries, peptidoforms, proteins, PSMs, spectra, and USI examples. Use when a user wants concise PROXI summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Proteomexchange Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Proteomexchange Skill

Use `scripts/rest_request.py` for all PROXI calls with `base_url=https://proteomecentral.proteomexchange.org/api/proxi/v0.1`.
- Paths: `datasets`, `datasets/<identifier>`, `libraries`, `peptidoforms`, `proteins`, `psms`, `spectra`, `usi_examples`.
- Narrow requests by identifier, spectrum, or dataset.
- For the full payload, set `save_raw=true` and report the saved file path.

## Input
- Read one JSON object from stdin.
- Required fields: `base_url`, `path`
- Optional fields: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`
- Common PROXI patterns:
  - `{"base_url":"https://proteomecentral.proteomexchange.org/api/proxi/v0.1","path":"datasets","max_items":10}`
  - `{"base_url":"https://proteomecentral.proteomexchange.org/api/proxi/v0.1","path":"datasets/PXD000001"}`
  - `{"base_url":"https://proteomecentral.proteomexchange.org/api/proxi/v0.1","path":"usi_examples","max_items":10}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.

Run: pipe the JSON to `python scripts/rest_request.py`.
