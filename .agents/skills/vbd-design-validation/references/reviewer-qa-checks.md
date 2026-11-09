---
title: VBD Reviewer and QA Checks
doc_type: reference
status: active
last_updated: 2026-09-28
---

# VBD reviewer and QA checks

## Reviewer checks

| Check | Pass condition |
| --- | --- |
| Source classification | Each architecture conclusion has source, section, scope, and exceptions. |
| Contract containment | A change simulation keeps unrelated caller contracts stable. |
| Authority fit | Component roles match owned decisions and change drivers. |
| Local precedence | Repository rules override global guidance where applicable. |
| Evidence gap honesty | The design does not claim the full IDesign standard was verified. |

## QA checks

| Check | Pass condition |
| --- | --- |
| Behavior | Tests cover accepted behavior at the boundary. |
| Failure path | Tests cover error behavior crossing the boundary. |
| Change simulation | Tests or inspection prove expected containment. |
| Regression | Anti-examples fail or receive documented rejection. |
| Documentation input | Accepted behavior and limits are available for the writer. |
