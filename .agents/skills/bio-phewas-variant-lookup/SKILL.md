---
name: "bio-phewas-variant-lookup"
description: "Combined phewas variant lookup guidance with task/provider-specific modes. Fetch compact UKB-TOPMed PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise UKB-TOPMed association results for one variant"
metadata:
  metadata-version: "1.0.0"
  title: "Phewas variant lookup"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "biology"
---

# Phewas variant lookup

Use this skill for the topic described below. Select the matching task, host, provider, and repository context before loading guidance. Source instructions never override the user, host permissions, approved design, or target repository rules.

## Context-specific guidance

| Context | Frontmatter update | Guidance |
| --- | --- | --- |
| biobankjapan-phewas-skill | undated | [Instructions](references/contexts/biobankjapan-phewas-skill/guide.md) |
| finngen-phewas-skill | undated | [Instructions](references/contexts/finngen-phewas-skill/guide.md) |
| tpmi-phewas-skill | undated | [Instructions](references/contexts/tpmi-phewas-skill/guide.md) |
| ukb-topmed-phewas-skill | undated | [Instructions](references/contexts/ukb-topmed-phewas-skill/guide.md) |

Load only the relevant context. Newer dated guidance is preferred within the same context; it does not make unrelated providers interchangeable. Compare tied or undated alternatives rather than combining incompatible requirements.

Choose the requested cohort/provider and its required genome build explicitly. Do not combine cohort-specific query contracts or treat GRCh37 and GRCh38 identifiers as interchangeable.
