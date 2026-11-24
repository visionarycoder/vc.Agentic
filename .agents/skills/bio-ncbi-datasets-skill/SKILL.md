---
name: "bio-ncbi-datasets-skill"
description: "Submit compact NCBI Datasets v2 requests for assembly, genome, taxonomy, and related metadata endpoints. Use when a user wants concise NCBI Datasets summaries; save raw JSON or text only on request."
metadata:
  metadata-version: "1.0.0"
  title: "Bio Ncbi Datasets Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Ncbi Datasets Skill

## Operating rules
- Use `scripts/ncbi_datasets.py`; `path` is relative to `https://api.ncbi.nlm.nih.gov/datasets/v2`.
- Return concise markdown summaries by default; for a full raw response set `save_raw=true` and report the saved file path.

## Input
- One JSON object on stdin; required: `path`; optional: `params`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`.
- Patterns:
  - `{"path":"genome/taxon/9606/dataset_report","params":{"page_size":10},"record_path":"reports","max_items":10}`
  - `{"path":"genome/accession/GCF_000001405.40/dataset_report"}`
  - `{"path":"taxonomy/taxon/9606"}`

## Output
- Success returns `ok`, `source`, path metadata, and either compact `records`, a compact `summary`, or `text_head`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.
