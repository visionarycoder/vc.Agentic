---
name: "vbd-coding"
description: "Apply Juval Löwy Volatility-Based Decomposition (VBD) to code changes. Place each change in the component that owns that volatility."
metadata:
  metadata-version: "1.0.0"
  title: "Apply VBD to code"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "vbd"
---

# Apply VBD to code

## When to use

Use this skill for a code change, a new type, a refactor, or a code review.
Load `vbd-method` for source labels on architecture work.
Load `vbd-boundary-design` for contracts and call policy.
Load `vbd-design-validation` for change simulation.
Read [evidence labels](references/evidence.md) before you call a rule canonical.
Read [coding checklist](references/coding-checklist.md) before you edit.

## Scope and limits

The Method has two parts: system design and project design.
This skill applies system design to code.
Project design covers schedule, cost, and risk options. Leave it out unless the user asks.
Do not call this skill the complete IDesign standard.
The detailed IDesign standard stayed behind an access gate on 2026-10-09.
Do not invent Chapter 3 rule text. The public sources name "The Four Questions" and "Managers-to-Engines Ratio" and do not supply those rules.
Do not copy book text into code, comments, or reviews.
A repository rule that is stricter than this skill wins inside that repository.

## Design directive

Decompose by volatility.
Encapsulate each area of potential change in one building block.
Implement the required behavior as interaction among those blocks.
Do not design the code structure against the feature list.
Functional decomposition is valid for requirements discovery. It is invalid as the code structure.
Domain decomposition is functional decomposition under domain names. Reject it as structure.

## Volatility test

Encapsulate a change at the architecture boundary only when the change is open-ended and a missed boundary causes ripple edits.
Handle a closed, local difference with ordinary conditional logic. That difference is variability, not volatility.
Do not encapsulate the nature of the business.
Reject a speculative change that lacks a credible change event.
Two signs mark nature-of-business change: the change is rare, and any encapsulation attempt stays poor.

## Axes

Search change on two axes:

1. Same customer over time.
2. All customers at the same time.

Keep the axes mostly independent.
A proposed block that maps to neither axis is a functional block. Do not add it.

## Coding procedure

1. State the required behavior as one trigger and one observable result.
2. Strip solutions that sit inside the request. Name the underlying need.
3. List other known ways to meet that need.
4. Record one credible change event for the proposed edit. Name the axis.
5. Search the code for the block that already hides that change.
6. Edit that block when it exists. Keep every caller contract stable.
7. Stop when the edit ripples across unrelated blocks. Propose one volatility boundary. Do not patch every caller.
8. Add the smallest new block when no owner exists. Give it one reason to change.
9. Name the block for the volatility. Do not name it for the feature, entity, folder, or table.
10. Place the code with the placement table below.
11. Map external types at the boundary that talks to them. Callers depend on the immediate contract.
12. Add the tests in the test section.
13. Return the change summary. Label each architecture claim.

## Placement

Role names come from public interview material. They are secondary interpretation, not a verified call ban.

| Code concern | Place it in | Leave out |
| --- | --- | --- |
| Presentation, trigger shape, client technology | Client | Core business policy |
| Order, workflow, compensation, coordination | Manager | Activity rules that other workflows reuse |
| Business rule, validation, calculation, activity policy | Engine | Storage, protocol, and vendor mechanics |
| Provider, storage, protocol, query, transport | Resource Access | Workflow choice and business policy |
| Stored state or external capability | Resource | Logical policy |
| Logging, security helper, clock, metrics, serialization, message bus | Utility | Business terms and business rules |

A Manager is a set of related use cases in secondary slide material. An Engine is shared when several Managers need the same activity rule.
Do not add a pass-through type that only forwards a call.
Do not force an Engine into a path that has no policy.
Technology, class shape, and hosting sit inside the block. They are detailed design. They are not the decomposition.

## Tests

1. Contract test: callers still compile and pass against the same contract.
2. Isolation test: the volatility change stays inside the owner.
3. Interaction test: the activity still produces the observable result.
4. Regression test: one unchanged caller stays unchanged.

Unit tests alone do not prove the decomposition. Interaction defects live between blocks.

## Change summary

Return these fields:

- Behavior: trigger and result
- Need versus discarded solution
- Volatility and axis
- Owner path
- Contract kept or contract changed
- Unchanged callers
- Evidence label for each architecture claim

Evidence labels: `Primary guidance`, `Secondary interpretation`, `Team policy`, `Repository rule`, `Heuristic/Unknown`.

## Anti-patterns

- Feature class, use-case service, or entity service as the structure
- Client, controller, or page that sequences business steps and compensates failure
- Access type that selects workflow
- Utility that contains business terms
- Block added only because a past system had that block
- God block that absorbs unrelated change
- One block per requirement
- Copied data transfer object with no independent change evidence
- Service count used as a pass condition
- Size-based microservice split

## References

- [Evidence labels](references/evidence.md)
- [Coding checklist](references/coding-checklist.md)
