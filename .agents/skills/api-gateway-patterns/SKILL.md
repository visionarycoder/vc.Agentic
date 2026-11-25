---
name: "api-gateway-patterns"
description: "Design API gateway or edge layers with explicit routing, bounded transforms, ownership of cross-cutting policy, and observable traffic controls."
metadata:
  metadata-version: "1.0.0"
  title: "API Gateway Patterns"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-24"
  collection: "optional"
---

# API Gateway Patterns

Design gateway layers with explicit routing, bounded transforms, and observable traffic controls.

## When to Use

- A reverse proxy, edge gateway, or backend-for-frontend fronts multiple downstream APIs.
- Auth delegation, throttling, transformation, or aggregation is centralized at ingress.
- Gateway and service-mesh responsibilities must be separated.

Do not use it for a single API without a cross-service ingress layer, east-west policy inside a cluster, or static-content and CDN rules.

## Required Inputs

| Input | Notes |
|---|---|
| Downstream inventory | Services, route groups, protocols, ownership |
| Traffic goals | Routing, aggregation, throttling, auth delegation, transformation |
| Deployment topology | Self-hosted, managed edge, container platform, or hybrid |
| Failure posture | Timeout budget, breaker thresholds, retry ownership, fallback intent |
| Consumer set | Web, mobile, partner, internal, admin (optional) |

## Layering

| Scenario | Pattern | Guardrail |
|---|---|---|
| In-process proxy with custom middleware | Self-hosted gateway service | Keep policy code bounded and observable |
| Configuration-driven gateway with built-in aggregation | Declarative gateway | Keep extension scope narrow |
| Managed external edge with subscriptions and portal | Managed API management | Keep platform and application responsibilities separate |
| Managed edge plus internal composition | Two layers | Record which layer owns auth, throttling, and transforms |
| Public ingress plus internal service policy | Gateway plus service mesh | Gateway owns north-south traffic; mesh owns service-to-service |

## Rules

| Topic | Rule |
|---|---|
| Boundary ownership | Business logic stays in downstream services; ingress, composition, and cross-cutting policy stay in the gateway |
| Transforms | Use request and response transforms only when the caller contract requires them |
| Retry safety | No automatic retries for non-idempotent requests unless idempotency is defined |
| Aggregation | Aggregate a small set of latency-related calls with explicit failure semantics |
| Policy duplication | Auth and quota are enforced once; never conflicting across layers |
| Observability | Propagate correlation ids; capture downstream timing and failure class |
| Route design | Define route matching, destination groups, health probes, and load-balancing policy explicitly |

## Verification

| Check | Pass |
|---|---|
| Call representative routes | Requests reach the intended downstream |
| Repeated requests across healthy destinations | Distribution follows the selected policy |
| Inspect outbound headers, path, query, body | Downstream receives the intended contract |
| Exceed one client quota | Intended rejection result |
| Valid, missing, and insufficient credentials | Intended auth outcome; only intended identity context is forwarded |
| Slow or failing downstream | Gateway short-circuits or rejects per configuration |
| Inspect logs, traces, metrics, health | Route selection, latency, and failures are visible |

## Outputs

- Gateway layering decision
- Route, destination, and load-balancing plan
- Transformation and aggregation contract plan
- Auth, throttling, and resilience ownership plan
- Verification evidence for routing, failure behavior, and observability
