---
name: "bio-ncbi-pmc-skill"
description: "Submit compact NCBI PMC Open Access requests for article/file availability metadata. Use when a user wants concise PMC Open Access summaries; save raw XML only on request."
metadata:
  metadata-version: "1.0.0"
  title: "Bio Ncbi Pmc Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "biology"
---

# Bio Ncbi Pmc Skill

## Operating rules
- Use `scripts/ncbi_pmc.py`; covers only the PMC Open Access service. BLAST, Datasets, and Entrez belong to separate skills.
- Pass `params.id` as a PMCID or DOI.
- Return concise markdown summaries by default; for a full raw response set `save_raw=true` and report the saved file path.

## Input
- One JSON object on stdin; optional: `params`, `record_path`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`.
- Patterns:
  - `{"params":{"id":"PMC3257301"},"max_items":10}`
  - `{"params":{"id":"10.1093/nar/gkr1184"},"max_items":10}`

## Output
- Success returns `ok`, `source`, and a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.
