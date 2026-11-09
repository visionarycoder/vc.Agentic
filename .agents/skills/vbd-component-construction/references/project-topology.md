---
title: Project Topology
doc_type: reference
status: active
last_updated: 2026-08-14
---
# Project Topology

## Default physical layout

```text
src/
  <VaultType>/
    <Capability>/
      README.md
      <VaultType>.<Capability>.Contract/
      <VaultType>.<Capability>.Service/
      <VaultType>.<Capability>.Host/                 # optional
      <VaultType>.<Capability>.Simulator/            # optional
      <VaultType>.<Capability>.Emulator/             # optional
      <VaultType>.<Capability>.Orm.<Resource>/       # Access only

tests/
  <VaultType>/
    <Capability>/
      <VaultType>.<Capability>.Service.UnitTests/
      <VaultType>.<Capability>.Service.IntegrationTests/
      <VaultType>.<Capability>.Orm.<Resource>.IntegrationTests/  # Access ORM only
```

## Project kinds

| Project | Kind |
|---|---|
| Contract | Class library |
| Service | Class library |
| ORM | Class library |
| Host | Worker Service by default |
| Simulator | Console app |
| Emulator | Console app |
| UnitTests | Repository-selected test project |
| IntegrationTests | Repository-selected test project |

## Required projects

Always create:

```text
<VaultType>.<Capability>.Contract
<VaultType>.<Capability>.Service
<VaultType>.<Capability>.Service.UnitTests
<VaultType>.<Capability>.Service.IntegrationTests
```

## Solution

Use `.slnx`.

Mirror the physical hierarchy with solution folders:

```text
<VaultType>/
  <Capability>/
    <all component projects>
```

Add every generated or reused project if it is missing from the selected `.slnx`.

Do not create duplicate solution entries or duplicate project references on rerun.
