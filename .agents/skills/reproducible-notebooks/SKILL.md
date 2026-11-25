---
name: "reproducible-notebooks"
description: "Create, edit, or validate reproducible computational notebooks for analysis, experiments, diagnostics, or tutorials that are reviewable and rerunnable top to bottom."
metadata:
  metadata-version: "1.0.0"
  title: "Reproducible Notebooks"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-24"
  collection: "optional"
---

# Reproducible Notebooks

Treat a notebook as a reader-facing artifact, not a scratchpad dump. It is not complete until it runs top to bottom, or the execution gap is stated with the exact steps needed to reproduce it. Use `validate-data` when results support a recommendation or shared claim.

## Workflow

1. Lock the mode (analysis report, experiment log, diagnostic, data-quality check, calculation, tutorial, report companion), the reader, the decision, required inputs, and whether to create or minimally edit.
2. Use notebook-aware tooling instead of hand-editing raw JSON. When editing, preserve intent, avoid reordering cells unless it improves the story, and validate structure after any raw edit.
3. Structure by mode.
   - Analysis: `tl;dr`, Context & Methods (with Key Assumptions when they affect correctness), Data, Results, Takeaways.
   - Tutorial: Goal, Setup, Steps, Checks, Next Steps.
   - Write `tl;dr` and takeaways last, from executed outputs, with concrete values.
4. Separate setup, parameters, loading, preparation, calculation, visualization, and interpretation. Keep complex queries in query cells or separate files, not large embedded strings.
5. Confirm table choice, schema, partition filters, and sample rows before querying. Record query links, request ids, source paths, and extract versions for every result that supports the analysis. Keep queries filtered and bounded.
6. Keep cells short and single-purpose, each with a brief action-oriented header. Put multiple tables or charts in separate cells.
7. Check that numbers, charts, and takeaways match executed outputs. Add a reasonableness check, sample inspection, or reconciliation for surprising results before promoting them.
8. Execute top to bottom when possible. If not, state the reason and the exact command, dependency, credential, data access, or kernel needed.

## Standards

- Keep parameters, date ranges, filters, cohorts, assumptions, and source references visible near the top.
- Make computation deterministic; avoid hidden state, hand-edited intermediate values, out-of-order dependencies, and unexplained cached outputs.
- Document nonstandard packages, kernels, credentials, or local files in a setup cell.
- Keep outputs bounded: previews, samples, explicit limits, focused charts.
- Do not promote unexecuted or unverified calculations into the `tl;dr`; label caveats and validation gaps.
- Report execution gaps, partial runs, or unrun notebooks; do not add a routine validation section for a clean run.

## Checklist

- Section order matches the mode.
- Notebook runs without errors, or the failure is called out.
- Outputs are present, bounded, and not dominated by debug dumps.
- Summary, results, and takeaways match executed cells.
- Source references and links are preserved.
- Tables and charts are labeled and interpretable.
- The final response includes the notebook path and validation status.
