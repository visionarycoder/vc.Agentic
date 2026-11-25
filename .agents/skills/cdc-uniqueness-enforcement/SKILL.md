---
name: "cdc-uniqueness-enforcement"
description: "Enforce idempotent change-data-capture imports with a normalized composite key of log position and sequence value, in-memory duplicate detection, and database-level uniqueness."
metadata:
  metadata-version: "1.0.0"
  title: "CDC Uniqueness Enforcement"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-24"
  collection: "optional"
---

# CDC Uniqueness Enforcement

Enforce CDC idempotency with the composite key `(start position, sequence value)`. Normalize key values, detect duplicates in memory, and keep a database-level unique constraint. Batch size, transactions, and progress belong to `cdc-batch-import-patterns`.

## Required Inputs

| Input | Notes |
|---|---|
| Start position source | CSV column or entity bytes |
| Sequence value source | CSV column or entity bytes |
| Duplicate policy | Skip, reject, or overwrite, per call path |
| In-memory store scope | Concurrent key store |
| Database model | Unique key at the table layer |

## Rules

| Concern | Rule |
|---|---|
| Key helper | Use one shared composite-key helper for every path; no ad hoc concatenation |
| Normalization | Strip the hex prefix, uppercase, and join as `StartPosition\|SequenceValue` in stable order; CSV hex and entity bytes must yield an identical key string |
| Byte arrays | Never compare by reference; convert to normalized hex first |
| Key shape | Exactly two parts, in stable order; the start position alone is not unique |
| Validity | Validate completeness before duplicate checks; count invalid keys separately and reject them with correlation context |
| Existing rows | Load existing keys once per import scope into a set of normalized strings |
| In-batch duplicates | Use a concurrent map; the first add succeeds and repeats fail |
| Dispositions | Skip increments the skipped counter and is an idempotent outcome, not data loss; reject emits a failure record; overwrite only on an explicit replace path |
| Database | Unique index or constraint on both key parts, so parallel imports stay safe |
| Logging | Log table, composite key, source file, and disposition; information level for skips, error level for malformed keys |

## Verification

| Check | Pass |
|---|---|
| Same key from CSV hex and entity bytes | Storage key strings match exactly |
| Two rows with the same key in one batch | First is admitted; second increments skip or reject |
| Replay an already imported file | New inserts equal `0`; duplicate count equals replayed keys |
| Inspect schema or migration | Unique key covers both parts together |
| Null, empty, or invalid key values | Rows never reach insert; failure output names the key defect |

## Pitfalls

| Pitfall | Fix |
|---|---|
| Only the start position is the key | Include the sequence value |
| Existing rows and batch keys normalized differently | Route both through the shared helper |
| Uniqueness enforced only in memory | Add the database constraint |
| Overwrite on duplicate without policy | Restrict overwrite to explicit replace paths |
