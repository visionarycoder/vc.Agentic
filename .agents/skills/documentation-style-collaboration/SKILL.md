---
name: "documentation-style-collaboration"
description: "Improve documentation wording with collaborative, clear, and direct language."
metadata:
  metadata-version: "1.0.0"
  title: "Documentation Style Collaboration Skill"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "optional"
---

# Documentation Style Collaboration Skill

Agent improves documentation tone without changing technical meaning.

## When to Use

| User prompt | Use |
|---|---|
| User asks for Documentation Style Collaboration work | Use this skill |
| Request falls inside the documentation suite and needs this specific surface | Use this skill |
| The routed catalog needs a single current-state owner for this concern | Use this skill |

## When Not to Use

| User prompt | Route |
|---|---|
| Request is broader than this skill and suite routing is still unclear | Use `documentation-intake-router` first |
| Request belongs to a narrower specialist than this skill | Use that narrower specialist |
| Request is outside this skill's suite or concern | Use the correct suite router or execution skill |

## Workflow

| Step | Agent Action | Output |

|---|---|---|

| 1. Identify | Agent finds imperative-heavy or unclear sections. | Rewrite targets |

| 2. Rephrase | Agent adds explicit subjects and collaborative wording. | Revised prose |

| 3. Preserve | Agent keeps technical constraints and required facts unchanged. | Accurate content |

| 4. Review | Agent checks edited sections for tone and clarity. | Style confirmation |

## Style Goals

Agent uses clear and direct wording.

Agent uses collaborative phrasing instead of command-heavy prose.

Agent keeps rationale visible when rationale reduces ambiguity.

Agent keeps sentences concise and concrete.

## Preferred Patterns

| Use | Avoid |

|---|---|

| `Agent updates...` | Bare imperative lines with no subject |

| `Developers use...` | Vague actor-free instructions |

| `This step keeps...` | Unexplained procedure blocks |

## Quality Gate

| Check | Test | Pass Criteria |

|---|---|---|

| Explicit subjects | Review edited sentences. | Every edited sentence names a subject. |

| Collaborative tone | Review edited sections for command-heavy phrasing. | Edited sections use clear, non-commanding language. |

| Technical fidelity | Compare revised text to source requirements. | Revised wording preserves the original technical meaning. |

## Additional source coverage

The selected version is the preferred starting point by the recorded date/context basis. Distinct source coverage is retained in the scoped references; do not apply superseded or conflicting defaults automatically.

- [documentation-style-collaboration-alternative-1](references/contexts/documentation-style-collaboration-alternative-1/guide.md)
