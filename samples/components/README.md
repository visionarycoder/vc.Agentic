---
metadata-version: "1.0.0"
title: "Component initialization samples"
description: "Illustrate Manager, Engine, and Access component initialization."
document-type: "index"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# Component initialization samples

These examples instantiate the [initialization template](../../templates/components/component-initialization.md). Their names are illustrative; they do not establish approved application components or decomposition decisions.

| Capability | VaultType | Contract | Implementation |
| --- | --- | --- | --- |
| Order | Manager | [IOrderManager.cs](OrderManager/IOrderManager.cs) | [OrderManager.cs](OrderManager/OrderManager.cs) |
| Pricing | Engine | [IPricingEngine.cs](PricingEngine/IPricingEngine.cs) | [PricingEngine.cs](PricingEngine/PricingEngine.cs) |
| Inventory | Access | [IInventoryAccess.cs](InventoryAccess/IInventoryAccess.cs) | [InventoryAccess.cs](InventoryAccess/InventoryAccess.cs) |

Each class has an ILoggerFactory primary constructor, creates its concrete typed logger, and passes that logger to ComponentBase<T>. Interfaces are deliberately empty starting points.

The files assume the existing Ifx.Component base class and Microsoft.Extensions.Logging references. They are not standalone projects and have not selected package versions, namespaces for a consuming application, contract operations, proxy generation, DI registration, or service hosting. Do not register these targets directly as caller-facing component contracts.

The samples use separate files for each top-level type and explicit imports. No production framework implementation is copied here.
