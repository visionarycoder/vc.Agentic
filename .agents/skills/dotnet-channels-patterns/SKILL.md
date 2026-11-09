---
name: "dotnet-channels-patterns"
description: "Use System.Threading.Channels for high-performance, lock-free coordination between producers and consumers. Replace legacy threading patterns with channel-based work distribution."
metadata:
  metadata-version: "1.0.0"
  title: ".NET Channels Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# .NET Channels Patterns

Agent uses `System.Threading.Channels` for lock-free, high-throughput producer-consumer coordination. Agent replaces legacy `BlockingCollection<T>`, `Queue<T>` with manual locks, and `Task.Run` chains with channel-based pipelines.

## When to Use

| Condition | Use |
|---|---|
| Agent implements producer-consumer patterns between tasks or threads | Use this skill |
| Agent needs high-performance work queuing without locks | Use this skill |
| Agent converts BlockingCollection or manual queue synchronization | Use this skill |
| Agent chains async processing stages with bounded buffers | Use this skill |

## When Not to Use

| Condition | Use |
|---|---|
| Single-threaded async orchestration without concurrency | Use async/await patterns directly |
| One-time task spawning or fire-and-forget work | Use Task.Run or hosted services |
| Real-time synchronization primitive needed (Semaphore, Mutex) | Route to threading primitives |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Item type | Yes | Type flowing through channel |
| Producer model | Yes | Single, multiple, or source-generated |
| Consumer model | Yes | Single, multiple, or reader loop |
| Backpressure strategy | Yes | Bounded, unbounded, or dynamic |
| Completion signal | Yes | Graceful close, cancellation, or error propagation |

## Workflow

Agent follows these steps:

1. Agent selects channel capacity: `CreateUnbounded<T>()` for unbounded, `CreateBounded<T>()` for backpressure.
2. Agent implements producer loop: writes items, signals completion via `Complete()`.
3. Agent implements consumer loop: reads via `ReadAllAsync()` or manual `TryRead()`.
4. Agent ensures cancellation propagates through both sides using `CancellationToken`.
5. Agent validates no deadlocks or resource leaks on exception.

Test: Run `dotnet test [test-project].csproj --filter Channel` when tests exist.
Pass: Zero hanging reads, zero missed completion signals, zero deadlocks.

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Producer never calls Complete() | Call explicitly when done |
| Reader never completes when channel closes | Use ReadAllAsync() which auto-completes |
| Consumer loop ignores cancellation | Pass CancellationToken to ReadAllAsync() |
| Unbounded channel used for all patterns | Select bounded channel for backpressure |
| Exception in reader silently stops consumption | Log and rethrow or propagate via channel.Writer.TryComplete(ex) |

## Channel Selection Matrix

| Use Case | Channel Type | Capacity | Buffering |
|---|---|---|---|
| Work queue with backpressure | Bounded | CPU count × 2 to 10× | Drop oldest or wait |
| Event log or metrics stream | Unbounded | N/A | Memory-bounded by upstream |
| Request batch processor | Bounded | 100–1000 | Drop or fast-fail |
| Real-time pipeline stage | Bounded | 1–10 | Single-item hand-off |

## Completion and Error Handling

| Scenario | Pattern |
|---|---|
| Producer finishes normally | Call `channel.Writer.Complete()` |
| Producer encounters error | Agent completes the writer with `channel.Writer.Complete(exception)` |
| Consumer detects error | Catch in read loop, rethrow or log |
| Cancellation arrives mid-read | `ReadAllAsync()` cancels cleanly via token |

## Verification Matrix

| Test | Run | Pass |
|---|---|---|
| Compile verification | `dotnet build [project].csproj` | Zero compile errors |
| Completion flow | Write 10 items, close, verify reader sees all and completes | All items received, no hang |
| Cancellation | Pass cancellation token to ReadAllAsync, await cancellation | Cancellation honored promptly |
| Backpressure | Bound channel, high-rate producer, verify write throttling | Writer waits when buffer full |

## Verification Checklist

Agent verifies:
- [ ] Channel type and capacity match use case
- [ ] Producer signals completion or error
- [ ] Consumer loop handles all items before channel closes
- [ ] Cancellation propagates cleanly
- [ ] No deadlocks on exception
- [ ] Disposal cleans up resources

## Legacy Pattern Migration

### Before: BlockingCollection with Manual Locking

```csharp
public class LegacyWorkProcessor
{
    private readonly BlockingCollection<WorkItem> _queue = new(100);

    public void Enqueue(WorkItem item)
    {
        if (!_queue.TryAdd(item, TimeSpan.FromSeconds(1)))
            throw new InvalidOperationException("Queue full");
    }

    public async Task ProcessAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            if (_queue.TryTake(out var item, 100, ct))
            {
                await ProcessItemAsync(item, ct);
            }
        }
    }
}
```

### After: System.Threading.Channels

```csharp
public class ModernWorkProcessor(
    ILogger<ModernWorkProcessor> logger,
    IMetricsService metrics)
{
    private Channel<WorkItem> _channel = Channel.CreateBounded<WorkItem>(
        new BoundedChannelOptions(100)
        {
            FullMode = BoundedChannelFullMode.Wait
        });

    public async ValueTask EnqueueAsync(WorkItem item, CancellationToken ct)
    {
        if (!await _channel.Writer.WriteAsync(item, ct))
            throw new InvalidOperationException("Channel closed");
    }

    public async Task ProcessAsync(CancellationToken ct)
    {
        await foreach (var item in _channel.Reader.ReadAllAsync(ct))
        {
            // exception handling example
            {
                await ProcessItemAsync(item, ct);
                metrics.RecordSuccess(item.Type);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Failed to process {ItemType}", item.Type);
                metrics.RecordFailure(item.Type);
            }
        }
    }

    public ValueTask CompleteAsync() => _channel.Writer.WriteAsync(
        new WorkItem { IsTerminal = true });

    private async Task ProcessItemAsync(WorkItem item, CancellationToken ct)
    {
        await Task.Delay(100, ct);
    }
}
```

## C# 14+ Channel Patterns

### Primary Constructor with Channel Factory

```csharp
public class PipelineStage(
    ChannelReader<T> input,
    ChannelWriter<U> output,
    ILogger<PipelineStage> logger)
{
    public async Task RunAsync(CancellationToken ct)
    {
        await foreach (var item in input.ReadAllAsync(ct))
        {
            // exception handling example
            {
                var transformed = await TransformAsync(item, ct);
                await output.WriteAsync(transformed, ct);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Transformation failed");
                output.Writer.Complete(ex);
                return;
            }
        }

        await output.Writer.Complete();
    }

    private async ValueTask<U> TransformAsync(T item, CancellationToken ct)
    {
        return default!;
    }
}
```

### File-Scoped Bounded Channel Options

```csharp
file static class ChannelDefaults
{
    internal static BoundedChannelOptions WorkQueueOptions =>
        new(Environment.ProcessorCount * 4)
        {
            FullMode = BoundedChannelFullMode.Wait
        };

    internal static BoundedChannelOptions FastPipelineOptions =>
        new(1)
        {
            FullMode = BoundedChannelFullMode.DropNewest
        };
}
```
