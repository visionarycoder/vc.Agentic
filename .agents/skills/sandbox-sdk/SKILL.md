---
name: "sandbox-sdk"
description: "Build sandboxed applications for secure code execution. Load when building AI code execution, code interpreters, CI/CD systems, interactive dev environments, or executing untrusted code. Covers Sandbox SDK lifecycle, commands, files, code interpreter, and preview URLs. Biases towards retrieval from Cloudflare docs over pre-trained knowledge."
metadata:
  metadata-version: "1.0.0"
  title: "Cloudflare Sandbox SDK"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "optional"
---

# Cloudflare Sandbox SDK

Build secure, isolated code execution environments on Cloudflare Workers.

## FIRST: Verify Installation

```bash
npm install @cloudflare/sandbox
docker info  # Must succeed - Docker required for local dev
```

## Retrieval Sources

Your knowledge of the Sandbox SDK may be outdated. **Prefer retrieval over pre-training** for any Sandbox SDK task.

| Resource | URL |
|----------|-----|
| Docs | https://developers.cloudflare.com/sandbox/ |
| API Reference | https://developers.cloudflare.com/sandbox/api/ |
| Examples | https://github.com/cloudflare/sandbox-sdk/tree/main/examples |
| Get Started | https://developers.cloudflare.com/sandbox/get-started/ |

When implementing features, fetch the relevant doc page or example first.

## Required Configuration

**wrangler.jsonc** (exact - do not modify structure):

```jsonc
{
  "containers": [{
    "class_name": "Sandbox",
    "image": "./Dockerfile",
    "instance_type": "lite",
    "max_instances": 1
  }],
  "durable_objects": {
    "bindings": [{ "class_name": "Sandbox", "name": "Sandbox" }]
  },
  "migrations": [{ "new_sqlite_classes": ["Sandbox"], "tag": "v1" }]
}
```

**Worker entry** - must re-export Sandbox class:

```typescript
import { getSandbox } from '@cloudflare/sandbox';
export { Sandbox } from '@cloudflare/sandbox';  // Required export
```

## Quick Reference

| Task | Method |
|------|--------|
| Get sandbox | `getSandbox(env.Sandbox, 'user-123')` |
| Run command | `await sandbox.exec('python script.py')` |
| Run code (interpreter) | `await sandbox.runCode(code, { language: 'python' })` |
| Expose port | `await sandbox.exposePort(8080)` |
| Destroy | `await sandbox.destroy()` |

Defaults: `exec` timeout is 60000 ms; `createCodeContext` defaults to language `python` and cwd `/workspace` with a 30000 ms request timeout. `runCode` reports failures in `result.error`; `exec` returns `{ stdout, stderr, exitCode, success }`.

## When to Use What

Use `exec()` for shell commands, scripts, and build/test pipelines. Use `runCode()` for LLM-generated code and data analysis (rich outputs, state persistence). Create explicit contexts with `createCodeContext` for production; state persists within a context (languages: `python`, `javascript`, `typescript`).

## Extending the Dockerfile

Base image (`docker.io/cloudflare/sandbox:0.7.0`) includes Python 3.11, Node.js 20, and common tools. Extend it with `FROM docker.io/cloudflare/sandbox:0.7.0` plus `RUN` installs, and keep `EXPOSE 8080` for local port exposure. Keep images lean; size affects cold start.

## Preview URLs

Preview URLs from `exposePort()` need a custom domain with wildcard DNS (`*.yourdomain.com`); `.workers.dev` does not support them. See https://developers.cloudflare.com/sandbox/guides/expose-services/

## OpenAI Agents SDK Integration

Helpers live at `@cloudflare/sandbox/openai` (`Shell`, `Editor`); see `examples/openai-agents`.

## Lifecycle

Containers sleep after 10 minutes of inactivity (`sleepAfter`; `keepAlive: true` prevents it). `getSandbox()` returns immediately and the container starts lazily.

## Anti-Patterns

- Don't use internal clients (`CommandClient`, `FileClient`); use `sandbox.*` methods.
- Don't hardcode sandbox IDs for multi-user; use user or session identifiers.
- Call `destroy()` for temporary sandboxes.

## Detailed References

- **[references/api-quick-ref.md](references/api-quick-ref.md)** - Full API with options and return types
- **[references/examples.md](references/examples.md)** - Example index with use cases
