---
name: "message-patterns"
description: "Apply pub/sub, request/reply, idempotent handling, outbox, and saga patterns with explicit contracts and replay-safe business handling, independent of any broker or framework."
metadata:
  metadata-version: "1.0.0"
  title: "Message Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-24"
  collection: "optional"
---

# Message Patterns

Design transport-agnostic messaging with explicit contracts, durable dispatch, and replay-safe handlers.

## Pattern Selection

| Pattern | Use | Avoid |
|---|---|---|
| Pub/sub event | One producer notifies many subscribers | Synchronous fan-out in the request path |
| Request/reply | Caller needs one correlated response | Events where exactly one reply is required |
| Idempotent handler | Delivery is at-least-once | Side effects keyed by transient transport state |
| Outbox | A state change and its publish must succeed together | Publish after commit with no durable dispatch record |
| Saga | Multi-step workflow needs state and compensation | Distributed transaction across services |

Skip this skill for in-process calls, broker-specific topology, or cache-level pub/sub.

## Required Inputs

| Input | Notes |
|---|---|
| Message contract set | Commands, events, replies, and identifiers |
| Consistency boundary | Transaction that covers state and outbox record |
| Idempotency key source | Message id, business key, or request token |
| Workflow state | Saga state fields and terminal conditions |
| Timeout and retry path | Expiry, retry budget, compensation path |

## Rules

| Rule | Verify | Fix |
|---|---|---|
| MSG-001 | Contracts carry a message id and a correlation id | Add stable identifiers |
| MSG-002 | Duplicate delivery does not repeat external side effects | Add an idempotency store keyed by message id |
| MSG-003 | Publish-after-write uses an outbox written in the same transaction | Add an outbox table and a dispatcher |
| MSG-004 | Saga state is explicit and persisted, with timestamps and a terminal state | Add a persistent state record |
| MSG-005 | Request/reply has a reply contract and a timeout path | Add reply correlation and timeout handling |
| MSG-006 | Handlers stay transport-agnostic | Move broker logic into publisher or consumer adapters |
| MSG-007 | No mediator layer is introduced between transport and handlers | Use explicit interfaces and handlers |

## Pitfalls

| Pitfall | Fix |
|---|---|
| Adapter contains business orchestration | Move it into an application service or saga |
| Idempotency key is a random per-attempt value | Key off a stable message or business id |
| Saga state lives only in memory | Persist it |
| Saga step lacks a timeout or compensation | Give every step a next, timeout, and terminal path |

## Verification

| Check | Pass |
|---|---|
| Process the same message twice | Side effects occur once |
| Simulate a publish outage after the write | Outbox rows persist and dispatch later |
| Exercise request/reply, subscriber, and compensation paths | Replies correlate, subscribers react once, saga reaches the expected terminal state |
| Run targeted build and tests | Build succeeds and tests pass |

## Outputs

- Stable command, event, and reply contracts
- Idempotent handler boundary
- Outbox persistence and dispatcher flow
- Saga state and transition model
- Verification evidence for duplicate, timeout, and compensation paths
