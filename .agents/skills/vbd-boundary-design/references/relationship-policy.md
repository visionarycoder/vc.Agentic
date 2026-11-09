---
title: VBD Relationship Policy
doc_type: reference
status: active
last_updated: 2026-09-28
---

# VBD relationship policy

## Policy status

This relationship policy is a team default.
The full canonical IDesign call matrix was not verified.
Use the policy to ask evidence questions, not to invent source claims.

## Review questions

| Finding | Question | Pass condition |
| --- | --- | --- |
| Client calls Access | Which Manager owns the activity boundary? | A Manager owns orchestration, or the design records why no orchestration exists. |
| Manager calls Manager | Which workflow owns the sequence? | The peer chain has no cycle and each Manager has separate change evidence. |
| Engine calls Engine | Which policy changes independently? | Each Engine owns different policy volatility. |
| Access calls Manager or Engine | Which dependency direction changed? | Access stays mechanism-focused, or an exception records callback ownership. |
| Any cycle | Which contract breaks the cycle? | No cycle remains, or a documented exception owns risk and failure behavior. |
| Async queue | Which component owns mediation? | Queue use changes timing only, unless a mediator owns policy. |
