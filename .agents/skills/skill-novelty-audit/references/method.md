# Novelty method reference

## Item types

- **General proposition**: a concept the skill states. Question asks the model to explain or decide using the concept. Expected answer is the proposition.
- **Exact contract**: a specific the agent must reproduce (parameter, threshold, name, order, file location, exception). Expected answer is the exact value or step.

Skip headings, transitions, and pure navigation lines.

## Writing questions

- Phrase as a realistic task or decision, not a quiz of the skill's wording.
- Do not include the answer or distinctive terms from it.
- Include enough scenario that a correct answer is unambiguous.
- Keep `expected` short and checkable.

## Grading rubric (judge from a different model family)

- `correct`: matches `expected` including exact details.
- `concept`: gets the general idea but misses or invents exact details.
- `wrong`: misses the idea or contradicts `expected`.

Judge each arm independently and blind to which arm produced it. Use a panel when cost allows.

## Scoring

`score` computes quadrants twice.

| Mode | Counts as known when | Meaning |
| --- | --- | --- |
| lenient | `concept` or `correct` | Does the model have the general idea? |
| strict | `correct` only | Does it have the exact details? |

| Without | With | Quadrant | Action |
| --- | --- | --- | --- |
| known | known | already-known | Trim concept explanation. |
| known | not known | harmful | Remove or rewrite first. |
| not known | known | novel | Keep. |
| not known | not known | missed | Rewrite so it lands, or drop. |

Expect a large lenient/strict gap: concepts are mostly known, specifics mostly are not. A skill with a high strict novelty is earning its context.

## Caveats

- Novelty is model-specific. Record the model, tool access, and date.
- Do not use it on steering or process skills.
- The static `scan` heuristic flags generic-looking prose using surface signals (inline code, numbers, paths, constants versus definitional phrasing). It over-flags procedural text. Use it only to order review.
- A low novelty score is not proof a line is safe to delete. Confirm with task evals.
- Reference: Petrov, "Skill Novelty" (AI Engineer talk, 2026-11-11), summarized at mdflow.cz; decomposition adapted from FActScore (Min et al., EMNLP 2023).
