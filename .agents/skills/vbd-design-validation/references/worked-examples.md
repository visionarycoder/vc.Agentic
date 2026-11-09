---
title: VBD Worked Examples
doc_type: reference
status: active
last_updated: 2026-09-28
---

# VBD worked examples

## Example 1: finance batch transport

### Before

One batch service reads files, validates records, posts accounting entries, writes storage state, and sends status messages.
The service changes for file protocol, validation policy, posting workflow, and status presentation.

### VBD boundaries

| Component | Role | Reason to change | Stable contract |
| --- | --- | --- | --- |
| BatchPortal | Client | Status view and operator command shape changes. | Start batch and read status. |
| BatchManager | Manager | Workflow order, retry policy, and compensation rules change. | Batch activity contract. |
| AccountingEngine | Engine | Posting and validation policy changes. | Posting policy contract. |
| BatchTransportAccess | Resource Access | File, queue, or adapter protocol changes. | Batch transport contract. |
| AccountingResourceAccess | Resource Access | Accounting provider mapping changes. | Accounting provider contract. |
| OperationsUtility | Utility | Logging, clock, and metrics details change. | Utility contract. |

### Change simulations

| Change | Changed components | Unchanged contracts |
| --- | --- | --- |
| Replace SFTP with object storage event input. | BatchTransportAccess | BatchManager activity contract and AccountingEngine policy contract. |
| Add a new accounting validation rule. | AccountingEngine | BatchTransportAccess contract and BatchPortal status contract. |
| Change status wording for operators. | BatchPortal | BatchManager activity contract and Resource Access contracts. |

### Anti-example

Do not create six services because the example has six rows.
Merge BatchPortal and BatchManager when the same process owns presentation and orchestration changes together.
Do not add a DTO per row unless callers need independent contract evolution.

## Example 2: agent metrics

### Before

One script polls sessions, attributes work, computes cost, stores data, and renders a Markdown report.
The script changes for adapter protocol, attribution policy, accounting policy, storage mechanism, and report presentation.

### VBD boundaries

| Component | Role | Reason to change | Stable contract |
| --- | --- | --- | --- |
| MetricsCollector | Manager | Polling sequence and recovery policy change. | Collection run contract. |
| OpenCodeAdapter | Resource Access | OpenCode API or CLI protocol changes. | Session and message read contract. |
| AttributionPolicy | Engine | Work-item attribution rules change. | Attribution decision contract. |
| AccountingPolicy | Engine | Runtime cost and estimate rules change. | Cost classification contract. |
| MetricsStore | Resource Access | File, lock, or schema storage mechanism changes. | Metrics persistence contract. |
| MetricsReport | Client | Markdown report presentation changes. | Report projection contract. |

### Change simulations

| Change | Changed components | Unchanged contracts |
| --- | --- | --- |
| OpenCode changes pagination syntax. | OpenCodeAdapter | AttributionPolicy and AccountingPolicy contracts. |
| The team changes child-session attribution. | AttributionPolicy | OpenCodeAdapter read contract and MetricsStore persistence contract. |
| Storage moves from JSON files to SQLite. | MetricsStore | MetricsCollector collection contract and MetricsReport projection contract. |
| The report adds a stale-data section. | MetricsReport | AccountingPolicy and MetricsStore contracts. |

### Anti-example

Do not add a separate service for every token field.
Do not force a Manager to call an Engine when no policy exists.
Keep adapter protocol, attribution policy, accounting policy, storage mechanism, and report presentation as separate change reasons.
