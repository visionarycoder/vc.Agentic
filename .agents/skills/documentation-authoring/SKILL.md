---
name: "documentation-authoring"
description: "Compose well-formed documentation content for ADRs, designs, test plans, reviews, reports, diagrams, and Azure DevOps text sent to scribe."
metadata:
  metadata-version: "1.0.0"
  title: "Documentation Authoring"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Documentation Authoring

Agent composes documentation content and Azure DevOps text. Any authoring agent loads this skill to write its own repository Markdown, diagrams, and ADRs directly. `scribe` loads this skill to write Azure DevOps text. Requesting agents load it to prepare a `scribe` request.

## When to Use

| Condition | Use |
|---|---|
| Agent writes its own document, ADR, or diagram under `docs/**` | Use this skill |
| Agent prepares a request for `scribe` | Use this skill |
| `scribe` writes a work item, comment, wiki page, or message-board entry | Use this skill |
| Agent reviews a request before submitting | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Moving or renaming existing documents | `documentation-file-placement` |
| Repairing links | `documentation-link-repair` |
| Normalizing front matter only | `documentation-frontmatter` |
| Tone and wording only | `documentation-style-collaboration` |

## Request Rules

The `scribe` request format lives in `.agents/agent-team.instructions.md`. This skill adds the content rules for requests and for documents the agent writes directly.

| Rule | Test | Pass criteria |
|---|---|---|
| Requester owns meaning | Compare `intent` with `content`. | Content states the decision, finding, or plan in the requester's words. |
| One purpose per document | Count the questions the document answers. | The document answers one question. |
| Target stays inside `docs/**` | Read `target`. | Path starts with `docs/`. |
| Code is a sample | Look for code in `content`. | Code appears only inside a fenced block in a document. |
| No secrets | Search `content` for keys, tokens, and connection strings. | Zero matches. |
| Work item linked | Read `workitem_link`. | Value is present for every design, review, and test-plan document. |

## Templates by `doc_type`

Every document starts with the front matter contract in `.agents/instructions/frontmatter-standard.instructions.md`: `title`, `doc_type`, `status`, `last_updated`.

| `doc_type` | Required sections |
|---|---|
| `adr` | Context, Decision, Alternatives (at least two, with tradeoffs in cost, time, and effort), Consequences, Status |
| `design` | Purpose, Requirements covered, Components and contracts, Interactions, Open questions |
| `test-plan` | Requirement, Test cases (happy path, bad input, failure), Pass criteria, Coverage gaps |
| `review` | Subject, Standard applied, Verdict, Findings (evidence, root cause, at least two alternatives), Next step |
| `report` | Summary, Method, Results, Recommendations |
| `diagram` | Title, Purpose, Mermaid source, Rendered image link, Legend |

ADRs live in `docs/adr/`. Other placement follows `documentation-file-placement`.

## Diagrams

1. Write the Mermaid source in a `.mmd` file.
2. Render to PNG with `mermaid-cli`.
3. Store the `.mmd` and `.png` together under `docs/`, with the same base name.
4. Show one idea per diagram. Split any diagram that needs more than about 15 nodes.
5. Link the PNG from the owning document and add alt text that states what the diagram shows.

## Work Items

| Field | Content |
|---|---|
| Title | Verb and object, under 80 characters |
| Description | Problem, scope, and the design document link |
| Acceptance criteria | Measurable test and pass criteria |
| Link | Parent requirement or feature |
| State change | Only a state the work-item flow allows, with a one-line reason |

A rejection comment names the root cause and at least two alternatives with tradeoffs.

## Wording

Use explicit subjects and zero modal verbs. State each rule as a test with a pass criterion. Apply `documentation-style-collaboration` for tone.

## Validation

| Step | Test | Pass criteria |
|---|---|---|
| Front matter | `npm run frontmatter:validate` | Zero errors |
| Links | Check relative links in the new file | Zero broken links |
| Placement | Compare path with the canonical location | File sits in the correct folder |
| Template | Compare headings with the table above | Every required section present |
