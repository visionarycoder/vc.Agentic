---
name: "kubernetes-dotnet"
description: "Deploy, configure, scale, observe, and update .NET applications on Kubernetes with health probes, secure configuration, and platform integration patterns."
metadata:
  metadata-version: "1.0.0"
  title: "Kubernetes for .NET"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-23"
  collection: "dotnet"
---

# Kubernetes for .NET

Agent deploys .NET workloads to Kubernetes with clear workload manifests, probe contracts, configuration surfaces, rollout controls, scaling rules, and cluster-facing observability.

## When to Use

| Condition | Use |
|---|---|
| .NET service deploys to Kubernetes or OpenShift-style clusters | Use this skill |
| Team needs Deployment, Service, Ingress, or Helm guidance for a .NET app | Use this skill |
| Workload needs readiness, liveness, startup probes, HPA, or rollout tuning | Use this skill |
| Request combines .NET Aspire resources with Kubernetes packaging | Use this skill |
| Platform design includes Prometheus, Grafana, or service mesh integration | Use this skill |

## When Not to Use

| Condition | Route |
|---|---|
| Request focuses on image construction only | Use `docker-dotnet` |
| Request focuses on one ASP.NET Core health endpoint implementation | Use `health-checks-aspnetcore` |
| Request focuses on local AppHost orchestration without cluster deployment | Use `aspire-orchestration` |
| Workload targets a single VM, App Service, or Windows Service host | Use the matching deployment skill for that platform |

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| Workload type | Yes | API, worker, gRPC, scheduled job, or stateful service |
| Image contract | Yes | Registry, tag strategy, ports, and startup command |
| Configuration model | Yes | ConfigMaps, Secrets, mounted files, and external providers |
| Traffic model | Yes | Internal-only, cluster ingress, gateway, or mesh |
| SLO and scaling signals | Yes | CPU, memory, queue depth, request rate, and rollout constraints |

## Project-Specific Rules

- Keep Aspire AppHost resource names and environment contracts identical to cluster manifests.
- Add a sidecar service mesh only for a stated mTLS, traffic, or telemetry outcome; otherwise record the non-mesh path.
- Verify Service DNS resolution, ingress routing, and scrape or trace configuration; restart one stateful pod when storage is in scope.

## Outputs

- Kubernetes or Helm pattern matched to the .NET workload type
- Externalized config, secret, probe, resource, and rollout model
- Autoscaling, ingress, storage, and monitoring guidance
- Verification checks for readiness, routing, scaling, and observability
