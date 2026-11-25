---
name: "cdc-batch-import-patterns"
description: "Import change-data-capture rows in bounded batches with duplicate-aware progress tracking, per-batch transactions, and failure accumulation."
metadata:
  metadata-version: "1.0.0"
  title: "CDC Batch Import Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-24"
  collection: "optional"
---

# CDC Batch Import Patterns

Import change-data-capture rows in batches that stay idempotent, bound memory, and keep partial-failure evidence. Duplicate-key rules belong to `cdc-uniqueness-enforcement`.

## Required Inputs

| Input | Notes |
|---|---|
| Row set | Normalized rows for one table at a time |
| Batch size | Requested size, default `1000` |
| Duplicate policy | Skip or reject, aligned with the uniqueness rules |
| Persistence path | Existing repository or approved bulk path |
| Correlation scope | One correlation value per import execution or package |
| Cancellation token | Propagated through every I/O and insert boundary |

## Rules

| Concern | Rule |
|---|---|
| Context | Resolve table, entity type, duplicate policy, and correlation id before inserts start |
| Partitioning | One table at a time; every batch size is `> 0` and `<=` the configured size |
| Batch size | Start at `1000`; change it only from measured pressure (lock time, memory growth, command duration) |
| Duplicates | Pre-filter known duplicates when an existing-key lookup is available; keep the duplicate count in progress metrics |
| Change tracking | Disable automatic change detection and bound tracked entities during inserts; restore defaults afterward |
| Insert path | Use the repository's existing bulk path; otherwise add rows in ranges, save per batch, and clear tracking periodically. Do not add bulk packages as a side effect |
| Transactions | One transaction per batch (or another bounded retry unit); a failed batch does not roll back completed batches |
| Failure isolation | When a batch fails and the exact bad rows are needed, bisect the batch |
| Error accumulation | Record serialized row, error message, table, composite key, and time; continue unaffected batches; final status is partial success when loaded count `> 0` |
| Progress | Per batch log ordinal, size, inserted, skipped, failed, remaining, elapsed, and correlation id |
| Cancellation | Check before each batch, inside row loops, and before commit; no new batch starts after cancellation |

## Verification

| Check | Pass |
|---|---|
| Known row count with fixed batch size | Batch count and sizes match the partition formula |
| Replay input with known duplicates | `Inserted + Skipped + Failed` equals total input |
| Fail one middle batch | Earlier batches stay committed; later batches continue only if policy allows |
| Mixed-validity input | One failed-record entry per bad row, with correlation metadata |
| Cancel during a large import | Stops before the next batch; no open transaction remains |

## Pitfalls

| Pitfall | Fix |
|---|---|
| Whole file saved in one call | Partition into bounded batches |
| Change detection left on for large inserts | Disable it for the batch scope |
| First bad row stops the import | Accumulate the failure and continue |
| One transaction spans the whole package | Limit it to one batch |
| Progress logs omit duplicate and failure counters | Emit all counters per batch |
