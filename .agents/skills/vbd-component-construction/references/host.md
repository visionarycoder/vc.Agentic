---
title: Host Scaffold
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Host Scaffold

Host is optional. Ask every time; default to not creating it.

## Naming

```text
<VaultType>.<Capability>.Host
```

Do not use `Worker` in the project name. Worker Service is the default technology, not the architectural name.

## Default technology

Use the .NET Worker Service template unless the repository or developer selects another host technology.

## Responsibilities

Host may own:

- startup
- configuration
- dependency composition
- runtime selection of Service/Simulator/Emulator
- observability
- hosting lifecycle

Host must not own component business behavior.

## References

Reference Service by default.

Do not add a direct Contract reference unless Host source code actually requires Contract types.

Do not add direct ORM or downstream-vault references merely because the Host exists.
