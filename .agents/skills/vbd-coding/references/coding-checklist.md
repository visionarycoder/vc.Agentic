---
title: VBD Coding Checklist
doc_type: reference
status: active
last_updated: 2026-10-09
---

# Coding checklist

Run this list before the edit and again before the handoff.

## Before the edit

1. Write the trigger and the observable result in one sentence each.
2. Mark each requested design choice as need or solution.
3. Name the axis: time, customer, both, or neither.
4. Write the change event. Reject the block when the event is missing, rare, or speculative.
5. Search for an existing owner by volatility, not by feature name.
6. Record the current caller contract.

## During the edit

1. Change the owner of that volatility.
2. Keep the caller contract stable unless the user accepts a contract change.
3. Put sequence and compensation in the Manager path.
4. Put reusable activity rules in the Engine path.
5. Put vendor, storage, and protocol code in the Access path.
6. Put cross-cutting infrastructure in the Utility path.
7. Convert resource types at the Access boundary.
8. Stop on a ripple. List each extra file and the volatility it exposes.

## Before handoff

1. Diff contains no new feature-named architecture block.
2. Diff contains no new entity-named architecture block.
3. Client code contains no new business sequence.
4. Access code contains no new workflow choice.
5. Utility code contains no new business term.
6. Tests cover contract, isolation, and interaction.
7. Change summary names owner, volatility, axis, and evidence label.

## Review rejects

Reject the change when any line is true:

- The new type name matches the feature, use case, or database table.
- A caller outside the owner changes because an internal type moved.
- The same business rule now exists in two clients.
- The edit adds a block with no independent change event.
- The summary calls an unknown Chapter 3 rule canonical.
