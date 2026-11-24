---
name: "azure-service-bus-patterns"
description: "Implement Azure Service Bus queues, topics, sessions, dead-letter handling, deferral, and reliable processor flows in .NET."
metadata:
  metadata-version: "1.0.0"
  title: "Azure Service Bus Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "azure"
---

# Azure Service Bus Patterns

Implement Azure Service Bus messaging with explicit settlement, session-aware processing, dead-letter routing, and replay-safe handlers.

## When to Use

| Condition | Use |
|---|---|
| Workload uses Azure-managed brokered messaging | Use this skill |
| Flow needs queues, topics, subscriptions, or sessions | Use this skill |
| Handler needs dead-letter, deferral, or poison-message control | Use this skill |
| Service uses `ServiceBusProcessor` or `ServiceBusSessionProcessor` | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Work stays inside one process | Use `background-services-channels` |
| Flow needs event log retention and partition replay | Use Event Hubs |
| Deployment uses self-hosted broker | Use `rabbitmq-patterns` |
| Requirement is cross-cutting idempotency or outbox only | Use `message-patterns-dotnet` |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Namespace and entity names | Yes | Queue, topic, subscription, and session scope |
| Auth path | Yes | Use `DefaultAzureCredential` with RBAC |
| Message contract | Yes | Stable payload and correlation fields |
| Settlement path | Yes | Complete, abandon, dead-letter, or defer |
| Retry budget | Yes | Handler retry and lock-renew strategy |

## Workflow

| Step | Agent Action | Test | Pass |
|---|---|---|---|
| 1 | Map workload to queue, topic, or session entity. | Review entity choice. | Entity shape matches delivery semantics. |
| 2 | Agent registers `ServiceBusClient` and processor options. | Inspect DI setup. | Client and processor use explicit options. |
| 3 | Implement handler with async settlement path. | Inspect message handler. | Handler completes every success and failure branch. |
| 4 | Add dead-letter, deferral, and poison-message rules. | Review failure path. | Unrecoverable messages move to explicit path. |
| 5 | Add idempotency and correlation fields where duplicates matter. | Inspect message contract and storage. | Duplicate delivery does not create duplicate business effects. |
| 6 | Verify receive, retry, session, and dead-letter behavior. | Run targeted tests. | Main success and failure flows pass. |

## Implementation Patterns

Dead-letter final failures; defer recoverable ordering gaps (never dead-letter them or loop on abandon).

```csharp
builder.Services.AddSingleton(_ => new ServiceBusClient(
    builder.Configuration["Messaging:ServiceBus:Namespace"],
    new DefaultAzureCredential()));

builder.Services.AddSingleton(_ => new ServiceBusProcessorOptions
{
    AutoCompleteMessages = false,
    MaxConcurrentCalls = 8,
    PrefetchCount = 32,
    MaxAutoLockRenewalDuration = TimeSpan.FromMinutes(5)
});

public sealed class InvoicePostedProcessor(ServiceBusClient client, ServiceBusProcessorOptions options, InvoicePostedHandler handler) : IHostedService, IAsyncDisposable
{
    private readonly ServiceBusProcessor processor = client.CreateProcessor("invoice-posted", options);
    private async Task ProcessMessageAsync(ProcessMessageEventArgs args)
    {
        try
        {
            await handler.HandleAsync(args.Message.Body.ToObjectFromJson<InvoicePostedMessage>()!, args.CancellationToken);
            await args.CompleteMessageAsync(args.Message, args.CancellationToken);
        }
        catch (WaitingOnDependencyException ex)
        {
            await args.DeferMessageAsync(args.Message, new Dictionary<string, object> { ["DeferredReason"] = ex.Message }, args.CancellationToken);
        }
        catch (InvalidMessageException ex)
        {
            await args.DeadLetterMessageAsync(args.Message, "ValidationFailed", ex.Message, args.CancellationToken);
        }
    }
}
```

## Rules

| Rule | Agent Verifies | Fix |
|---|---|---|
| ASB-001 | `AutoCompleteMessages` stays `false` for custom reliability logic | Use explicit settlement |
| ASB-002 | Handlers are idempotent when duplicate delivery matters | Add idempotency store keyed by `MessageId` |
| ASB-003 | Session entities use stable `SessionId` from domain key | Set `SessionId` at publish time |
| ASB-004 | Poison messages move to dead-letter with reason metadata | Add `DeadLetterMessageAsync` branch |
| ASB-005 | Recoverable ordering gaps use deferral | Store sequence data and defer |
| ASB-006 | Processor concurrency matches handler throughput and lock duration | Tune `MaxConcurrentCalls`, prefetch, and lock renewal |
| ASB-007 | Logs include entity path, message id, and correlation id only | Remove payload or secret logging |

## Verification

Replay the same `MessageId`, send invalid, out-of-order, and same-session messages, then run targeted build and tests. Duplicates must not repeat effects, poison messages dead-letter, gaps defer (store `SequenceNumber` and a retrieval key), and sessions keep order.

## Outputs

- Service Bus client and processor registration
- Queue, topic, or session handler implementation
- Dead-letter and deferral policy
- Idempotent settlement flow
- Targeted verification steps for delivery and failure paths
