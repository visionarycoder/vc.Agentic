---
title: Project Topology
doc_type: reference
status: active
last_updated: 2026-11-09
---
# Project Topology

## Illustrative physical layout

Use the accepted component design and repository conventions. This example does
not mandate project counts, hosting technology or a solution format.

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

Create or reuse only the projects required by the assigned accepted design.
The following are illustrative names:

```text
<VaultType>.<Capability>.Contract
<VaultType>.<Capability>.Service
<VaultType>.<Capability>.Service.UnitTests
<VaultType>.<Capability>.Service.IntegrationTests
```

## Solution

Use the repository's accepted solution format; use `.slnx` when selected there.

Mirror the physical hierarchy with solution folders:

```text
<VaultType>/
  <Capability>/
    <all component projects>
```

Add every generated or reused project if it is missing from the selected `.slnx`.

Do not create duplicate solution entries or duplicate project references on rerun.
