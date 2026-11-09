---
name: "architecture-documentation"
description: "name: architecture-documentation"
metadata:
  metadata-version: "1.0.0"
  title: "Architecture Documentation"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

name: architecture-documentation
description: >
  Automated architectural decision documentation and formatting. Write technical decisions properly with Mermaid diagrams, ADR format, and proper structure.
version: 2.0.0
author: visionarycoder
license: MIT
metadata:
  heritage:
    tags: [documentation, architecture, adr, documentation]
    vc:
      role: architect
      tier: architect
      monitors: [docs/adr, surface.md]
---

# Architecture Documentation

You are responsible for documenting architectural decisions properly. Every design decision that affects the system must be documented in an ADR (Architecture Decision Record) using standardized format.

## Procedural Requirements

### Every Architecture Decision Follows This Procedure

```yaml
1.  Determine document type: ADR, surface.md entry, or decision log item
2.  Create document template with correct metadata
3.  Write procedure documentation first, then add supporting tables/diagrams
4.  Embed Mermaid where appropriate; prefer text tables for decisions
5.  Validate against decision matrix before committing
6.  Link to decision registry and status.md entry
```

### When to Document a Decision

**Document if:**
- Decision affects component boundaries or interfaces
- Decision involves trade-offs between architectures
- Decision affects how future agents document related topics
- Decision requires non-obvious justification beyond code comments

**Do not document if:**
- Decision is obvious from existing code patterns
- Decision follows established convention or style guide
- Decision can be inferred from project requirements (see Requirements.md)
- Local developer choice with no architectural ripple effect

### When Using Mermaid

1.  Use Mermaid for visual diagrams when they add clarity
2.  Include only relevant diagrams to decision; avoid decoration
3.  Ensure diagram has clear labels and minimal technical jargon
4.  Refer readers to the decision matrix if multiple patterns apply

### When Using Decision Tables

```markdown
| Field | Required | Description |
|-------|----------|-------------|
| X | Yes       | Short description |
```

Never use ASCII art unless no table alternative exists. Text-based tables are more portable with less rendering risk.

---

## ADR Structure

All ADRs follow the same structure:

```markdown
---
title: [Descriptive Title]
doc_type: adr
status: draft | active | deprecated
last_updated: YYYY-MM-DD
type: technical | infrastructure | architectural | business
summary: One sentence summary of decision and outcome
depends_on: []        # Linked decisions if any
tags: [tag1, tag2]    # Category tags for discovery
---

# Architecture Decision

## Context (One Paragraph)
[What was the problem? What options existed? Any constraints?]

## Alternatives Considered

| Option | Rationale | Trade-offs |
|--------|-----------|------------|
| Option A | [Why considered] | [What you gave up] |

## Decision Summary (One Sentence)
**Selected:** Choose X because of Y. We prioritized Z over W.

## Technical Specs

| Property | Value | Notes |
|----------|-------|-------|
| API | JSON | Standard REST |
| Storage | SQLite | Single file per I/O |
| Protocol | REST | HTTP v2 or higher |

## Validation Criteria

- Criterion 1: [Verification method]
- Criterion 2: [Verification method]

Reference documentation: [URL or internal doc name]
```

### Mandatory Fields (Red Lines)

| Field | Status | Enforcement |
|-------|--------|-------------|
| title, doc_type, status | required | No commit without all filled |
| summary | required | Must capture full decision intent |
| depends_on | optional | Required if referencing other ADRs |
| tags | required | Minimum one relevant category tag |

### Formatting Rules

- **Tone:** Technical, authoritative. Avoid "we think" or "possibly."
- **Consistency:** Use same terminology throughout (e.g., always "ADR-XXX", consistently named fields)
- **Brevity:** 1–4 paragraphs maximum; tables preferred over prose for decisions
- **Evidence only not claims:** Cite requirements, constraints, and design documents as evidence, not opinions

---

## Decision Log Format

Maintain an evergreen registry file (e.g., `DR/decisions.md`) tracking all ADRs:

```markdown
| ID  | Type           | Status     | Title                                      | File Path          | Date    |
|-----|----------------|------------|--------------------------------------------|--------------------|---------|
| D-001 | Technical       | Draft      | Headless Architecture                       | design/adr/ADR-0001 | 2026-10-XX |
```

All decisions are indexed here for discovery. Status updates when decision changes from draft → accepted.

---

## Common Patterns

### When Deferring Decisions

```markdown
## Decision Pending
**Pending:** [decision description]
**Status:** [pending decision from leader]
**Reference:** [document or spec that contains the decision]
```

### When Referencing Existing Specs

```markdown
## Specification Reference
Refer to: [name of specification], section [section]. The ADR in question implements [option] from this spec, consistent with requirements documentation.
```
