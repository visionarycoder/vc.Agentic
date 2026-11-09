# VBD ServiceModel Default Path

Use this reference with [../SKILL.md](../SKILL.md) when building or reviewing manager, engine, or access vault work.

## Default Order

1. Start with [vbd-service-model](../../vbd-service-contracts/SKILL.md).
2. Apply [vbd-rules](../SKILL.md) for the canonical volatility rules.
3. Use the role skill only for the specific vault shape:
   - [vbd-manager-vault](../../vbd-manager-components/SKILL.md)
   - [vbd-engine-vault](../../vbd-engine-components/SKILL.md)
   - [vbd-access-vault](../../vbd-access-components/SKILL.md)
4. Use [token-efficient-implementation](../../token-efficient-implementation/SKILL.md) for the actual slice.

## ServiceModel Is The Default

- Treat the service model as the required starting point for VBD vault work.
- Do not restate boundary rules in every skill when this reference already covers them.
- Keep manager, engine, and access skills focused on role-specific shape and diagnostics.

## Shared Shape

- `Contract` project: public boundary surface.
- `Service` project: internal implementation details.
- DI: bind contract to implementation at the composition root.
- Managers communicate with sibling managers through the shared message bus wrapper.
- Generated implementations should keep `ILogger<T> logger` first and trailing `CancellationToken ct` on public async methods when supported.
