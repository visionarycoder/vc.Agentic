---
title: ADR Creation Template
doc_type: readme
status: active
summary: Pre-formatted ADR template for architectural decisions with all required metadata
references:
  - docs/dr/adr-template.md
---
# ADR Creation Template

Use this template when documenting a new technical decision. All mandatory fields must be filled before committing.

---
title: [Describe the decision briefly]
doc_type: adr
status: draft
last_updated: 2026-10-XX
type: technical
summary: Decision summary — one sentence capturing what was decided and why
depends_on: []
tags: [technical, infrastructure]
---

# Architecture Decision

## Context

[What problem were you solving? What alternatives existed? Any hard constraints? Reference requirements doc if applicable.]

## Alternatives Considered

| Option | Why Considered | Major Trade-off |
|--:----:
| A | [Brief rationale] | [Primary cost]
| B | [Brief rationale] | [Primary cost]
| **Decision** | [One-liner selecting option] | [What you accepted as limitation]

## Decision Summary

**Selected:** Option X because Y. We prioritized Z over W due to [constraint or trade-off].

## Technical Specs

| Property | Value | Notes |
|----------|-------|-------|
| Pattern/Approach | Describe the selected pattern | See implementation notes |
| Format/Protocol | JSON, REST, etc. | Version if applicable |
| Validation rule | [Rule description] | Failure behavior? |

## Validation Criteria

- **Criterion 1:** [How to verify this criterion]
- **Criterion 2:** [How to verify this criterion]

## References

- Source document for decision` (`url/path` example)`
- Requirements doc reference` (`link` example)`
