# Server-Sent Events (SSE) for Streaming Responses

SSE is the standard for streaming text-based data from server to client. OpenAI's streaming completions API uses SSE.

## Why SSE Over WebSockets?

**SSE advantages:**

- Simpler: One-way server-to-client, no handshake
- HTTP-native: Works through proxies, load balancers, CDNs
- Automatic reconnection: Browsers handle reconnects with `Last-Event-ID`
- Text-based: Easy to debug with `curl`

**Use WebSockets when:**

- You need bidirectional communication
- Binary data is required
- Sub-second latency matters (SSE has ~1-2s reconnect overhead)

## ASP.NET Core SSE Implementation

### Basic Pattern

```csharp
[HttpPost("completions/stream")]
public async Task StreamCompletion(
    [FromBody] ChatCompletionRequest request,
    CancellationToken cancellationToken)
{
    Response.Headers.ContentType = "text/event-stream";
    Response.Headers.CacheControl = "no-cache";
    Response.Headers.Connection = "keep-alive";

    await foreach (var chunk in chatService.StreamCompletionAsync(request, cancellationToken))
    {
        await Response.WriteAsync($"data: {JsonSerializer.Serialize(chunk)}\n\n", cancellationToken);
        await Response.Body.FlushAsync(cancellationToken);
    }
}
```

**Critical details:**

- `Content-Type: text/event-stream` is mandatory
- Each message: `data: <payload>\n\n` (two newlines)
- **Flush after every write**—SSE requires immediate delivery
- Respect `CancellationToken` to detect client disconnects

### Service Layer with IAsyncEnumerable

```csharp
public interface IChatService
{
    IAsyncEnumerable<ChatCompletionChunk> StreamCompletionAsync(
        ChatCompletionRequest request,
        CancellationToken cancellationToken);
}

public sealed class ChatService : IChatService
{
    public async IAsyncEnumerable<ChatCompletionChunk> StreamCompletionAsync(
        ChatCompletionRequest request,
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        // Example: streaming from an LLM API
        await foreach (var token in llmClient.StreamAsync(request, cancellationToken))
        {
            yield return new ChatCompletionChunk(
                Id: Guid.NewGuid().ToString(),
                Model: request.Model,
                Choices: [new Choice(Delta: new Delta(Content: token))]
            );
        }
    }
}
```

**Why `IAsyncEnumerable<T>`?**

- Backpressure: If the client is slow, production pauses automatically
- Cancellation: Stops processing when the client disconnects
- Memory-efficient: No buffering of the entire response

### OpenAI-Style SSE Format

OpenAI sends:

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","choices":[{"delta":{"content":"Hello"}}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","choices":[{"delta":{"content":" world"}}]}

data: [DONE]
```

Implement the same:

```csharp
await foreach (var chunk in chatService.StreamCompletionAsync(request, cancellationToken))
{
    var json = JsonSerializer.Serialize(chunk);
    await Response.WriteAsync($"data: {json}\n\n", cancellationToken);
    await Response.Body.FlushAsync(cancellationToken);
}

await Response.WriteAsync("data: [DONE]\n\n", cancellationToken);
await Response.Body.FlushAsync(cancellationToken);
```

## Error Handling in SSE

SSE doesn't support HTTP error codes mid-stream. Once headers are sent (200 OK), you can't change the status. Handle errors **within the stream**:

```csharp
try
{
    await foreach (var chunk in chatService.StreamCompletionAsync(request, cancellationToken))
    {
        await Response.WriteAsync($"data: {JsonSerializer.Serialize(chunk)}\n\n", cancellationToken);
        await Response.Body.FlushAsync(cancellationToken);
    }
}
catch (Exception ex)
{
    var errorChunk = new
    {
        error = new
        {
            message = ex.Message,
            type = "internal_error",
            code = "500"
        }
    };

    await Response.WriteAsync($"data: {JsonSerializer.Serialize(errorChunk)}\n\n", cancellationToken);
    await Response.Body.FlushAsync(cancellationToken);
}
```

Clients must parse the stream and detect error objects.

## Compression and SSE

**Do NOT enable compression for SSE endpoints.** Response compression buffers data, breaking streaming.

Disable per-endpoint:

```csharp
[HttpPost("completions/stream")]
[ResponseCache(NoStore = true, Location = ResponseCacheLocation.None)]
public async Task StreamCompletion(...)
{
    // Disable compression
    Response.Headers.Remove("Content-Encoding");

    // SSE logic...
}
```

Or configure globally:

```csharp
builder.Services.AddResponseCompression(options =>
{
    options.EnableForHttps = true;
    options.ExcludedMimeTypes = ["text/event-stream"];
});
```

## Client Disconnection Detection

`CancellationToken` fires when the client disconnects. Always check it:

```csharp
await foreach (var chunk in chatService.StreamCompletionAsync(request, cancellationToken))
{
    if (cancellationToken.IsCancellationRequested)
    {
        logger.LogInformation("Client disconnected, stopping stream");
        break;
    }

    await Response.WriteAsync($"data: {JsonSerializer.Serialize(chunk)}\n\n", cancellationToken);
    await Response.Body.FlushAsync(cancellationToken);
}
```

This prevents wasted computation when clients navigate away.

## Testing SSE Endpoints

### With curl

```bash
curl -N -H "Content-Type: application/json" \
  -d '{"model":"gpt-4","messages":[{"role":"user","content":"Hello"}],"stream":true}' \
  https://localhost:5001/v1/chat/completions/stream
```

The `-N` flag disables buffering.

### Integration Test

```csharp
[Fact]
public async Task StreamCompletion_ReturnsChunks()
{
    var client = factory.CreateClient();
    var request = new ChatCompletionRequest(Model: "gpt-4", Messages: [...], Stream: true);

    var response = await client.PostAsJsonAsync("/v1/chat/completions/stream", request);
    response.EnsureSuccessStatusCode();

    Assert.Equal("text/event-stream", response.Content.Headers.ContentType?.MediaType);

    var stream = await response.Content.ReadAsStreamAsync();
    using var reader = new StreamReader(stream);

    var chunks = new List<string>();
    while (!reader.EndOfStream)
    {
        var line = await reader.ReadLineAsync();
        if (line?.StartsWith("data: ") == true)
        {
            chunks.Add(line[6..]); // Remove "data: " prefix
        }
    }

    Assert.NotEmpty(chunks);
    Assert.Contains("[DONE]", chunks.Last());
}
```

## Performance Considerations

- **Flush frequency**: Flush after each chunk, not after every byte. Batching 10-50ms of tokens reduces overhead.
- **Cancellation checks**: Check `cancellationToken.IsCancellationRequested` every iteration to avoid wasted work.
- **Connection limits**: SSE connections are long-lived. Monitor active connection counts and set limits.
- **Timeout configuration**: Increase Kestrel timeouts for streaming endpoints:

```csharp
builder.WebHost.ConfigureKestrel(options =>
{
    options.Limits.KeepAliveTimeout = TimeSpan.FromMinutes(10);
    options.Limits.RequestHeadersTimeout = TimeSpan.FromMinutes(10);
});
```

## When NOT to Use SSE

- **Binary data**: SSE is text-only. Use WebSockets or HTTP/2 server push.
- **Bidirectional communication**: SSE is server-to-client only. Use WebSockets.
- **Sub-second latency requirements**: SSE reconnection overhead (~1-2s) may be too high. Use WebSockets.
- **Non-browser clients**: If your client is a backend service, consider gRPC streaming instead.

## Further Reading

- [MDN: Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [OpenAI Streaming API](https://platform.openai.com/docs/api-reference/streaming)
- [ASP.NET Core IAsyncEnumerable](https://learn.microsoft.com/en-us/aspnet/core/web-api/action-return-types#iasyncenumerablet-type)
