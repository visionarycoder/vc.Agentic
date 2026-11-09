---
name: "maui-devflow-debug"
description: "Diagnose and recover MauiDevFlow failures in .NET MAUI apps. Use when MauiDevFlow MCP tools time out, report no agents, cannot reach an agent, return transport errors, or fail after the app launches."
metadata:
  metadata-version: "1.0.0"
  title: "MauiDevFlow Debugging"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# MauiDevFlow Debugging

Use evidence to identify the failing layer before retrying or changing the app.

## Failure Layers

Treat these as separate checkpoints:

1. **Build integration** - the agent package and `MAUI_DEVFLOW` initialization code are present in the launched build.
2. **Broker registration** - the running app appears in the broker's agent list.
3. **Agent reachability** - `maui_status` can contact the selected agent and report its identity.
4. **UI automation** - `maui_tree` can execute on the app UI thread.

Passing one checkpoint does not prove the next one works. In particular, an agent listed by the broker may still be unreachable.

## First Failure Workflow

1. Preserve the exact failing tool name, parameters, and first meaningful error.
2. If the app may still be starting, call `maui_wait` once. Do not replace it with arbitrary sleeps.
3. If the failure remains, call `dotnet_maui_diagnoseDevFlow` immediately instead of repeating the same MCP call.
   - This tool invokes the extension's bundled MAUI CLI independently of the MCP connection.
   - It reports `complete` or `partial`; never describe a `partial` report as a clean diagnostic result.
   - Inspect CLI version, broker status and port, agent registration/details, exact version mismatches, the selected startup project and whether the CLI discovered it, Android forwarding data, and DevFlow-filtered app debug output.
   - The tool automatically targets the active running Android device. Pass `deviceId` only when that target cannot be resolved.
4. Apply only the recovery that matches the evidence.
5. Verify recovery with `maui_status`, then `maui_tree`. A successful `maui_list_agents` result alone is insufficient.

Stop after two identical failures. Re-read the first meaningful error and change the hypothesis rather than looping through list/wait/status calls.

## Evidence-Based Recovery

| Evidence | Interpretation | Targeted action |
|---|---|---|
| Diagnostics are `partial` | The CLI diagnostic command itself failed | Use `diagnosticError` and `appDebugOutput`; check the bundled CLI/runtime error before changing app code |
| `brokerRunning=false` | The broker layer is unavailable | Restart the MAUI debug session once so the extension and app can re-establish DevFlow; then diagnose again |
| `agentCount=0` | No running app is currently registered | Confirm the intended app is running, inspect DevFlow debug output, then check build integration and platform requirements |
| `agentCount>0`, `maui_status` fails | Registration works but transport does not | Check Android forwarding, stale agent selection, and CLI/agent version mismatch |
| `maui_status` works, `maui_tree` fails | Transport works but UI automation does not | Inspect `maui_logs` and app debug output for dispatcher, startup, or unhandled-exception failures |
| `versionMismatch=true` | CLI and in-app agent builds differ | Clear the NuGet HTTP cache and rebuild with `MauiDevFlowEnabled=true` |
| `startupProjectDetectedByCli=false` | The selected project was not found by the CLI's static scan | This is expected for extension-managed injection; verify the selected project, `MauiProgram.cs`, and launched build instead of adding a permanent package reference |

An empty agent list is runtime state, not proof that source integration is missing.

## Integration Checks

The extension injects `Microsoft.Maui.DevFlow.Agent` for supported Debug builds. Do not add a permanent package reference to the app project.

`MauiProgram.cs` must initialize the agent:

```csharp
#if MAUI_DEVFLOW
using Microsoft.Maui.DevFlow.Agent;
#endif

#if MAUI_DEVFLOW
builder.AddMauiDevFlowAgent();
#endif
```

For Blazor Hybrid apps, also add `using Microsoft.Maui.DevFlow.Blazor;` and `builder.AddMauiBlazorDevFlowTools();` inside the same conditional blocks.

Mac Catalyst requires `com.apple.security.network.server` set to `true` in `Platforms/MacCatalyst/Entitlements.plist`.

## Android Connectivity

Android emulators require two tunnels with different directions:

```bash
adb reverse tcp:19223 tcp:19223
adb forward tcp:<agent-port> tcp:<agent-port>
```

- `reverse` lets the in-app agent reach the host broker.
- `forward` lets the host CLI/MCP server reach the in-app HTTP agent.
- Never use `adb reverse` for the agent port.
- Use the port reported by diagnostics or the selected agent; do not assume a fixed port.

The extension normally creates these tunnels. Use manual commands only as a targeted fallback when diagnostics show the expected mapping is missing.

## Version Recovery

When diagnostics show a mismatch:

```bash
dotnet nuget locals http-cache --clear
dotnet build -p:MauiDevFlowEnabled=true
```

Stop the active debug session before rebuilding. If the project contains a manually added `Microsoft.Maui.DevFlow.Agent` package reference, remove it so the extension can inject its compatible version.

## Evidence to Preserve

Before applying a workaround, retain:

- Exact tool and sanitized parameters
- First meaningful error
- Diagnostic status and failing layer
- Platform, target framework, and device category
- CLI and agent versions
- Minimal DevFlow app log excerpt

Do not include credentials, tokens, request bodies, user data, or unrelated application logs.
