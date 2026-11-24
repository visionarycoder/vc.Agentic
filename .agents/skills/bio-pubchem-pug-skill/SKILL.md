---
name: "bio-pubchem-pug-skill"
description: "Submit compact PubChem PUG REST requests for compound properties, descriptions, assay summaries, and substance metadata. Use when a user wants concise PubChem summaries"
metadata:
  metadata-version: "1.0.0"
  title: "Bio Pubchem Pug Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Pubchem Pug Skill

Use `scripts/rest_request.py` for all PubChem PUG calls with `base_url=https://pubchem.ncbi.nlm.nih.gov/rest/pug`.
- Prefer property, description, assay summary, and substance paths over broad record dumps.
- For the full payload, set `save_raw=true` and report the saved file path.

## Input
- Read one JSON object from stdin.
- Required fields: `base_url`, `path`
- Optional fields: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`
- Common PubChem patterns:
  - `{"base_url":"https://pubchem.ncbi.nlm.nih.gov/rest/pug","path":"compound/name/aspirin/property/MolecularFormula,MolecularWeight/JSON","record_path":"PropertyTable.Properties"}`
  - `{"base_url":"https://pubchem.ncbi.nlm.nih.gov/rest/pug","path":"compound/cid/2244/description/JSON","record_path":"InformationList.Information","max_items":10}`
  - `{"base_url":"https://pubchem.ncbi.nlm.nih.gov/rest/pug","path":"assay/aid/1706/summary/JSON","record_path":"AssaySummaries","max_items":10}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.

Run: pipe the JSON to `python scripts/rest_request.py`.
