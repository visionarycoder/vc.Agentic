---
name: "adr"
description: "Record an architectural decision with context, alternatives, consequences, and the actual project approval status."
metadata:
  metadata-version: "1.0.0"
  title: "Architecture decision records"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "core"
---

# Architecture decision records

Use for significant architectural choices and their tradeoffs, not routine implementation notes.

1. Locate the consuming project's decision records, template, naming rules, and responsible decision owner. Follow an existing convention rather than assuming `docs/adr` exists.
2. If no template exists, draft a compact record containing title, date, status, context, options, proposed decision, rationale, consequences, and related evidence. Choose a location appropriate to the request.
3. Distinguish a proposal from an adopted decision. Only record acceptance supported by the responsible owner's actual decision; drafting or committing a record does not approve it.
4. Explain why alternatives were rejected and what would justify revisiting the choice. Use traceable sources without copying restricted source material.
5. Update existing navigation when it exists. Do not require separate INDEX, TOC, or README files merely to write one decision.
6. Report the record location, decision status, verification, and unresolved owner input. Commit only when authorized.
